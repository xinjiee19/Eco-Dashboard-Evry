from django import forms
from .models import EquipementNumerique

class NumeriqueForm(forms.ModelForm):
    class Meta:
        model = EquipementNumerique
        fields = ['year', 'nom', 'marque_modele', 'type_equipement', 'quantite', 'duree_vie']
        widgets = {
            'year': forms.NumberInput(attrs={'class': 'form-input', 'placeholder': 'Ex: 2026'}),
            'nom': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Ex: Service IT - Parc PC'}),
            'marque_modele': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Ex: Dell Latitude 5420'}),
            'type_equipement': forms.Select(attrs={'class': 'form-input'}),
            'quantite': forms.NumberInput(attrs={'class': 'form-input', 'min': 1}),
            'duree_vie': forms.NumberInput(attrs={'class': 'form-input', 'min': 1, 'placeholder': 'Années'}),
        }
