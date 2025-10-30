"""
Contact views - CRUD operations
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views import View
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
import pandas as pd
import io

from apps.contacts.models import Contact
from apps.contacts.forms import ContactForm, ContactFilterForm
from services.contact_service import ContactService


class ContactListView(LoginRequiredMixin, ListView):
    """Contact list view with search and filters"""
    model = Contact
    template_name = 'contacts/list.html'
    context_object_name = 'contacts'
    paginate_by = 25
    
    def get_queryset(self):
        """Filter contacts based on query parameters"""
        queryset = Contact.objects.all()
        
        # Search
        search = self.request.GET.get('search', '')
        if search:
            from django.db.models import Q
            queryset = queryset.filter(
                Q(full_name__icontains=search) |
                Q(company__icontains=search) |
                Q(email__icontains=search)
            )
        
        # Filter by industry
        industry = self.request.GET.getlist('industry')
        if industry:
            queryset = queryset.filter(industry__in=industry)
        
        # Filter by country
        country = self.request.GET.getlist('country')
        if country:
            queryset = queryset.filter(country__in=country)
        
        return queryset.order_by('-created_at')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Get unique values for filter dropdowns
        context['industries'] = Contact.objects.filter(industry__isnull=False).values_list('industry', flat=True).distinct()
        context['countries'] = Contact.objects.filter(country__isnull=False).values_list('country', flat=True).distinct()
        
        # Add search query
        context['search'] = self.request.GET.get('search', '')
        
        return context


class ContactCreateView(LoginRequiredMixin, View):
    """Create new contact"""
    
    def get(self, request):
        form = ContactForm()
        return render(request, 'contacts/form.html', {'form': form, 'action': 'Add'})
    
    def post(self, request):
        form = ContactForm(request.POST)
        if form.is_valid():
            try:
                contact = ContactService.create_contact(form.cleaned_data)
                messages.success(request, f'Contact "{contact.full_name}" created successfully!')
                return redirect('contacts:list')
            except ValueError as e:
                messages.error(request, f'Validation error: {str(e)}')
        
        return render(request, 'contacts/form.html', {'form': form, 'action': 'Add'})


class ContactUpdateView(LoginRequiredMixin, View):
    """Update existing contact"""
    
    def get(self, request, pk):
        contact = get_object_or_404(Contact, pk=pk)
        form = ContactForm(instance=contact)
        return render(request, 'contacts/form.html', {'form': form, 'action': 'Edit', 'contact': contact})
    
    def post(self, request, pk):
        contact = get_object_or_404(Contact, pk=pk)
        form = ContactForm(request.POST, instance=contact)
        
        if form.is_valid():
            try:
                updated = ContactService.update_contact(pk, form.cleaned_data)
                if updated:
                    messages.success(request, f'Contact "{updated.full_name}" updated successfully!')
                    return redirect('contacts:list')
                else:
                    messages.error(request, 'Failed to update contact')
            except ValueError as e:
                messages.error(request, f'Validation error: {str(e)}')
        
        return render(request, 'contacts/form.html', {'form': form, 'action': 'Edit', 'contact': contact})


class ContactDeleteView(LoginRequiredMixin, DeleteView):
    """Delete contact"""
    model = Contact
    template_name = 'contacts/delete_confirm.html'
    success_url = reverse_lazy('contacts:list')
    
    def delete(self, request, *args, **kwargs):
        contact = self.get_object()
        if ContactService.delete_contact(contact.id):
            messages.success(request, f'Contact "{contact.full_name}" deleted successfully!')
        else:
            messages.error(request, 'Failed to delete contact')
        return redirect(self.success_url)


class ContactExportView(LoginRequiredMixin, View):
    """Export contacts to CSV"""
    
    def post(self, request):
        # Get contacts
        contacts = Contact.objects.all()
        
        # Apply filters if provided
        industry = request.POST.getlist('industry')
        if industry:
            contacts = contacts.filter(industry__in=industry)
        
        country = request.POST.getlist('country')
        if country:
            contacts = contacts.filter(country__in=country)
        
        # Create DataFrame
        data = []
        for contact in contacts:
            data.append({
                'ID': contact.id,
                'First Name': contact.first_name,
                'Last Name': contact.last_name,
                'Full Name': contact.full_name,
                'Email': contact.email,
                'Phone': contact.phone,
                'Company': contact.company,
                'Industry': contact.industry,
                'Title': contact.title,
                'Website': contact.website,
                'City': contact.city,
                'State': contact.state,
                'Country': contact.country,
                'LinkedIn': contact.linkedin,
                'Notes': contact.notes,
                'Created': contact.created_at.strftime('%Y-%m-%d') if contact.created_at else ''
            })
        
        df = pd.DataFrame(data)
        
        # Generate CSV
        output = io.BytesIO()
        df.to_csv(output, index=False)
        output.seek(0)
        
        response = HttpResponse(output, content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="contacts_export.csv"'
        
        return response


@login_required
def bulk_export_api(request):
    """Export selected contacts"""
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    
    try:
        import json
        data = json.loads(request.body)
        contact_ids = data.get('contact_ids', [])
        format_type = data.get('format', 'csv')
        
        if not contact_ids:
            return JsonResponse({'error': 'No contacts selected'}, status=400)
        
        # Get contacts
        contacts = Contact.objects.filter(id__in=contact_ids)
        
        if not contacts.exists():
            return JsonResponse({'error': 'No contacts found'}, status=404)
        
        # Prepare data
        data_list = []
        for contact in contacts:
            data_list.append({
                'Name': contact.full_name,
                'Email': contact.email,
                'Phone': contact.phone,
                'Company': contact.company,
                'Industry': contact.industry,
                'Title': contact.title,
                'Website': contact.website,
                'City': contact.city,
                'State': contact.state,
                'Country': contact.country,
                'LinkedIn': contact.linkedin,
                'Notes': contact.notes,
                'Created': contact.created_at.strftime('%Y-%m-%d') if contact.created_at else ''
            })
        
        df = pd.DataFrame(data_list)
        
        if format_type.lower() == 'csv':
            # Generate CSV
            output = io.BytesIO()
            df.to_csv(output, index=False)
            output.seek(0)
            
            response = HttpResponse(output, content_type='text/csv')
            response['Content-Disposition'] = f'attachment; filename="contacts_export_{len(contact_ids)}_contacts.csv"'
            
            return response
        else:
            return JsonResponse({'error': 'Unsupported format'}, status=400)
            
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@login_required
def bulk_delete_api(request):
    """Delete selected contacts"""
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    
    try:
        import json
        data = json.loads(request.body)
        contact_ids = data.get('contact_ids', [])
        
        if not contact_ids:
            return JsonResponse({'error': 'No contacts selected'}, status=400)
        
        # Get contacts
        contacts = Contact.objects.filter(id__in=contact_ids)
        
        if not contacts.exists():
            return JsonResponse({'error': 'No contacts found'}, status=404)
        
        # Delete contacts
        deleted_count = contacts.count()
        contacts.delete()
        
        return JsonResponse({
            'success': True,
            'message': f'{deleted_count} contacts deleted successfully',
            'deleted_count': deleted_count
        })
        
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@login_required
def bulk_update_api(request):
    """Update selected contacts"""
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    
    try:
        import json
        data = json.loads(request.body)
        contact_ids = data.get('contact_ids', [])
        field = data.get('field')
        value = data.get('value')
        
        if not contact_ids:
            return JsonResponse({'error': 'No contacts selected'}, status=400)
        
        if not field:
            return JsonResponse({'error': 'Field is required'}, status=400)
        
        # Get contacts
        contacts = Contact.objects.filter(id__in=contact_ids)
        
        if not contacts.exists():
            return JsonResponse({'error': 'No contacts found'}, status=404)
        
        # Validate field
        valid_fields = ['company', 'industry', 'title', 'city', 'state', 'country']
        if field not in valid_fields:
            return JsonResponse({'error': f'Invalid field. Allowed fields: {", ".join(valid_fields)}'}, status=400)
        
        # Update contacts
        updated_count = contacts.update(**{field: value})
        
        return JsonResponse({
            'success': True,
            'message': f'{updated_count} contacts updated successfully',
            'updated_count': updated_count
        })
        
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
