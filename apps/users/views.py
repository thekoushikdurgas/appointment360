"""
Views for User management
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from apps.accounts.models import AdminUser
from .forms import UserCreateForm, UserEditForm


@login_required
def user_list_view(request):
    """
    List all users
    """
    if request.user.role != 'admin':
        messages.error(request, 'Access denied. Admin only.')
        return redirect('dashboard:index')
    
    users = AdminUser.objects.all().order_by('-date_joined')
    
    return render(request, 'admin/users/list.html', {
        'users': users
    })


@login_required
def user_create_view(request):
    """
    Create new user
    """
    if request.user.role != 'admin':
        messages.error(request, 'Access denied. Admin only.')
        return redirect('dashboard:index')
    
    if request.method == 'POST':
        form = UserCreateForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.created_by = request.user
            user.save()
            messages.success(request, 'User created successfully.')
            return redirect('users:list')
    else:
        form = UserCreateForm()
    
    return render(request, 'admin/users/create.html', {
        'form': form
    })


@login_required
def user_edit_view(request, user_id):
    """
    Edit existing user
    """
    if request.user.role != 'admin':
        messages.error(request, 'Access denied. Admin only.')
        return redirect('dashboard:index')
    
    user = get_object_or_404(AdminUser, id=user_id)
    
    if request.method == 'POST':
        form = UserEditForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'User updated successfully.')
            return redirect('users:list')
    else:
        form = UserEditForm(instance=user)
    
    return render(request, 'admin/users/create.html', {
        'form': form,
        'user': user
    })


@login_required
def user_column_settings_view(request, user_id):
    """
    Manage column permissions for a user
    """
    if request.user.role != 'admin':
        messages.error(request, 'Access denied. Admin only.')
        return redirect('dashboard:index')
    
    user = get_object_or_404(AdminUser, id=user_id)
    
    if request.method == 'POST':
        # Handle column permissions save
        columns = request.POST.getlist('columns')
        user.column_allowed = {'columns': columns}
        user.save()
        messages.success(request, 'Column permissions updated successfully.')
        return redirect('users:list')
    
    # Get available columns from Contact model
    from apps.contacts.models import Contact
    available_columns = [f.name for f in Contact._meta.fields if f.name not in ['id', 'created_at', 'updated_at']]
    
    allowed_columns = user.column_allowed.get('columns', []) if user.column_allowed else []
    
    return render(request, 'admin/users/column.html', {
        'user': user,
        'available_columns': available_columns,
        'allowed_columns': allowed_columns
    })

