"""
Views for Parcel Type management
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import ParcelType
import logging

logger = logging.getLogger(__name__)


@login_required
def parcel_type_list_view(request):
    """
    List all parcel types
    """
    parcel_types = ParcelType.objects.all().order_by('-created_at')
    
    return render(request, 'admin/parcels/list.html', {
        'parcel_types': parcel_types
    })


@login_required
def parcel_type_create_view(request):
    """
    Create or edit a parcel type
    """
    parcel_type_id = request.GET.get('id')
    parcel_type = None
    
    if parcel_type_id:
        try:
            parcel_type = ParcelType.objects.get(id=parcel_type_id)
        except ParcelType.DoesNotExist:
            messages.error(request, 'Parcel type not found.')
            return redirect('parcels:list')
    
    if not parcel_type:
        parcel_type = ParcelType()
        parcel_type.status = 'n'
    
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description', '')
        price = request.POST.get('price')
        status = request.POST.get('status', 'n')
        
        if name:
            parcel_type.name = name
            parcel_type.description = description
            parcel_type.status = status
            
            if price:
                try:
                    parcel_type.price = float(price)
                except ValueError:
                    parcel_type.price = None
            
            # Handle image upload if needed
            image = request.POST.get('parcel_type_image')
            if image:
                parcel_type.image = image
            
            parcel_type.save()
            
            if parcel_type_id:
                messages.success(request, 'Parcel type updated successfully.')
            else:
                messages.success(request, 'Parcel type created successfully.')
            
            return redirect('parcels:list')
        else:
            messages.error(request, 'Name is required.')
    
    return render(request, 'admin/parcels/create.html', {
        'parcel_type': parcel_type
    })


@login_required
def parcel_type_delete_view(request, parcel_type_id):
    """
    Delete a parcel type
    """
    try:
        parcel_type = ParcelType.objects.get(id=parcel_type_id)
        parcel_type.delete()
        messages.success(request, 'Parcel type deleted successfully.')
    except ParcelType.DoesNotExist:
        messages.error(request, 'Parcel type not found.')
    
    return redirect('parcels:list')
