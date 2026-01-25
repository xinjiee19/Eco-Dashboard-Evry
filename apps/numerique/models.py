from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class EquipementNumerique(models.Model):
    TYPE_CHOICES = [
        ('1. Hardware (Terminaux)', (
            ('LAPTOP', 'Ordinateur Portable (250kg CO2e)'),
            ('DESKTOP_SCREEN', 'Ordinateur Fixe + Écran (350kg CO2e)'),
            ('SMARTPHONE', 'Smartphone / Tablette (50kg CO2e)'),
        )),
        ('2. Réseau', (
            ('BORNE_WIFI', 'Borne Wi-Fi (20kg CO2e)'),
            ('SWITCH', 'Switch réseau (80kg CO2e)'),
        )),
        ('3. Cloud & Services', (
            ('CLOUD_INSTANCE', 'Instance Cloud / Serveur virtuel (500kg CO2e)'),
            ('CLOUD_STORAGE', 'Stockage Cloud 1 To (150kg CO2e)'),
        )),
        ('4. Périphériques', (
            ('PRINTER', 'Imprimante Laser (500kg CO2e)'),
            ('SCREEN_EXTRA', 'Écran supplémentaire (200kg CO2e)'),
        )),
    ]
    
    # Données ADEME (Fabrication en kg CO2e total)
    FAB_CO2 = {
        'LAPTOP': 250, 
        'DESKTOP_SCREEN': 350, 
        'SMARTPHONE': 50,
        'BORNE_WIFI': 20, 
        'SWITCH': 80,
        'CLOUD_INSTANCE': 500, 
        'CLOUD_STORAGE': 150,
        'PRINTER': 500, 
        'SCREEN_EXTRA': 200,
    }
    # Consommation moyenne (kWh/an)
    CONSO_MOYENNE = {
        'LAPTOP': 30, 
        'DESKTOP_SCREEN': 170, 
        'SMARTPHONE': 5,
        'BORNE_WIFI': 50, 
        'SWITCH': 100,
        'CLOUD_INSTANCE': 0,  # Cloud: conso incluse dans le facteur total souvent, ou gérée ailleurs
        'CLOUD_STORAGE': 0,
        'PRINTER': 200, 
        'SCREEN_EXTRA': 50,
    }

    user = models.ForeignKey(User, on_delete=models.CASCADE)
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
        # Calcul Fabrication
        facteur_fab = self.FAB_CO2.get(self.type_equipement, 0)
        self.empreinte_fabrication = facteur_fab * self.quantite
        
        # Calcul Consommation (Usage kWh)
        facteur_conso = self.CONSO_MOYENNE.get(self.type_equipement, 0)
        self.consommation_annuelle = facteur_conso * self.quantite

        # Calcul Total Annuel = (Fab / Durée) + (Conso * Facteur Elec)
        amortissement = self.empreinte_fabrication / max(self.duree_vie, 1)
        
        # Facteur Elec France 2024 (approx 0.052 kg/kWh)
        FACTEUR_ELEC = 0.052 
        usage_co2 = self.consommation_annuelle * FACTEUR_ELEC
        
        # Pour les services Cloud, souvent 100% est considéré comme impact annuel (abonnement)
        if 'CLOUD' in self.type_equipement:
            # Si c'est du cloud, on considère que la valeur FAB_CO2 est annuelle (ex: location serveur)
            # Donc pas d'amortissement sur 5 ans par défaut ?
            # On va suivre la logique : Fab / Durée. Si durée = 1 an, c'est tout bon.
            pass

        self.total_co2_kg = amortissement + usage_co2
        
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.nom} - {self.get_type_equipement_display()}"
    
    class Meta:
        verbose_name = "Équipement numérique"
        verbose_name_plural = "Données numérique"
        ordering = ['-year', '-created_at']

