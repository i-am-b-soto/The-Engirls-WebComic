from django import forms 
from .models import Subscription
#from dal import autocomplete


class SubscriptionForm(forms.ModelForm):
    class Meta:
        model = Subscription
        fields = ('email',)
