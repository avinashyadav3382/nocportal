from django import forms
from .models import MCT_Data


class MountAbuUpdateForm(forms.ModelForm):
    class Meta:
        model = MCT_Data
        fields = [
            'total_counter',
            'fully_ops_counter',
            'restricted_ops_counter',
            'non_ops_counter',
            'misc_counter',
        ]
        widgets = {
            'total_counter': forms.NumberInput(attrs={'class': 'form-control'}),
            'fully_ops_counter': forms.NumberInput(attrs={'class': 'form-control'}),
            'restricted_ops_counter': forms.NumberInput(attrs={'class': 'form-control'}),
            'non_ops_counter': forms.NumberInput(attrs={'class': 'form-control'}),
            'misc_counter': forms.NumberInput(attrs={'class': 'form-control'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        total = cleaned_data.get('total_counter', 0)
        ops_sum = sum(cleaned_data.get(f, 0) for f in [
            'fully_ops_counter',
            'restricted_ops_counter',
            'non_ops_counter',
            'misc_counter'
        ])
        if ops_sum != total:
            raise forms.ValidationError(
                "Sum of counters must equal total units."
            )
        return cleaned_data


class KasauliUpdateForm(forms.ModelForm):
    class Meta:
        model = MCT_Data
        fields = [
            'total_counter',
            'fully_ops_counter',
            'restricted_ops_counter',
            'non_ops_counter',
            'misc_counter',
        ]
        widgets = {
            'total_counter': forms.NumberInput(attrs={'class': 'form-control'}),
            'fully_ops_counter': forms.NumberInput(attrs={'class': 'form-control'}),
            'restricted_ops_counter': forms.NumberInput(attrs={'class': 'form-control'}),
            'non_ops_counter': forms.NumberInput(attrs={'class': 'form-control'}),
            'misc_counter': forms.NumberInput(attrs={'class': 'form-control'}),
        }

    

    def clean(self):
        cleaned_data = super().clean()
        total = cleaned_data.get('total_counter', 0)
        ops_sum = sum(cleaned_data.get(f, 0) for f in [
            'fully_ops_counter',
            'restricted_ops_counter',
            'non_ops_counter',
            'misc_counter'
        ])
        if ops_sum != total:
            raise forms.ValidationError(
                "Sum of counters must equal total units."
            )
        return cleaned_data


class AdminMCTUpdateForm(forms.ModelForm):
    class Meta:
        model = MCT_Data
        fields = [
            'total_counter',
            'fully_ops_counter',
            'restricted_ops_counter',
            'non_ops_counter',
            'misc_counter',
        ]
        widgets = {
            'total_counter': forms.NumberInput(attrs={'class': 'form-control'}),
            'fully_ops_counter': forms.NumberInput(attrs={'class': 'form-control'}),
            'restricted_ops_counter': forms.NumberInput(attrs={'class': 'form-control'}),
            'non_ops_counter': forms.NumberInput(attrs={'class': 'form-control'}),
            'misc_counter': forms.NumberInput(attrs={'class': 'form-control'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        print("Cleaned data in form:", cleaned_data)  # Debugging statement
        total = cleaned_data.get('total_counter', 0)
        ops_sum = sum(cleaned_data.get(f, 0) for f in [
            'fully_ops_counter',
            'restricted_ops_counter',
            'non_ops_counter',
            'misc_counter'
        ])
        print(f"Total: {total}, Sum of ops: {ops_sum}")  # Debugging statement
        if ops_sum != total:
            raise forms.ValidationError(
                "Sum of counters must equal total units."
            )
        return cleaned_data