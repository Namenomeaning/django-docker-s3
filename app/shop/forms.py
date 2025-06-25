from django import forms
from .models import Order


class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'email', 'address', 'postal_code', 'city']
        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'input',
                'placeholder': 'First Name'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'input',
                'placeholder': 'Last Name'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'input',
                'placeholder': 'Email Address'
            }),
            'address': forms.TextInput(attrs={
                'class': 'input',
                'placeholder': 'Address'
            }),
            'postal_code': forms.TextInput(attrs={
                'class': 'input',
                'placeholder': 'Postal Code'
            }),
            'city': forms.TextInput(attrs={
                'class': 'input',
                'placeholder': 'City'
            }),
        }
