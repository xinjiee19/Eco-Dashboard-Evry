from django.contrib import admin
from .models import EquipementNumerique

@admin.register(EquipementNumerique)
class EquipementNumeriqueAdmin(admin.ModelAdmin):
    """
    Interface admin pour les équipements numériques.
    
    Note: Les facteurs d'émission (Fabrication + Consommation) sont définis
    dans le code (modèle EquipementNumerique) selon les données ADEME.
    Pour mettre à jour: modifiez FAB_CO2 et CONSO_MOYENNE dans models.py
    """
    list_display = ('nom', 'group', 'year', 'type_equipement', 'quantite', 'total_co2_kg')
    list_filter = ('year', 'type_equipement', 'group')
    search_fields = ('nom', 'marque_modele', 'group__name')
    readonly_fields = ('empreinte_fabrication', 'consommation_annuelle', 'total_co2_kg', 'created_at')
