import random
from decimal import Decimal
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.utils import timezone

# Import models
from apps.batiment.models import BuildingEnergyData
from apps.vehicles.models import VehicleData, EmissionFactor as VehicleFactor
from apps.alimentation.models import FoodEntry, FoodEmissionFactor
from apps.purchases.models import PurchaseData, PurchaseEmissionFactor

User = get_user_model()

class Command(BaseCommand):
    help = 'Populate database with dummy data for graphing visualization.'

    def handle(self, *args, **options):
        self.stdout.write(self.style.WARNING("Starting dummy data generation..."))
        
        # 0. Clean existing data
        self.stdout.write("Cleaning old data...")
        BuildingEnergyData.objects.all().delete()
        VehicleData.objects.all().delete()
        FoodEntry.objects.all().delete()
        PurchaseData.objects.all().delete()

        # 1. Get or Create User
        user = User.objects.first()
        if not user:
            self.stdout.write("No user found. Creating 'admin_demo'...")
            user = User.objects.create_superuser('admin_demo', 'admin@demo.com', 'admin')
        
        self.stdout.write(f"Assigning data to user: {user.username}")

        # 2. Services List
        services = [
            "Direction des Sports", "Services Techniques", "Mairie Annexe", 
            "Ecole Jules Ferry", "Police Municipale", "C.C.A.S.", 
            "Espaces Verts", "Restauration Scolaire", "Voirie"
        ]

        years = [2024, 2025, 2026]

        # 3. Populate Emission Factors for Purchases (if empty)
        if not PurchaseEmissionFactor.objects.exists():
            self.stdout.write("Populating Purchase Emission Factors...")
            factors_data = [
                ('food_service', 'Restauration & Services légers', 100),
                ('insurance', 'Assurances & Cotisations', 110),
                ('it_telecom', 'IT & Téléphonie', 160),
                ('cleaning_maintenance', 'Nettoyage & Entretien & Espaces verts', 215),
                ('activities', 'Séjours & Activités', 270),
                ('laundry', 'Blanchisserie', 320),
                ('construction', 'Travaux & Construction', 360),
                ('transport', 'Transports', 560),
                ('equipment_rental', 'Location équipements', 600),
            ]
            for code, label, val in factors_data:
                PurchaseEmissionFactor.objects.create(
                    category_code=code,
                    category_label=label,
                    factor_kg_co2_per_keur=Decimal(val)
                )

        # 4. Populate Emission Factors for Food (if empty)
        if not FoodEmissionFactor.objects.exists():
            self.stdout.write("Populating Food Emission Factors...")
            food_factors = [
                ('beef', 'Bœuf/Veau', 6.0), # Dummy value close to reality (actually much higher usually ~30-60, maybe per meal it's lower)
                # Note: The model says kg_co2_per_meal. ADEME is ~7kg/kg usually. Per meal containing beef ~2-7kg?
                # Let's use simple plausible values for demo.
                ('pork', 'Porc', 2.0),
                ('poultry_fish', 'Volaille/Poisson', 1.5),
                ('vegetarian', 'Végétarien', 0.5),
                ('picnic_meat', 'Pique-nique (viande)', 1.5),
                ('picnic_veg', 'Pique-nique (végé)', 0.5),
            ]
            for code, label, val in food_factors:
                FoodEmissionFactor.objects.create(
                    code=code, label=label, kg_co2_per_meal=Decimal(val)
                )
        
        # 5. Populate Data
        
        # --- BATIMENTS ---
        self.stdout.write("Generating Batiment Data...")
        for year in years:
            for service in services:
                # Not every service has a building every year, but let's say yes for demo
                if random.random() > 0.8: continue

                BuildingEnergyData.objects.create(
                    user=user,
                    year=year,
                    site_name=f"Bâtiment {service}",
                    construction_year=random.randint(1970, 2010),
                    surface_area=Decimal(random.randint(200, 3000)),
                    electricity_kwh=Decimal(random.randint(5000, 50000)),
                    gas_kwh=Decimal(random.randint(0, 40000)),
                    heating_network_kwh=Decimal(random.randint(0, 20000)),
                    cooling_kwh=Decimal(random.randint(0, 10000)),
                    electricity_factor=Decimal("0.052"),
                    gas_factor=Decimal("0.227"),
                    heating_network_factor=Decimal("0.150"),
                    cooling_factor=Decimal("0.052")
                )

        # --- VEHICLES ---
        self.stdout.write("Generating Vehicle Data...")
        for year in years:
            for service in services:
                if random.random() > 0.7: continue
                
                method = random.choice(['fuel', 'distance'])
                entry = VehicleData(
                    user=user,
                    year=year,
                    service=service,
                    calculation_method=method
                )
                if method == 'fuel':
                    entry.essence_liters = Decimal(random.randint(100, 5000))
                    entry.gazole_liters = Decimal(random.randint(100, 5000))
                else:
                    entry.distance_km = Decimal(random.randint(1000, 50000))
                
                entry.save() # Triggers calculate_impact

        # --- ALIMENTATION ---
        self.stdout.write("Generating Alimentation Data...")
        for year in years:
            for service in services:
                # Randomly decide if this service has food entry
                if random.random() > 0.7: continue
                
                # Check existance to avoid IntegrityError
                if FoodEntry.objects.filter(year=year, service=service).exists():
                    continue

                FoodEntry.objects.create(
                    user=user,
                    year=year,
                    service=service,
                    beef_meals=random.randint(500, 5000),
                    pork_meals=random.randint(500, 5000),
                    poultry_fish_meals=random.randint(500, 5000),
                    vegetarian_meals=random.randint(500, 5000),
                    picnic_no_meat_meals=random.randint(100, 1000),
                    picnic_meat_meals=random.randint(100, 1000)
                )


        # --- PURCHASES ---
        self.stdout.write("Generating Purchases Data...")
        categories = [c[0] for c in PurchaseData.CATEGORY_CHOICES]
        for year in years:
            for service in services:
                # Create 1-3 purchases per service
                for _ in range(random.randint(1, 4)):
                    PurchaseData.objects.create(
                        user=user,
                        year=year,
                        service=service,
                        category=random.choice(categories),
                        description="Achat divers pour fonctionnement",
                        amount_euros=Decimal(random.randint(1000, 100000))
                    ) # save() triggers calc

        # --- NUMERIQUE ---
        self.stdout.write("Generating Numerique Data...")
        from apps.numerique.models import EquipementNumerique

        EquipementNumerique.objects.all().delete()

        # Realistic brands/models for each type
        marques_by_type = {
            'LAPTOP': ['Dell Latitude 5420', 'HP EliteBook 840', 'Lenovo ThinkPad T14', 'ASUS ExpertBook B9'],
            'DESKTOP_SCREEN': ['Dell OptiPlex 7090 + P2419H', 'HP ProDesk 600 + E243', 'Lenovo ThinkCentre M90t + L24q'],
            'SMARTPHONE': ['Samsung Galaxy A52', 'iPhone 12', 'Xiaomi Redmi Note 11', 'Google Pixel 6'],
            'BORNE_WIFI': ['Cisco Meraki MR46', 'Ubiquiti UniFi AP AC Pro', 'TP-Link EAP660 HD'],
            'SWITCH': ['Cisco Catalyst 2960', 'Netgear GS728T', 'HP Aruba 2930F'],
            'PRINTER': ['HP LaserJet Pro M404dn', 'Canon imageRUNNER 2625i', 'Xerox VersaLink C405'],
        }
        
        for year in years:
            for service in services:
                if random.random() > 0.8: continue

                # Add a few items per service
                for _ in range(random.randint(1, 4)):
                    qty = random.randint(1, 50)
                    equip_type = random.choice(list(marques_by_type.keys()))
                    marque = random.choice(marques_by_type[equip_type])
                    
                    EquipementNumerique.objects.create(
                        user=user,
                        year=year,
                        nom=f"Parc {service} - Lot {random.randint(1,10)}",
                        marque_modele=marque,
                        type_equipement=equip_type,
                        quantite=qty,
                        duree_vie=random.randint(3, 7)
                    )

        self.stdout.write(self.style.SUCCESS("Successfully generated dummy data!"))
