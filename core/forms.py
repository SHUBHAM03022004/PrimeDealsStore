from django import forms
from core.models import *
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product  # ← This line is fine *only* if Product is a model, not a string
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'desc': forms.Textarea(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'product_available_count': forms.NumberInput(attrs={'class': 'form-control'}),
            'img': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

from django import forms
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget

class CheckoutForm(forms.Form):
    street_address = forms.CharField(
        widget=forms.TextInput(attrs={
            'placeholder': 'Street Address',
            'class': 'form-control'
        })
    )
    apartment_address = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 'Apartment Address',
            'class': 'form-control'
        })
    )
    country = CountryField(blank_label='(Select country)').formfield(
        widget=CountrySelectWidget(attrs={
            'class': 'custom-select d-block w-100'
        })
    )
    zip = forms.CharField(
        widget=forms.TextInput(attrs={
            'placeholder': 'Zip Code',
            'class': 'form-control'
        })
    )
