from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import PurchaseData, PurchaseEmissionFactor
from .forms import PurchaseDataForm


@login_required
def purchase_form(request):
    """Vue du formulaire de saisie d'achat."""
    if request.method == 'POST':
        form = PurchaseDataForm(request.POST)
        if form.is_valid():
            purchase = form.save(commit=False)
            purchase.user = request.user
            user_group = request.user.groups.first()
            if user_group:
                purchase.group = user_group
            purchase.save()
            
            messages.success(
                request,
                f'✅ Achat enregistré ! Impact carbone : {purchase.total_co2_kg:.2f} kg CO₂e'
            )
            return redirect('purchase_list')
    else:
        form = PurchaseDataForm(initial={'year': 2026})
    
    # Récupérer les facteurs d'émission depuis la base de données
    emission_factors_qs = PurchaseEmissionFactor.objects.all().order_by('category_label')
    emission_factors = {
        ef.category_code: float(ef.factor_kg_co2_per_keur) 
        for ef in emission_factors_qs
    }
    
    return render(request, 'purchases/purchase_form.html', {
        'form': form,
        'emission_factors': emission_factors,
        'emission_factors_list': emission_factors_qs
    })



@login_required
def purchase_list(request):
    """Vue listant toutes les données d'achats de l'utilisateur."""
    if request.user.is_staff or request.user.is_superuser:
        purchases = PurchaseData.objects.all()
    else:
        purchases = PurchaseData.objects.filter(group__in=request.user.groups.all())
    
    # Statistiques
    total_co2 = sum(p.total_co2_kg for p in purchases)
    total_amount = sum(p.amount_euros for p in purchases)
    
    return render(request, 'purchases/purchase_list.html', {
        'purchases': purchases,
        'total_co2': total_co2,
        'total_amount': total_amount,
        'purchase_count': purchases.count()
    })


@login_required
def purchase_detail(request, pk):
    """Vue détaillée d'un achat."""
    if request.user.is_staff or request.user.is_superuser:
        purchase = get_object_or_404(PurchaseData, pk=pk)
    else:
        purchase = get_object_or_404(PurchaseData, pk=pk, group__in=request.user.groups.all())
    
    return render(request, 'purchases/purchase_detail.html', {
        'purchase': purchase
    })


@login_required
def purchase_update(request, pk):
    """Modification d'un achat."""
    if request.user.is_staff or request.user.is_superuser:
        purchase = get_object_or_404(PurchaseData, pk=pk)
    else:
        purchase = get_object_or_404(PurchaseData, pk=pk, group__in=request.user.groups.all())
    
    if request.method == 'POST':
        form = PurchaseDataForm(request.POST, instance=purchase)
        if form.is_valid():
            p = form.save(commit=False)
            p.user = request.user
            p.save()
            messages.success(request, '✅ Achat modifié avec succès !')
            return redirect('purchase_list')
    else:
        form = PurchaseDataForm(instance=purchase)
    
    # Récupérer les facteurs d'émission
    emission_factors_qs = PurchaseEmissionFactor.objects.all().order_by('category_label')
    emission_factors = {
        ef.category_code: float(ef.factor_kg_co2_per_keur) 
        for ef in emission_factors_qs
    }
    
    return render(request, 'purchases/purchase_form.html', {
        'form': form,
        'emission_factors': emission_factors,
        'emission_factors_list': emission_factors_qs
    })

@login_required
def purchase_delete(request, pk):
    """Suppression d'un achat."""
    if request.user.is_staff or request.user.is_superuser:
        purchase = get_object_or_404(PurchaseData, pk=pk)
    else:
        purchase = get_object_or_404(PurchaseData, pk=pk, group__in=request.user.groups.all())
    
    if request.method == 'POST':
        purchase.delete()
        messages.success(request, '🗑️ Achat supprimé avec succès')
        return redirect('purchase_list')
    
    return render(request, 'purchases/purchase_confirm_delete.html', {
        'purchase': purchase
    })
