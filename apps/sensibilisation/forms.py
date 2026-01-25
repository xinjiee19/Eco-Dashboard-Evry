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
                'placeholder': 'Ex: Semaine de la mobilité douce',
                'style': 'width: 100%; padding: 12px 16px; border: 2px solid #e0e0e0; border-radius: 8px; font-size: 1rem; transition: all 0.3s ease;'
            }),
            'contenu': forms.Textarea(attrs={
                'class': 'form-input',
                'placeholder': 'Décrivez votre message ou action en détail...',
                'rows': 5,
                'style': 'width: 100%; padding: 12px 16px; border: 2px solid #e0e0e0; border-radius: 8px; font-size: 1rem; resize: vertical; transition: all 0.3s ease;'
            }),
            'type_contenu': forms.Select(attrs={
                'class': 'form-select',
                'style': 'width: 100%; padding: 12px 16px; border: 2px solid #e0e0e0; border-radius: 8px; font-size: 1rem; background: white; cursor: pointer; transition: all 0.3s ease;'
            }),
            'type_message': forms.Select(attrs={
                'class': 'form-select',
                'style': 'width: 100%; padding: 12px 16px; border: 2px solid #e0e0e0; border-radius: 8px; font-size: 1rem; background: white; cursor: pointer; transition: all 0.3s ease;'
            }),
        }
