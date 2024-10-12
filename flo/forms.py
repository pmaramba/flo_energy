from django import forms
from .models import Company

class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = '__all__'
        labels = {
            'company_name': 'Company Name',
            'contact_person': 'Contact Person',
            'email': 'Email',
            'phone': 'Phone',
            'address': 'Address',
            'fuel_type': 'Fuel Type',
            'amount_paid': 'Amount Paid',
            'fuel_price': 'Fuel Price',
            'fuel_allocation': 'Fuel Allocation',
            'init_fuel': 'Init Fuel',
        }

        # Dropdown options for fuel_type
        OPTIONS = [
            ('Unleaded Petrol', 'Unleaded Petrol'),
            ('Regular Diesel', 'Regular Diesel'),
            ('Diesel 50', 'Diesel 50'),
            ('Blended Petrol', 'Blended Petrol'),
        ]

        widgets = {
            'company_name': forms.TextInput(attrs={'class': 'form-control'}),
            'contact_person': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control'}),
            'fuel_type': forms.Select(choices=OPTIONS, attrs={'class': 'form-control'}),  # Dropdown for fuel_type
            'amount_paid': forms.NumberInput(attrs={'class': 'form-control'}),
            'fuel_price': forms.NumberInput(attrs={'class': 'form-control'}),
            'init_fuel': forms.NumberInput(attrs={'class': 'form-control'}),
            'fuel_allocation': forms.NumberInput(attrs={'class': 'form-control'}),
        }
