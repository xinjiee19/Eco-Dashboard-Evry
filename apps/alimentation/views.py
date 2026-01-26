from django.contrib.auth.models import User, Group
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db import models
from django.contrib import messages

from .models import FoodEntry, FoodEmissionFactor
from .forms import FoodEntryForm


@login_required
def foodentry_create(request):
    factors = {f.code: f.kg_co2_per_meal for f in FoodEmissionFactor.objects.all()}
    if request.method == "POST":
        form = FoodEntryForm(request.POST) # Removed user from form
        if form.is_valid():
            user_group = request.user.groups.first()
            if not user_group and not request.user.is_superuser:
                messages.error(request, "Votre compte n'est associé à aucun groupe. Impossible d'enregistrer.")
                return redirect('food_list')

            entry = form.save(commit=False)
            entry.group = user_group
            entry.save()
            return redirect("food_list")
    else:
        form = FoodEntryForm() # Removed user from form

    return render(
        request,
        "alimentation/foodentry_form.html",
        {"form": form, "factors": factors},
    )

@login_required
def foodentry_list(request):
    if request.user.is_staff or request.user.is_superuser:
        entries = FoodEntry.objects.all().order_by("-year", "-created_at")
    else:
        # Les agents ne voient que les données de leur(s) groupe(s)
        entries = FoodEntry.objects.filter(group__in=request.user.groups.all()).order_by("-year", "-created_at")

    total_co2 = sum(e.total_co2_kg or 0 for e in entries)
    count = entries.count()

    context = {
        "entries": entries,
        "total_co2": total_co2,
        "count": count,
    }
    return render(request, "alimentation/list.html", context)


@login_required
def foodentry_update(request, pk):
    if request.user.is_staff or request.user.is_superuser:
        entry = get_object_or_404(FoodEntry, pk=pk)
    else:
        entry = get_object_or_404(FoodEntry, pk=pk, group__in=request.user.groups.all())
    factors = {f.code: f.kg_co2_per_meal for f in FoodEmissionFactor.objects.all()}

    if request.method == "POST":
        form = FoodEntryForm(request.POST, instance=entry) # Removed user from form
        if form.is_valid():
            form.save()
            return redirect("food_list")
    else:
        form = FoodEntryForm(instance=entry) # Removed user from form

    return render(
        request,
        "alimentation/foodentry_form.html",
        {"form": form, "factors": factors},
    )


@login_required
def foodentry_detail(request, pk):
    if request.user.is_staff or request.user.is_superuser:
        entry = get_object_or_404(FoodEntry, pk=pk)
    else:
        entry = get_object_or_404(FoodEntry, pk=pk, group__in=request.user.groups.all())
    return render(request, "alimentation/foodentry_detail.html", {"entry": entry})


@login_required
def foodentry_delete(request, pk):
    if request.user.is_staff or request.user.is_superuser:
        entry = get_object_or_404(FoodEntry, pk=pk)
    else:
        entry = get_object_or_404(FoodEntry, pk=pk, group__in=request.user.groups.all())
    if request.method == "POST":
        entry.delete()
        return redirect("food_list")
    return render(request, "alimentation/confirm_delete.html", {"entry": entry})
