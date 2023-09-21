# invoicing/forms.py
from django import forms
from .models import Client

class LoginForm(forms.Form):
    username = forms.CharField(max_length=150, label='Username')
    password = forms.CharField(widget=forms.PasswordInput, label='Password')


class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['clientName', 'clientLogo', 'addressLine1', 'province', 'postalCode', 'phoneNumber', 'emailAddress', 'taxNumber']
        widgets = {
            'clientName': forms.TextInput(attrs={'required': 'required'}),
            'province': forms.Select(attrs={'required': 'required'}),
            'phoneNumber': forms.TextInput(attrs={'required': 'required'}),
            'emailAddress': forms.EmailInput(attrs={'required': 'required'}),
        }