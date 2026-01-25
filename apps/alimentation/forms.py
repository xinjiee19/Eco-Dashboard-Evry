# apps/alimentation/forms.py
from django import forms
from .models import FoodEntry

class FoodEntryForm(forms.ModelForm):
    class Meta:
        model = FoodEntry
        fields = [
            "year",
            "service",
            "beef_meals",
            "pork_meals",
            "poultry_fish_meals",
            "vegetarian_meals",
            "picnic_no_meat_meals",
            "picnic_meat_meals",
        ]
        widgets = {
            "year": forms.NumberInput(attrs={
                "class": "form-input",
                "placeholder": "2026",
                "min": "2020",
                "max": "2040"
            }),
            "service": forms.TextInput(attrs={"class": "form-input"}),
            "beef_meals": forms.NumberInput(attrs={"class": "form-input", "placeholder": "0"}),
            "pork_meals": forms.NumberInput(attrs={"class": "form-input", "placeholder": "0"}),
            "poultry_fish_meals": forms.NumberInput(attrs={"class": "form-input", "placeholder": "0"}),
            "vegetarian_meals": forms.NumberInput(attrs={"class": "form-input", "placeholder": "0"}),
            "picnic_no_meat_meals": forms.NumberInput(attrs={"class": "form-input", "placeholder": "0"}),
            "picnic_meat_meals": forms.NumberInput(attrs={"class": "form-input", "placeholder": "0"}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)
        
        # Set default year to current year if not bound
        if not self.is_bound and not self.instance.pk:
            import datetime
            self.initial['year'] = datetime.datetime.now().year

        # Exemple : pré-remplir le service selon le profil
        if user and not self.instance.pk:
            self.fields["service"].initial = getattr(user, "service_name", "")
