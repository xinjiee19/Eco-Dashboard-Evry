import random
from decimal import Decimal
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

# Import models
from apps.batiment.models import BuildingEnergyData
from apps.vehicles.models import VehicleData
from apps.alimentation.models import FoodEntry, FoodEmissionFactor
from apps.purchases.models import PurchaseData, PurchaseEmissionFactor
from apps.numerique.models import EquipementNumerique

User = get_user_model()

class Command(BaseCommand):
    help = 'Populate database with dummy data for graphing visualization.'

    def handle(self, *args, **options):
        self.stdout.write(self.style.WARNING("Starting dummy data generation..."))
        
        # Ensure emission factors exist
        from django.core.management import call_command
        self.stdout.write("Initializing emission factors...")
        call_command('init_factors')
        
        # 0. Clean existing data for a fresh start
        self.stdout.write("Cleaning old data...")
        BuildingEnergyData.objects.all().delete()
        VehicleData.objects.all().delete()
        FoodEntry.objects.all().delete()
        PurchaseData.objects.all().delete()
        EquipementNumerique.objects.all().delete()
        User.objects.filter(is_superuser=False).delete()
        Group.objects.all().delete()
        User.objects.filter(username='admin_demo').delete()

        # 1. Create Admin User
        admin_user = User.objects.create_superuser('admin_demo', 'admin@demo.com', 'admin')
        self.stdout.write(self.style.SUCCESS(f"Superuser '{admin_user.username}' created. (password: admin)"))

        # 2. Initialize Reminder Template & User Manual
        from apps.core.models import ReminderTemplate, UserManual
        ReminderTemplate.get_template()
        self.stdout.write(self.style.SUCCESS("Reminder Template initialized."))

        UserManual.objects.update_or_create(
            group=None,
            defaults={
                'title': "Guide Utilisateur - Eco Dashboard",
                'content': """
                <div class="manual-content">
                    <h3 class="mb-4">🚀 Introduction</h3>
                    <p>Bienvenue sur l'outil de collecte de données carbone de la Mairie d'Evry-Courcouronnes. Cet outil permet à chaque service de renseigner ses activités afin de calculer automatiquement l'empreinte carbone de la collectivité.</p>
                    
                    <hr class="my-5">

                    <h3 class="mb-4">📂 Les Modules de Saisie</h3>
                    
                    <div class="row">
                        <div class="col-md-4 mb-4">
                            <h4 class="text-secondary">🏢 Bâtiments</h4>
                            <p class="small text-muted">Saisissez ici les consommations énergétiques de vos locaux.</p>
                            <ul class="small">
                                <li><strong>Électricité (kWh) :</strong> Relevez vos factures annuelles.</li>
                                <li><strong>Gaz & Chaleur :</strong> Indiquez les kWh consommés.</li>
                                <li><strong>Info requise :</strong> Nom du site, surface, année construction.</li>
                            </ul>
                        </div>
                        
                        <div class="col-md-4 mb-4">
                            <h4 class="text-primary">🚗 Véhicules</h4>
                            <p class="small text-muted">Pour la flotte de véhicules de service.</p>
                            <ul class="small">
                                <li><strong>Par Carburant (Recommandé) :</strong> Litres d'essence/gazole (plus précis).</li>
                                <li><strong>Par Distance :</strong> Kilomètres parcourus si vous n'avez pas les litres.</li>
                            </ul>
                        </div>
                        
                        <div class="col-md-4 mb-4">
                            <h4 class="text-success">🍽️ Alimentation</h4>
                            <p class="small text-muted">Pour les services de restauration (Cantines, Crèches...).</p>
                            <ul class="small">
                                <li>Indiquez le <strong>nombre de repas</strong> par an pour chaque type.</li>
                                <li>Distinguez bien les repas végétariens des repas carnés (impact très différent).</li>
                            </ul>
                        </div>

                        <div class="col-md-6 mb-4">
                            <h4 class="text-secondary" style="color: #9B59B6 !important;">🛍️ Achats</h4>
                            <p class="small text-muted">Pour les prestations de services et achats divers.</p>
                            <ul class="small">
                                <li>Saisissez le <strong>Montant HT</strong> engagé sur l'année.</li>
                                <li><strong>Attention :</strong> Ne saisissez PAS le matériel informatique ici (utilisez le module Numérique).</li>
                            </ul>
                        </div>

                        <div class="col-md-6 mb-4">
                            <h4 class="text-dark">💻 Numérique</h4>
                            <p class="small text-muted">Inventaire du matériel informatique physique.</p>
                            <ul class="small">
                                <li>Saisissez le <strong>nombre d'équipements</strong> (PC, Écrans, Smartphones...).</li>
                                <li>Précisez la durée de vie estimée (amortissement carbone).</li>
                            </ul>
                        </div>
                    </div>

                    <hr class="my-5">

                    <h3 class="mb-4">📊 Visualisation & Export</h3>
                    <p>Une fois vos données saisies, rendez-vous dans l'onglet <strong>"Statistiques"</strong> pour visualiser l'impact global.<br>
                    Vous pouvez télécharger un rapport complet au format <strong>Excel</strong> via le bouton "Exporter".</p>

                    <div class="text-center mt-5">
                        <a href="/" class="btn btn-success btn-lg px-5">J'ai compris, commencer la saisie !</a>
                    </div>
                </div>
                """
            }
        )
        self.stdout.write(self.style.SUCCESS("Default User Manual updated."))

        # 3. Define Sectors, Create Groups and a sample User for each Group
        self.stdout.write("Creating groups and a sample user for each sector...")
        sectors = ["Bâtiments", "Véhicules", "Alimentation", "Achats", "Numérique"]
        groups = {}
        users = {}
        for sector_name in sectors:
            group, _ = Group.objects.get_or_create(name=sector_name)
            groups[sector_name] = group
            
            # Sanitize username
            username = f"agent_{sector_name.lower().replace('é', 'e').replace('â', 'a')}"
            user, created = User.objects.get_or_create(
                username=username, 
                defaults={'email': f'{username}@demo.com'}
            )
            if created:
                user.set_password('password')
                user.save()
            
            user.groups.add(group)
            users[sector_name] = user
            self.stdout.write(f"  - Group '{group.name}' created.")
            self.stdout.write(f"  - User '{user.username}' created and added to group. (password: password)")


        # --- Static Data & Factors ---

        services = [
            "Direction des Sports", "Services Techniques", "Mairie Annexe", 
            "Ecole Jules Ferry", "Police Municipale", "C.C.A.S.", 
            "Espaces Verts", "Restauration Scolaire", "Voirie"
        ]
        years = [2024, 2025, 2026]

        # Populate Emission Factors for Purchases (if empty)
        if not PurchaseEmissionFactor.objects.exists():
            self.stdout.write("Populating Purchase Emission Factors...")
            factors_data = [
                ('food_service', 'Restauration & Services légers', 100),
                ('insurance', 'Assurances & Cotisations', 110),
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

        # Populate Emission Factors for Food (if empty)
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
        
        # 3. Populate Sector Data
        
        # --- BATIMENTS ---
        self.stdout.write("Generating Batiment Data...")
        batiments_group = groups["Bâtiments"]
        batiments_user = users["Bâtiments"]
        for year in years:
            for service in services:
                if random.random() > 0.8: continue

                BuildingEnergyData.objects.create(
                    group=batiments_group,
                    user=batiments_user,
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
        vehicules_group = groups["Véhicules"]
        vehicules_user = users["Véhicules"]
        for year in years:
            for service in services:
                if random.random() > 0.7: continue
                
                method = random.choice(['fuel', 'distance'])
                entry = VehicleData(
                    group=vehicules_group,
                    user=vehicules_user,
                    year=year,
                    service=service,
                    calculation_method=method
                )
                if method == 'fuel':
                    entry.essence_liters = Decimal(random.randint(100, 5000))
                    entry.gazole_liters = Decimal(random.randint(100, 5000))
                else:
                    entry.distance_km = Decimal(random.randint(1000, 50000))
                
                entry.save() 

        # --- ALIMENTATION ---
        self.stdout.write("Generating Alimentation Data...")
        alimentation_group = groups["Alimentation"]
        alimentation_user = users["Alimentation"]
        for year in years:
            for service in services:
                if random.random() > 0.7: continue
                
                if FoodEntry.objects.filter(group=alimentation_group, year=year, service=service).exists():
                    continue

                FoodEntry.objects.create(
                    group=alimentation_group,
                    user=alimentation_user,
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
        achats_group = groups["Achats"]
        achats_user = users["Achats"]
        categories = [c[0] for c in PurchaseData.CATEGORY_CHOICES]
        for year in years:
            for service in services:
                for _ in range(random.randint(1, 4)):
                    PurchaseData.objects.create(
                        group=achats_group,
                        user=achats_user,
                        year=year,
                        service=service,
                        category=random.choice(categories),
                        description="Achat divers pour fonctionnement",
                        amount_euros=Decimal(random.randint(1000, 100000))
                    )

        # --- NUMERIQUE ---
        self.stdout.write("Generating Numerique Data...")
        numerique_group = groups["Numérique"]
        numerique_user = users["Numérique"]
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

                for _ in range(random.randint(1, 4)):
                    qty = random.randint(1, 50)
                    equip_type = random.choice(list(marques_by_type.keys()))
                    marque = random.choice(marques_by_type[equip_type])
                    
                    EquipementNumerique.objects.create(
                        group=numerique_group,
                        user=numerique_user,
                        year=year,
                        nom=f"Parc {service} - Lot {random.randint(1,10)}",
                        marque_modele=marque,
                        type_equipement=equip_type,
                        quantite=qty,
                        duree_vie=random.randint(3, 7)
                    )

        # --- ADMIN DATA ---
        # --- ADMIN DATA ---
        # Generate some data for superusers (admin, admin_demo) so they see something in Lists
        self.stdout.write("Generating Admin Data...")
        admins = User.objects.filter(is_superuser=True)
        # Admins will get data assigned to "Bâtiments" group for example, or null
        # Let's assign them to "Bâtiments" to simulate they are also in a group if needed
        # Or just assign group=None if we want to test that. But models allow null.
        # But RBAC views filter by group. So if admin is not in group, they only see if they are superuser.
        # Superuser sees all. So group doesn't matter much for visibility but good for consistency.
        # Let's assign to "Bâtiments" group for consistency.
        
        # Actually, let's just create data without group or with a random group for Admin to show they own it?
        # If views filter by "user.groups.all()", and Admin has NO groups, but is superuser -> sees ALL.
        # So it doesn't matter what group the data has.
        
        for admin in admins:
            for year in years:
            # Vehicle
                VehicleData.objects.create(
                    group=groups["Véhicules"],
                    user=admin,
                    year=year,
                    service="Mairie - Direction",
                    calculation_method="distance",
                    distance_km=Decimal(random.randint(5000, 20000))
                )
                # Building
                BuildingEnergyData.objects.create(
                    group=groups["Bâtiments"],
                    user=admin,
                    year=year,
                    site_name="Hôtel de Ville",
                    construction_year=1980,
                    surface_area=Decimal(5000),
                    electricity_kwh=Decimal(150000),
                    gas_kwh=Decimal(80000),
                    electricity_factor=Decimal("0.052"),
                    gas_factor=Decimal("0.227"),
                    heating_network_factor=Decimal("0.150"),
                    cooling_factor=Decimal("0.052")
                )
                # Food
                FoodEntry.objects.create(
                    group=groups["Alimentation"],
                    user=admin,
                    year=year,
                    service="Cantine Centrale",
                    beef_meals=100,
                    pork_meals=100,
                    poultry_fish_meals=100,
                    vegetarian_meals=100,
                    picnic_no_meat_meals=50,
                    picnic_meat_meals=50
                )
                # Purchase
                PurchaseData.objects.create(
                    group=groups["Achats"],
                    user=admin,
                    year=year,
                    service="Achats Généraux",
                    category="equipment_rental",
                    description="Location Photocopieurs",
                    amount_euros=Decimal(15000)
                )
                # Numerique
                EquipementNumerique.objects.create(
                    group=groups["Numérique"],
                    user=admin,
                    year=year,
                    nom="PC Admin",
                    marque_modele="Dell XPS",
                    type_equipement="LAPTOP",
                    quantite=5,
                    duree_vie=4
                )
        
        self.stdout.write(self.style.SUCCESS("Successfully generated dummy data!"))
