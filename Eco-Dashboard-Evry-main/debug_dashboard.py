import os
import django
from django.conf import settings
from django.db.models import Sum
from django.utils import timezone

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.vehicles.models import VehicleData
from apps.purchases.models import PurchaseData
from apps.alimentation.models import FoodEntry
from apps.batiment.models import BuildingEnergyData
from apps.numerique.models import EquipementNumerique

try:
    current_year = timezone.now().year
    print(f"Year: {current_year}")

    vehicles_total = float(VehicleData.objects.filter(year=current_year).aggregate(total=Sum('total_co2_kg'))['total'] or 0)
    print(f"Vehicles: {vehicles_total}")
    
    purchases_total = float(PurchaseData.objects.filter(year=current_year).aggregate(total=Sum('total_co2_kg'))['total'] or 0)
    print(f"Purchases: {purchases_total}")
    
    alimentation_total = float(FoodEntry.objects.filter(year=current_year).aggregate(total=Sum('total_co2_kg'))['total'] or 0)
    print(f"Alimentation: {alimentation_total}")
    
    building_total = float(BuildingEnergyData.objects.filter(year=current_year).aggregate(total=Sum('total_co2_kg'))['total'] or 0)
    print(f"Buildings: {building_total}")

    numerique_total = float(EquipementNumerique.objects.filter(year=current_year).aggregate(total=Sum('total_co2_kg'))['total'] or 0)
    print(f"Numerique: {numerique_total}")
    
    total = vehicles_total + purchases_total + alimentation_total + building_total + numerique_total
    print(f"Total: {total}")

except Exception as e:
    print(f"ERROR: {e}")
