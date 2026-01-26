# Register your models here.
from django.contrib import admin
from .models import FoodEmissionFactor, FoodEntry

@admin.register(FoodEmissionFactor)
class FoodEmissionFactorAdmin(admin.ModelAdmin):
    list_display = ("code", "label", "kg_co2_per_meal")
    search_fields = ('code', 'label')
    ordering = ('label',)

@admin.register(FoodEntry)
class FoodEntryAdmin(admin.ModelAdmin):
    list_display = ('year', 'service', 'total_co2_kg', 'group', 'created_at')
    list_filter = ('year', 'group')
    search_fields = ('service', 'group__name')
    readonly_fields = ('total_co2_kg', 'created_at', 'updated_at')