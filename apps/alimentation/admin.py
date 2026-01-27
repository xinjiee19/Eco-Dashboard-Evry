# Register your models here.
from django.contrib import admin
from .models import FoodEmissionFactor, FoodEntry

@admin.register(FoodEmissionFactor)
class FoodEmissionFactorAdmin(admin.ModelAdmin):
    list_display = ("code", "label", "kg_co2_per_meal", "source")
    list_editable = ("kg_co2_per_meal",)
    search_fields = ('code', 'label')
    ordering = ('label',)

@admin.register(FoodEntry)
class FoodEntryAdmin(admin.ModelAdmin):
    list_display = ('year', 'service', 'total_co2_kg', 'user', 'created_at')
    list_filter = ('year', 'user')
    search_fields = ('service', 'user__username')
    readonly_fields = ('total_co2_kg', 'created_at')