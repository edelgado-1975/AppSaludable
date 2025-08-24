
from django import forms
from .models import Profile

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['level'] 
        labels = {
            'level': 'Tu Nivel de Condición Física Actual'
        }
        widgets = {
            'level': forms.Select(attrs={'class': 'form-select'})
        }