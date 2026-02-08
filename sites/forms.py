# sites/forms.py
from django import forms
from .models import MCT_SatcomData

class MCTSatcomEditForm(forms.ModelForm):
    class Meta:
        model = MCT_SatcomData
        fields = ['status']
        widgets = {
            'status': forms.Select(attrs={'class': 'form-select form-select-sm'}),
        }

class MCTSatcomAdminAddForm(forms.ModelForm):
    class Meta:
        model = MCT_SatcomData
        fields = ['name', 'data_type', 'status']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter unique name'}),
            'data_type': forms.Select(attrs={'class': 'form-select'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
        }

    def clean_name(self):
        name = self.cleaned_data['name']
        if MCT_SatcomData.objects.filter(name__iexact=name).exists():
            raise forms.ValidationError("This name already exists.")
        return name

class MCTAddForm(forms.ModelForm):
    class Meta:
        model = MCT_SatcomData
        fields = ['name', 'status']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter unique name'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
        }

    def clean_name(self):
        name = self.cleaned_data['name']
        if MCT_SatcomData.objects.filter(name__iexact=name).exists():
            raise forms.ValidationError("This name already exists.")
        return name

class SatcomAddForm(forms.ModelForm):
    class Meta:
        model = MCT_SatcomData
        fields = ['name', 'status']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter unique name'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
        }

    def clean_name(self):
        name = self.cleaned_data['name']
        if MCT_SatcomData.objects.filter(name__iexact=name).exists():
            raise forms.ValidationError("This name already exists.")
        return name