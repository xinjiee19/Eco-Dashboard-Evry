from django.db import models
from django.contrib.auth.models import User, Group
from django.utils import timezone


class NumeriqueEmissionFactor(models.Model):
    """Facteurs d'émission pour le numérique (stockés en base)"""
    type_equipement = models.CharField(max_length=50, unique=True, verbose_name="Code Type")
    nom = models.CharField(max_length=100, verbose_name="Libellé")
    
    # Valeurs
    fabrication_kg_co2 = models.DecimalField(max_digits=10, decimal_places=2, help_text="Empreinte fabrication (kg CO2e)")
    conso_kwh_an = models.DecimalField(max_digits=10, decimal_places=2, help_text="Conso électrique annuelle moyenne (kWh)")
    
    source = models.CharField(max_length=200, default="ADEME", blank=True)
    
    def __str__(self):
        return f"{self.nom} (Fab: {self.fabrication_kg_co2} kg, Conso: {self.conso_kwh_an} kWh)"

    class Meta:
        verbose_name = "Facteur Émission Numérique"
        verbose_name_plural = "Facteurs Émission Numérique"

class EquipementNumerique(models.Model):
    TYPE_CHOICES = [
        ('1. Hardware (Terminaux)', (
            ('LAPTOP', 'Ordinateur Portable'),
            ('DESKTOP_SCREEN', 'Ordinateur Fixe + Écran'),
            ('SMARTPHONE', 'Smartphone / Tablette'),
        )),
        ('2. Réseau', (
            ('BORNE_WIFI', 'Borne Wi-Fi'),
            ('SWITCH', 'Switch réseau'),
        )),
        ('3. Cloud & Services', (
            ('CLOUD_INSTANCE', 'Instance Cloud / Serveur virtuel'),
            ('CLOUD_STORAGE', 'Stockage Cloud 1 To'),
        )),
        ('4. Périphériques', (
            ('PRINTER', 'Imprimante Laser'),
            ('SCREEN_EXTRA', 'Écran supplémentaire'),
        )),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Groupe")
    year = models.IntegerField(default=timezone.now().year, verbose_name="Année")
    created_at = models.DateTimeField(auto_now_add=True)

    nom = models.CharField(max_length=100, verbose_name="Nom / Service")
    marque_modele = models.CharField(max_length=200, blank=True, null=True, verbose_name="Marque / Modèle")
    type_equipement = models.CharField(max_length=30, choices=TYPE_CHOICES, verbose_name="Type d'équipement")
    quantite = models.PositiveIntegerField(default=1, verbose_name="Quantité")
    duree_vie = models.PositiveIntegerField(default=5, verbose_name="Durée de vie (ans)")
    
    # Champs calculés
    empreinte_fabrication = models.FloatField(default=0, editable=False, help_text="Total fabrication (non amorti)")
    consommation_annuelle = models.FloatField(default=0, editable=False, help_text="kWh par an")
    
    total_co2_kg = models.FloatField(default=0, editable=False, help_text="Empreinte annuelle amortie + Usage")

    def save(self, *args, **kwargs):
        # Récupérer le facteur en base
        try:
            # On utilise le code stocké dans type_equipement pour trouver le facteur
            factor = NumeriqueEmissionFactor.objects.get(type_equipement=self.type_equipement)
            
            # Calcul Fabrication
            # Note: factor.valeur est Decimal, on convertit en float pour calculs
            self.empreinte_fabrication = float(factor.fabrication_kg_co2) * self.quantite
            
            # Calcul Consommation (Usage kWh)
            self.consommation_annuelle = float(factor.conso_kwh_an) * self.quantite
            
        except NumeriqueEmissionFactor.DoesNotExist:
            # Sécurité : si facteur non trouvé, on met 0 (ou on pourrait logguer une erreur)
            self.empreinte_fabrication = 0
            self.consommation_annuelle = 0

        # Calcul Total Annuel = (Fab / Durée) + (Conso * Facteur Elec)
        amortissement = self.empreinte_fabrication / max(self.duree_vie, 1)
        
        # Facteur Elec France (récupéré depuis le module Bâtiment ou défaut 0.052)
        try:
            from apps.batiment.models import BuildingEmissionFactor
            elec_factor_obj = BuildingEmissionFactor.objects.filter(type_energie='ELEC').first()
            if elec_factor_obj:
                FACTEUR_ELEC = float(elec_factor_obj.facteur)
            else:
                FACTEUR_ELEC = 0.052
        except Exception:
            FACTEUR_ELEC = 0.052

        usage_co2 = self.consommation_annuelle * FACTEUR_ELEC
        
        # Pour les services Cloud, on considère souvent que l'abonnement annuel inclut tout
        # Ici on simplifie en traitant comme du matériel amorti sur durée_vie
        # Si durée_vie = 1 an, alors amortissement = fabrication totale (abonnement annuel)

        self.total_co2_kg = amortissement + usage_co2
        
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.nom} - {self.get_type_equipement_display()}"
    
    class Meta:
        verbose_name = "Équipement numérique"
        verbose_name_plural = "Données numérique"
        ordering = ['-year', '-created_at']
