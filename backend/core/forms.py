from django import forms
from .models import Coordinates


class CoordinatesForm(forms.ModelForm):
    file = forms.FileField()

    class Meta:
        model = Coordinates
        fields = ('latitude', 'longitude', 'file')
