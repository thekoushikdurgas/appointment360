"""
Contact forms
"""
from django import forms
from apps.contacts.models import Contact


class ContactForm(forms.ModelForm):
    """Contact form"""
    
    class Meta:
        model = Contact
        fields = [
            'first_name', 'last_name', 'email', 'phone',
            'company', 'industry', 'title', 'website',
            'city', 'state', 'country', 'linkedin',
            'notes', 'is_active'
        ]
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'required': True}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'required': True}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'company': forms.TextInput(attrs={'class': 'form-control'}),
            'industry': forms.Select(attrs={'class': 'form-select'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'website': forms.URLInput(attrs={'class': 'form-control'}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
            'state': forms.TextInput(attrs={'class': 'form-control'}),
            'country': forms.TextInput(attrs={'class': 'form-control'}),
            'linkedin': forms.URLInput(attrs={'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email and Contact.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError("Email already exists")
        return email


class ContactFilterForm(forms.Form):
    """Contact filter form"""
    search = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Search by name, company, email...'
        })
    )
    industry = forms.MultipleChoiceField(
        required=False,
        widget=forms.SelectMultiple(attrs={'class': 'form-select'})
    )
    country = forms.MultipleChoiceField(
        required=False,
        widget=forms.SelectMultiple(attrs={'class': 'form-select'})
    )

