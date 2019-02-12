from django import forms
from .models import Coordinates
from .utils import check_uploaded_file

class OrderForm(forms.ModelForm):
    file = forms.FileField()

    class Meta:
        model = Coordinates
        fields = ('title', 'description', 'latitude', 'longitude', 'file')

    def clean_file(self):
        uploaded_file = self.cleaned_data['file']
        if not check_uploaded_file(uploaded_file):
            raise forms.ValidationError("Insert a .zip file with the .shp file.")

        return uploaded_file

    def clean_latitude(self):
        cleaned_data = self.cleaned_data
        latitude = cleaned_data['latitude']
        if latitude < (-90) or latitude > 90:
            raise forms.ValidationError("The latitude must be between -90 and 90.")

        return latitude

    def clean_longitude(self):
        cleaned_data = self.cleaned_data
        longitude = cleaned_data['longitude']
        if longitude < (-180) or longitude > 180:
            raise forms.ValidationError("The longitude must be between -180 and 180.")

        return longitude
