from django.core.management.base import BaseCommand
from apps.vehicles.models import EmissionFactor
from apps.batiment.models import BuildingEmissionFactor
from apps.alimentation.models import FoodEmissionFactor
from apps.purchases.models import PurchaseEmissionFactor
from apps.numerique.models import NumeriqueEmissionFactor
from decimal import Decimal

class Command(BaseCommand):
    help = 'Initialize default ADEME emission factors for all modules'

    def handle(self, *args, **kwargs):
        self.stdout.write("Initializing Emission Factors...")

        # 1. VEHICULES
        self.stdout.write("- Vehicles...")
        vehicles_factors = [
            {'name': 'Essence', 'category': 'fuel', 'unit': 'L', 'value': '2.79', 'source': 'ADEME'},
            {'name': 'Gazole', 'category': 'fuel', 'unit': 'L', 'value': '3.16', 'source': 'ADEME'},
            {'name': 'Voiture thermique moyenne', 'category': 'vehicle_km', 'unit': 'km', 'value': '0.192', 'source': 'ADEME'},
        ]
        for f in vehicles_factors:
            EmissionFactor.objects.get_or_create(
                name=f['name'],
                defaults={
                    'category': f['category'],
                    'unit': f['unit'],
                    'factor_value': Decimal(f['value']),
                    'source': f['source']
                }
            )

        # 2. BATIMENT
        self.stdout.write("- Batiment...")
        batiment_factors = [
            {'type': 'ELEC', 'facteur': '0.052', 'unit': 'kgCO2e/kWh'},
            {'type': 'GAZ', 'facteur': '0.227', 'unit': 'kgCO2e/kWh'},
            {'type': 'HEAT', 'facteur': '0.150', 'unit': 'kgCO2e/kWh'},
            {'type': 'COOL', 'facteur': '0.052', 'unit': 'kgCO2e/kWh'},
        ]
        for f in batiment_factors:
            BuildingEmissionFactor.objects.get_or_create(
                type_energie=f['type'],
                defaults={
                    'facteur': Decimal(f['facteur']),
                    'unit': f['unit']
                }
            )

        # 3. ALIMENTATION
        self.stdout.write("- Alimentation...")
        food_factors = [
            {'code': 'beef', 'label': 'Repas bœuf/veau', 'value': '7.260'},
            {'code': 'pork', 'label': 'Repas porc', 'value': '1.580'},
            {'code': 'poultry_fish', 'label': 'Repas poulet/poisson', 'value': '1.380'},
            {'code': 'vegetarian', 'label': 'Repas végétariens', 'value': '0.510'},
            {'code': 'picnic_veg', 'label': 'Pique-niques sans viande', 'value': '0.510'},
            {'code': 'picnic_meat', 'label': 'Pique-niques avec viande', 'value': '1.580'},
        ]
        for f in food_factors:
            FoodEmissionFactor.objects.get_or_create(
                code=f['code'],
                defaults={
                    'label': f['label'],
                    'kg_co2_per_meal': Decimal(f['value'])
                }
            )

        # 4. ACHATS
        self.stdout.write("- Achats...")
        purchase_factors = [
             ('food_service', 'Restauration & Services légers', '100.00'),
             ('insurance', 'Assurances & Cotisations', '110.00'),
             ('it_telecom', 'IT & Téléphonie', '160.00'),
             ('cleaning_maintenance', 'Nettoyage & Entretien & Espaces verts', '215.00'),
             ('activities', 'Séjours & Activités', '270.00'),
             ('laundry', 'Blanchisserie', '320.00'),
             ('construction', 'Travaux & Construction', '360.00'),
             ('transport', 'Transports', '560.00'),
             ('equipment_rental', 'Location équipements', '600.00'),
        ]
        for code, label, value in purchase_factors:
            PurchaseEmissionFactor.objects.get_or_create(
                category_code=code,
                defaults={
                    'category_label': label,
                    'factor_kg_co2_per_keur': Decimal(value)
                }
            )

        # 5. NUMERIQUE
        self.stdout.write("- Numerique...")
        numerique_factors = [
            {'type': 'LAPTOP', 'nom': 'Ordinateur Portable', 'fab': '250', 'conso': '30'},
            {'type': 'DESKTOP_SCREEN', 'nom': 'Ordinateur Fixe + Écran', 'fab': '350', 'conso': '170'},
            {'type': 'SMARTPHONE', 'nom': 'Smartphone / Tablette', 'fab': '50', 'conso': '5'},
            {'type': 'BORNE_WIFI', 'nom': 'Borne Wi-Fi', 'fab': '20', 'conso': '50'},
            {'type': 'SWITCH', 'nom': 'Switch réseau', 'fab': '80', 'conso': '100'},
            {'type': 'CLOUD_INSTANCE', 'nom': 'Instance Cloud / Serveur virtuel', 'fab': '500', 'conso': '0'},
            {'type': 'CLOUD_STORAGE', 'nom': 'Stockage Cloud 1 To', 'fab': '150', 'conso': '0'},
            {'type': 'PRINTER', 'nom': 'Imprimante Laser', 'fab': '500', 'conso': '200'},
            {'type': 'SCREEN_EXTRA', 'nom': 'Écran supplémentaire', 'fab': '200', 'conso': '50'},
        ]
        for f in numerique_factors:
            NumeriqueEmissionFactor.objects.get_or_create(
                type_equipement=f['type'],
                defaults={
                    'nom': f['nom'],
                    'fabrication_kg_co2': Decimal(f['fab']),
                    'conso_kwh_an': Decimal(f['conso'])
                }
            )

        self.stdout.write(self.style.SUCCESS('Successfully initialized all emission factors!'))
