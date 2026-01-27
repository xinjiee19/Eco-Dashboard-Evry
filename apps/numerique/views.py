from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum
from .models import EquipementNumerique, NumeriqueEmissionFactor
from .forms import NumeriqueForm
import json

@login_required
def numerique_dashboard(request):
    """Vue principale : formulaire + inventaire + graphiques"""
    if request.method == 'POST':
        form = NumeriqueForm(request.POST)
        if form.is_valid():
            numerique = form.save(commit=False)
            numerique.user = request.user
            user_group = request.user.groups.first()
            if user_group:
                numerique.group = user_group
            numerique.save()
            messages.success(request, '✅ Équipement ajouté avec succès !')
            return redirect('numerique_dashboard')
    else:
        from django.utils import timezone
        form = NumeriqueForm(initial={'year': timezone.now().year})
    
    # Récupérer tous les équipements de l'utilisateur
    if request.user.is_staff or request.user.is_superuser:
        equipements = EquipementNumerique.objects.all().order_by('-created_at')
    else:
        equipements = EquipementNumerique.objects.filter(group__in=request.user.groups.all()).order_by('-created_at')
    
    # Calcul des totaux
    total_carbone = equipements.aggregate(Sum('empreinte_fabrication'))['empreinte_fabrication__sum'] or 0
    total_conso = equipements.aggregate(Sum('consommation_annuelle'))['consommation_annuelle__sum'] or 0
    
    # Données pour les graphiques (répartition par type)
    repartition = equipements.values('type_equipement').annotate(
        total_fab=Sum('empreinte_fabrication'),
        total_conso=Sum('consommation_annuelle')
    ).order_by('-total_fab')
    
    # Mapper les codes vers les noms lisibles
    type_display_map = {}
    for group_name, choices in EquipementNumerique.TYPE_CHOICES:
        for code, label in choices:
            # Simplifier le label (retirer les valeurs entre parenthèses)
            clean_label = label.split('(')[0].strip()
            type_display_map[code] = clean_label
    
    chart_labels = []
    chart_fab_data = []
    chart_conso_data = []
    
    for item in repartition:
        label = type_display_map.get(item['type_equipement'], item['type_equipement'])
        chart_labels.append(label)
        chart_fab_data.append(float(item['total_fab'] or 0))
        chart_conso_data.append(float(item['total_conso'] or 0))
    
    return render(request, 'numerique/numerique_dashboard.html', {
        'form': form,
        'equipements': equipements,
        'total_carbone': total_carbone,
        'total_conso': total_conso,
        'chart_labels': json.dumps(chart_labels),
        'chart_fab_data': json.dumps(chart_fab_data),
        'chart_fab_data': json.dumps(chart_fab_data),
        'chart_conso_data': json.dumps(chart_conso_data),
        'emission_factors': NumeriqueEmissionFactor.objects.all(),
    })

@login_required
def numerique_list(request):
    """Liste des équipements numériques (ancienne vue, gardée pour compatibilité)"""
    from django.db.models import Sum
    if request.user.is_staff or request.user.is_superuser:
        equipements = EquipementNumerique.objects.all().order_by('-year', 'nom')
    else:
        equipements = EquipementNumerique.objects.filter(group__in=request.user.groups.all()).order_by('-year', 'nom')
    total_co2 = equipements.aggregate(Sum('total_co2_kg'))['total_co2_kg__sum'] or 0
    
    return render(request, 'numerique/numerique_list.html', {
        'equipements': equipements,
        'total_co2': total_co2
    })

@login_required
def numerique_create(request):
    """Ajouter un équipement (redirige vers dashboard)"""
    return redirect('numerique_dashboard')

@login_required
def numerique_update(request, pk):
    """Modifier un équipement"""
    if request.user.is_staff or request.user.is_superuser:
        numerique = get_object_or_404(EquipementNumerique, pk=pk)
    else:
        numerique = get_object_or_404(EquipementNumerique, pk=pk, group__in=request.user.groups.all())
    
    if request.method == 'POST':
        form = NumeriqueForm(request.POST, instance=numerique)
        if form.is_valid():
            form.save()
            messages.success(request, '✅ Équipement mis à jour !')
            return redirect('numerique_dashboard')
    else:
        form = NumeriqueForm(instance=numerique)
    
    return render(request, 'numerique/numerique_form.html', {
        'form': form,
        'title': 'Modifier Équipement',
        'emission_factors': NumeriqueEmissionFactor.objects.all(),
    })

@login_required
def numerique_detail(request, pk):
    """Détail d'un équipement"""
    if request.user.is_staff or request.user.is_superuser:
        numerique = get_object_or_404(EquipementNumerique, pk=pk)
    else:
        numerique = get_object_or_404(EquipementNumerique, pk=pk, group__in=request.user.groups.all())
    
    return render(request, 'numerique/detail.html', {
        'object': numerique
    })

@login_required
def numerique_delete(request, pk):
    """Supprimer un équipement"""
    if request.user.is_staff or request.user.is_superuser:
        numerique = get_object_or_404(EquipementNumerique, pk=pk)
    else:
        numerique = get_object_or_404(EquipementNumerique, pk=pk, group__in=request.user.groups.all())
    
    if request.method == 'POST':
        numerique.delete()
        messages.success(request, '🗑️ Équipement supprimé.')
        return redirect('numerique_dashboard')
        
    return render(request, 'numerique/confirm_delete.html', {
        'object': numerique
    })
