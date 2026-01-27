from django.contrib import admin
from .models import EquipementNumerique, NumeriqueEmissionFactor

@admin.register(NumeriqueEmissionFactor)
class NumeriqueEmissionFactorAdmin(admin.ModelAdmin):
    list_display = ('nom', 'type_equipement', 'fabrication_kg_co2', 'conso_kwh_an', 'source')
    list_editable = ('fabrication_kg_co2', 'conso_kwh_an')
    search_fields = ('nom', 'type_equipement')

@admin.register(EquipementNumerique)
class EquipementNumeriqueAdmin(admin.ModelAdmin):
    """
    Interface admin pour les équipements numériques.
    
    Note: Les facteurs d'émission (Fabrication + Consommation) sont définis
    dans le code (modèle EquipementNumerique) selon les données ADEME.
    Pour mettre à jour: modifiez FAB_CO2 et CONSO_MOYENNE dans models.py
    """
    list_display = ('nom', 'user', 'year', 'type_equipement', 'quantite', 'total_co2_kg')
    list_filter = ('year', 'type_equipement', 'user')
    search_fields = ('nom', 'marque_modele')
    readonly_fields = ('empreinte_fabrication', 'consommation_annuelle', 'total_co2_kg')
