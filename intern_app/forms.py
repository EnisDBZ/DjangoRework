# forms.py
from django import forms
from .models import Billing

class BillingForm(forms.ModelForm):
    card_exp = forms.CharField(
        label="Expiration Date (MM/YY)",
        widget=forms.TextInput(attrs={
            'placeholder': 'MM/YY',
            'maxlength': '5',
            'class': 'form-control expiry-input',
            'autocomplete': 'cc-exp'
        }),
        help_text="Enter in MM/YY format"
    )
    
    class Meta:
        model = Billing
        fields = '__all__'  # or specify your fields
    
    def clean_card_exp(self):
        data = self.cleaned_data['card_exp']
        try:
            month, year = map(int, data.split('/'))
            if month < 1 or month > 12:
                raise forms.ValidationError("Invalid month (must be 1-12)")
            if year < 23 or year > 40:  # Adjust year range as needed
                raise forms.ValidationError("Invalid year")
            return data
        except (ValueError, AttributeError):
            raise forms.ValidationError("Please use MM/YY format")