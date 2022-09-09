from django import forms
from .models import Shopping, Register

class ShoppingForm(forms.ModelForm):
    class Meta:
        model = Shopping
        # fields = '__all__'
        fields = ['customer_name','nft_name', 'nft_price']

class RegisterForm(forms.ModelForm):
    class Meta:
        model = Register
        fields = ['nft_name', 'Token_uri', 'Token_id','nft_price']