from django import forms
from .models import MessageSensibilisation


class MessageSensibilisationForm(forms.ModelForm):
    class Meta:
        model = MessageSensibilisation
        fields = ['titre', 'contenu', 'type_contenu', 'type_message']
        labels = {
            'titre': 'Titre du message',
            'contenu': 'Contenu',
            'type_contenu': 'Type de contenu',
            'type_message': 'Catégorie',
        }
        help_texts = {
            'type_contenu': '📌 Message/Conseil = Affichage standard | Zoom = Mise en avant spéciale avec encadré orange',
            'type_message': '🏷️ Info = Neutre | Conseil = Pratique | Alerte = Important | Objectif = Cible à atteindre',
        }
        widgets = {
            'titre': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Ex: Semaine de la mobilité douce'
            }),
            'contenu': forms.Textarea(attrs={
                'class': 'form-input',
                'placeholder': 'Décrivez votre message ou action en détail...',
                'rows': 5
            }),
            'type_contenu': forms.Select(attrs={
                'class': 'form-select',
            }),
            'type_message': forms.Select(attrs={
                'class': 'form-select',
            }),
        }
