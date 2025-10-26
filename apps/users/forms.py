"""
Forms for User management
"""
from django import forms
from apps.accounts.models import AdminUser


class UserCreateForm(forms.ModelForm):
    """Form for creating new users"""
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    
    class Meta:
        model = AdminUser
        fields = ['name', 'email', 'role', 'download_limit']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'role': forms.Select(attrs={'class': 'form-control'}),
            'download_limit': forms.NumberInput(attrs={'class': 'form-control'}),
        }


class UserEditForm(forms.ModelForm):
    """Form for editing users"""
    
    class Meta:
        model = AdminUser
        fields = ['name', 'email', 'role', 'download_limit', 'is_active']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'role': forms.Select(attrs={'class': 'form-control'}),
            'download_limit': forms.NumberInput(attrs={'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

