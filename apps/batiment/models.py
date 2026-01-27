from django.conf import settings
from django.db import models
from django.contrib.auth.models import Group


class BuildingEmissionFactor(models.Model):
    """Facteurs d'émission pour les énergies des bâtiments"""
    TYPE_CHOICES = [
        ('ELEC', 'Électricité'),
        ('GAZ', 'Gaz Naturel'),
        ('HEAT', 'Réseau de chaleur'),
        ('COOL', 'Climatisation'),
    ]
    type_energie = models.CharField(max_length=10, choices=TYPE_CHOICES, unique=True, verbose_name="Type d'énergie")
    facteur = models.DecimalField(max_digits=10, decimal_places=6, help_text="kgCO2e/kWh")
    unit = models.CharField(max_length=20, default="kgCO2e/kWh")
    source = models.CharField(max_length=200, default="ADEME", blank=True)

    def __str__(self):
        return f"{self.get_type_energie_display()}: {self.facteur}"

    class Meta:
        verbose_name = "Facteur Émission Bâtiment"
        verbose_name_plural = "Facteurs Émission Bâtiment"

class BuildingEnergyData(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Groupe")
    year = models.PositiveIntegerField(verbose_name="Année")
    site_name = models.CharField(max_length=200, default="Site inconnu", verbose_name="Nom du site")
    surface_area = models.DecimalField(max_digits=10, decimal_places=2, default=0, help_text="m²", verbose_name="Surface (m²)")
    construction_year = models.PositiveIntegerField(null=True, blank=True, verbose_name="Année de construction")
    
    # Energy Consumptions
    electricity_kwh = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name="Électricité (kWh)")
    gas_kwh = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name="Gaz Naturel (kWh)")
    heating_network_kwh = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name="Réseau de chaleur (kWh)")
    cooling_kwh = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name="Climatisation (kWh)")
    photovoltaic_production_kwh = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name="Production PV (kWh)")

    # Factors (kgCO2e / kWh) stored for historical record
    electricity_factor = models.DecimalField(max_digits=10, decimal_places=6, default=0)
    gas_factor = models.DecimalField(max_digits=10, decimal_places=6, default=0)
    heating_network_factor = models.DecimalField(max_digits=10, decimal_places=6, default=0)
    cooling_factor = models.DecimalField(max_digits=10, decimal_places=6, default=0)

    total_co2_kg = models.DecimalField(max_digits=14, decimal_places=2, default=0)

    notes = models.TextField(blank=True, verbose_name="Notes")
    created_at = models.DateTimeField(auto_now_add=True)

    def compute_total(self):
        # Calculation: sum(consumption * factor)
        # Note: Photovoltaic production is tracked but does not subtract from footprint in this simplified mode
        total = (self.electricity_kwh * self.electricity_factor) + \
                (self.gas_kwh * self.gas_factor) + \
                (self.heating_network_kwh * self.heating_network_factor) + \
                (self.cooling_kwh * self.cooling_factor)
        return total

    def save(self, *args, **kwargs):
        # Récupérer les facteurs en base s'ils sont à 0 (nouveau ou update)
        # On essaie de les remplir dynamiquement
        try:
            # BuildingEmissionFactor est défini dans ce fichier, on peut l'utiliser directement
            factors = {f.type_energie: f.facteur for f in BuildingEmissionFactor.objects.all()}
            
            # Si le facteur n'est pas déjà fixé (ou si on veut le mettre à jour ? 
            # Pour l'instant, on met à jour si c'est 0, pour garder l'historique sur les vieux enregistrements)
            if self.electricity_factor == 0:
                self.electricity_factor = factors.get('ELEC', 0.052) # Fallback hardcoded if missing
            
            if self.gas_factor == 0:
                self.gas_factor = factors.get('GAZ', 0.227)
                
            if self.heating_network_factor == 0:
                self.heating_network_factor = factors.get('HEAT', 0.150)
                
            if self.cooling_factor == 0:
                self.cooling_factor = factors.get('COOL', 0.052)
                
        except Exception:
            # Fallback total si table pas encore prête (migration)
            pass

        self.total_co2_kg = self.compute_total()
        super().save(*args, **kwargs)
    
    class Meta:
        verbose_name = "Donnée bâtiment"
        verbose_name_plural = "Données bâtiment"
        ordering = ['-year', '-created_at']

    def __str__(self):
        return f"{self.year} - {self.site_name} ({self.total_co2_kg} kgCO2e)"
