"""
Views for Contact management
"""
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
from .models import Contact, Industry
from .serializers import ContactSerializer, ContactListSerializer, IndustrySerializer
import logging

logger = logging.getLogger(__name__)


class ContactViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Contact CRUD operations
    Supports advanced filtering, search, and export
    """
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer
    permission_classes = [IsAuthenticated]
    
    def get_serializer_class(self):
        if self.action == 'list':
            return ContactListSerializer
        return ContactSerializer
    
    def get_queryset(self):
        queryset = Contact.objects.all()
        
        # Advanced filtering
        params = self.request.query_params
        
        # Name search
        name_search = params.get('name_search', '')
        if name_search:
            queryset = queryset.filter(
                Q(first_name__icontains=name_search) | 
                Q(last_name__icontains=name_search)
            )
        
        # Location filter
        location = params.get('location', '')
        if location:
            queryset = queryset.filter(
                Q(city__iexact=location) | 
                Q(state__iexact=location) | 
                Q(country__iexact=location)
            )
        
        # Industry filter
        industries = params.getlist('industry')
        if industries:
            queryset = queryset.filter(industry__in=industries)
        
        # Email status filter
        email_status = params.getlist('email_status')
        if email_status:
            queryset = queryset.filter(email_status__in=email_status)
        
        # Employee range filter
        min_employees = params.get('min_employees')
        max_employees = params.get('max_employees')
        if min_employees or max_employees:
            if min_employees and max_employees:
                queryset = queryset.filter(employees__gte=min_employees, employees__lte=max_employees)
            elif min_employees:
                queryset = queryset.filter(employees__gte=min_employees)
            elif max_employees:
                queryset = queryset.filter(employees__lte=max_employees)
        
        # Revenue range filter
        min_revenue = params.get('min_revenue')
        max_revenue = params.get('max_revenue')
        if min_revenue or max_revenue:
            if min_revenue and max_revenue:
                queryset = queryset.filter(annual_revenue__gte=min_revenue, annual_revenue__lte=max_revenue)
            elif min_revenue:
                queryset = queryset.filter(annual_revenue__gte=min_revenue)
            elif max_revenue:
                queryset = queryset.filter(annual_revenue__lte=max_revenue)
        
        # Technology filter
        technologies = params.getlist('technologies')
        if technologies:
            for tech in technologies:
                queryset = queryset.filter(technologies__icontains=tech)
        
        return queryset
    
    @action(detail=False, methods=['get'])
    def autocomplete(self, request):
        """
        Autocomplete endpoint for search suggestions
        """
        field = request.query_params.get('field', 'name')
        query = request.query_params.get('q', '')
        
        if not query:
            return Response([])
        
        if field == 'technologies':
            results = Contact.objects.filter(technologies__icontains=query).values_list('technologies', flat=True).distinct()[:10]
            # Parse comma-separated technologies
            suggestions = []
            for techs in results:
                if techs:
                    tech_list = [t.strip() for t in techs.split(',') if t.strip()]
                    suggestions.extend([t for t in tech_list if query.lower() in t.lower()])
            suggestions = list(set(suggestions))[:10]
            return Response([{'value': s} for s in suggestions])
        
        elif field == 'keywords':
            results = Contact.objects.filter(keywords__icontains=query).values_list('keywords', flat=True).distinct()[:10]
            suggestions = []
            for keywords in results:
                if keywords:
                    kw_list = [k.strip() for k in keywords.split(',') if k.strip()]
                    suggestions.extend([k for k in kw_list if query.lower() in k.lower()])
            suggestions = list(set(suggestions))[:10]
            return Response([{'value': s} for s in suggestions])
        
        elif field == 'revenue':
            results = Contact.objects.filter(annual_revenue__isnull=False).values_list('annual_revenue', flat=True).distinct()[:10]
            return Response([{'value': str(r)} for r in results])
        
        else:
            # Default: search by field
            results = Contact.objects.values_list(field, flat=True).distinct().filter(
                **{f'{field}__icontains': query}
            )[:10]
            return Response([{'value': str(v)} for v in results])
    
    @action(detail=False, methods=['post'])
    def export(self, request):
        """
        Export selected contacts to Excel
        """
        from .utils import export_contacts_to_excel
        
        contact_ids = request.data.get('contact_ids', [])
        selected_fields = request.data.get('fields', None)
        
        if not contact_ids:
            return Response({
                'success': False,
                'message': 'No contact IDs provided'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        contacts = Contact.objects.filter(id__in=contact_ids)
        
        if not contacts.exists():
            return Response({
                'success': False,
                'message': 'No contacts found'
            }, status=status.HTTP_404_NOT_FOUND)
        
        # Export to Excel
        try:
            excel_data = export_contacts_to_excel(contacts, selected_fields)
            filename = f"contacts_export_{self.request.user.id}.xlsx"
            
            return Response({
                'success': True,
                'filename': filename,
                'file': f'data:application/vnd.ms-excel;base64,{excel_data}'
            })
        except Exception as e:
            logger.error(f"Export failed: {str(e)}")
            return Response({
                'success': False,
                'message': f'Export failed: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class IndustryViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for Industry (read-only)
    """
    queryset = Industry.objects.filter(is_active=True)
    serializer_class = IndustrySerializer
    permission_classes = [IsAuthenticated]


# Template-based views for web interface
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages


@login_required
def contact_list_view(request):
    """
    Web-based contact list view with advanced filtering
    """
    # Get filter options
    industries = Industry.objects.filter(is_active=True).values_list('name', flat=True).distinct()
    job_titles = Contact.objects.exclude(title__isnull=True).exclude(title='').values_list('title', flat=True).distinct()[:100]
    
    # Get initial filters from query params
    filters = {
        'name': request.GET.get('name', ''),
        'job_titles': request.GET.getlist('job_titles', []),
        'industry': request.GET.getlist('industry', []),
        'location': request.GET.get('location', ''),
        'employees_range': request.GET.getlist('employees_range', []),
        'email_status': request.GET.getlist('email_status', []),
        'technologies': request.GET.getlist('technologies', []),
        'revenue_min': request.GET.get('min_rev', ''),
        'revenue_max': request.GET.get('max_rev', ''),
        'linkedin': request.GET.get('LinkedIn', ''),
    }
    
    context = {
        'industries': industries,
        'job_titles': job_titles,
        'filters': filters,
    }
    
    return render(request, 'admin/contacts/list.html', context)


@login_required
def contact_create_view(request):
    """
    Web-based contact create/edit view
    """
    contact = None
    contact_id = request.GET.get('id')
    
    if contact_id:
        try:
            contact = Contact.objects.get(id=contact_id)
        except Contact.DoesNotExist:
            messages.error(request, 'Contact not found.')
            return redirect('contacts:list')
    
    # Get all columns except id and timestamps
    from django.db import connection
    
    columns = [f[0] for f in Contact._meta.fields if f.column not in ['id', 'created_at', 'updated_at', 'contact_id', 'account_id']]
    
    if request.method == 'POST':
        # Handle form submission
        form_data = {}
        for col in columns:
            form_data[col] = request.POST.get(col, '')
        
        if contact:
            for key, value in form_data.items():
                setattr(contact, key, value)
            contact.save()
            messages.success(request, 'Contact updated successfully.')
        else:
            contact = Contact(**form_data)
            contact.save()
            messages.success(request, 'Contact created successfully.')
        
        return redirect('contacts:list')
    
    context = {
        'contact': contact,
        'columns': columns,
    }
    
    return render(request, 'admin/contacts/create.html', context)


@login_required
def contact_import_view(request):
    """
    Web-based contact import view
    """
    return render(request, 'admin/contacts/import.html')
