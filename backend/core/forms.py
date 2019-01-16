from django import forms
from .models import Coordinates


class OrderForm(forms.ModelForm):
    file = forms.FileField()

    class Meta:
        model = Coordinates
        fields = ('title', 'description', 'latitude', 'longitude', 'file')
