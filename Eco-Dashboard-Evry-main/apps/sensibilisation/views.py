from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum
from datetime import datetime

from apps.vehicles.models import VehicleData
from apps.purchases.models import PurchaseData
from apps.alimentation.models import FoodEntry
from apps.batiment.models import BuildingEnergyData
from apps.numerique.models import EquipementNumerique
from .models import MessageSensibilisation
from .services import SensibilisationService
from .forms import MessageSensibilisationForm


def get_module_totals(year, user=None):
    """Calcule les totaux CO2 par module pour une année donnée"""
    vehicles = float(VehicleData.objects.filter(year=year).aggregate(total=Sum('total_co2_kg'))['total'] or 0)
    purchases = float(PurchaseData.objects.filter(year=year).aggregate(total=Sum('total_co2_kg'))['total'] or 0)
    alimentation = float(FoodEntry.objects.filter(year=year).aggregate(total=Sum('total_co2_kg'))['total'] or 0)
    batiment = float(BuildingEnergyData.objects.filter(year=year).aggregate(total=Sum('total_co2_kg'))['total'] or 0)
    numerique = float(EquipementNumerique.objects.filter(year=year).aggregate(total=Sum('total_co2_kg'))['total'] or 0)
    
    return {
        'vehicles': vehicles,
        'purchases': purchases,
        'alimentation': alimentation,
        'batiment': batiment,
        'numerique': numerique,
        'total': vehicles + purchases + alimentation + batiment + numerique
    }


def calculate_variation(current, previous):
    """Calcule la variation en pourcentage"""
    if previous == 0:
        return None
    return round(((current - previous) / previous) * 100, 1)


@login_required
def sensibilisation_page(request):
    """Page dédiée Sensibilisation avec équivalences, conseils et comparatif"""
    current_year = datetime.now().year
    previous_year = current_year - 1

    # Handle form submission (admin only)
    form = None
    if request.user.is_staff:
        if request.method == 'POST':
            form = MessageSensibilisationForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, '✅ Message créé avec succès !')
                return redirect('sensibilisation_page')
        else:
            form = MessageSensibilisationForm()

    # Totaux année en cours
    stats_current = get_module_totals(current_year, request.user)
    # Totaux année précédente
    stats_previous = get_module_totals(previous_year, request.user)

    # Calculer les variations
    comparaison = []
    modules_labels = {
        'vehicles': ('Véhicules', '🚗'),
        'batiment': ('Bâtiments', '🏢'),
        'purchases': ('Achats', '🛒'),
        'alimentation': ('Alimentation', '🍽️'),
        'numerique': ('Numérique', '💻'),
    }
    
    for key, (label, icon) in modules_labels.items():
        current = stats_current.get(key, 0)
        previous = stats_previous.get(key, 0)
        variation = calculate_variation(current, previous)
        comparaison.append({
            'label': label,
            'icon': icon,
            'current': current,
            'previous': previous,
            'variation': variation,
            'positive': variation is not None and variation < 0  # Moins d'émissions = positif
        })

    # Messages et Zoom Actions (séparés)
    messages_admin = MessageSensibilisation.objects.filter(actif=True, type_contenu='message')
    zoom_actions = MessageSensibilisation.objects.filter(actif=True, type_contenu='zoom')

    # Conseils automatiques
    conseils = SensibilisationService.get_conseils_automatiques(stats_current)
    equivalences = SensibilisationService.get_equivalences(stats_current['total'])

    context = {
        'total_co2': stats_current['total'],
        'total_previous': stats_previous['total'],
        'variation_total': calculate_variation(stats_current['total'], stats_previous['total']),
        'current_year': current_year,
        'previous_year': previous_year,
        'comparaison': comparaison,
        'messages_admin': messages_admin,
        'zoom_actions': zoom_actions,
        'equivalences': equivalences,
        'conseils': conseils,
        'form': form,
    }
    return render(request, 'sensibilisation/sensibilisation_page.html', context)

