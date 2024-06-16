from django import forms
from .models import Request, Offer

class RequestForm(forms.ModelForm):
    class Meta:
        model = Request
        fields = ['title', 'description', 'category', 'requestType', 'budget']

class OfferForm(forms.ModelForm):
    class Meta:
        model = Offer
        fields = ['bid', 'notes']
