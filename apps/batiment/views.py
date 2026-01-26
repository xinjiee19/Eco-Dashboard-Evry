from django.contrib.auth.models import User, Group
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import BuildingEnergyData
from .forms import BuildingEnergyForm


from decimal import Decimal

@login_required
def batiment_form_view(request):
    """Vue du formulaire de saisie bâtiments & énergies"""
    if request.method == "POST":
        form = BuildingEnergyForm(request.POST)
        if form.is_valid():
            user_group = request.user.groups.first()
            if not user_group and not request.user.is_superuser:
                messages.error(request, "Votre compte n'est associé à aucun groupe. Impossible d'enregistrer.")
                return redirect('batiment_list')

            data = form.save(commit=False)
            data.group = user_group
            
            # Application des facteurs d'émission standard (ADEME - France Continentale)
            # Électricité (Mix moyen) : ~0.052 kgCO2e/kWh
            # Gaz Naturel : ~0.227 kgCO2e/kWh
            # Réseau de chaleur (Moyenne) : ~0.150 kgCO2e/kWh
            # Climatisation (via Élec) : ~0.052 kgCO2e/kWh
            
            data.electricity_factor = Decimal("0.052")
            data.gas_factor = Decimal("0.227")
            data.heating_network_factor = Decimal("0.150")
            data.cooling_factor = Decimal("0.052")
            
            data.save()
            
            messages.success(
                request,
                f"✅ Données enregistrées ! Impact carbone : {float(data.total_co2_kg):.2f} kg CO₂e"
            )
            return redirect("batiment_list")
    else:
        form = BuildingEnergyForm()

    context = {"form": form}
    return render(request, "batiment/form.html", context)


@login_required
def batiment_list_view(request):
    """Vue de la liste des données bâtiments"""
    if request.user.is_staff or request.user.is_superuser:
        rows = BuildingEnergyData.objects.all().order_by("-year", "-created_at")
    else:
        # Les agents ne voient que les données de leur(s) groupe(s)
        rows = BuildingEnergyData.objects.filter(group__in=request.user.groups.all()).order_by("-year", "-created_at")
    
    total_co2 = sum(float(r.total_co2_kg or 0) for r in rows)

    context = {
        "rows": rows,
        "total_co2": total_co2,
        "count": rows.count(),
    }
    return render(request, "batiment/list.html", context)


@login_required
def batiment_form_update(request, pk):
    """Vue de modification d'une donnée bâtiment"""
    if request.user.is_staff or request.user.is_superuser:
        row = get_object_or_404(BuildingEnergyData, pk=pk)
    else:
        row = get_object_or_404(BuildingEnergyData, pk=pk, group__in=request.user.groups.all())
    
    if request.method == "POST":
        form = BuildingEnergyForm(request.POST, instance=row)
        if form.is_valid():
            data = form.save(commit=False)
            # Factors are already set on create, but we can re-apply or leave them.
            # Here we preserve them unless we want to update them to latest standard.
            # Simplified: just save.
            data.save()
            
            messages.success(
                request,
                f"✅ Données modifiées ! Impact carbone : {float(data.total_co2_kg):.2f} kg CO₂e"
            )
            return redirect("batiment_list")
    else:
        form = BuildingEnergyForm(instance=row)

    context = {"form": form}
    return render(request, "batiment/form.html", context)


@login_required
def batiment_detail_view(request, pk):
    """Vue détail"""
    if request.user.is_staff or request.user.is_superuser:
        row = get_object_or_404(BuildingEnergyData, pk=pk)
    else:
        row = get_object_or_404(BuildingEnergyData, pk=pk, group__in=request.user.groups.all())
    return render(request, "batiment/detail.html", {"row": row})


@login_required
def batiment_delete_view(request, pk):
    """Vue suppression"""
    if request.user.is_staff or request.user.is_superuser:
        row = get_object_or_404(BuildingEnergyData, pk=pk)
    else:
        row = get_object_or_404(BuildingEnergyData, pk=pk, group__in=request.user.groups.all())

    if request.method == "POST":
        row.delete()
        messages.success(request, "🗑️ Donnée supprimée avec succès.")
        return redirect("batiment_list")

    return render(request, "batiment/confirm_delete.html", {"row": row})
