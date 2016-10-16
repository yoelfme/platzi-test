from django import forms

class PaymentForm(forms.Form):
    name = forms.CharField()
    email = forms.EmailField()
    stripeToken = forms.CharField()
