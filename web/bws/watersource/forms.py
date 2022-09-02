from django import forms
from .models import WaterSource


class WaterSourceCreateForm(forms.ModelForm):
    class Meta:
        model = WaterSource
        fields = ['identification', 'description', 'latitude', 'longitude']
