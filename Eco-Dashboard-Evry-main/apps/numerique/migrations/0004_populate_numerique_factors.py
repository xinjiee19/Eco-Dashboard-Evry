from django.db import migrations

def populate_factors(apps, schema_editor):
    NumeriqueEmissionFactor = apps.get_model('numerique', 'NumeriqueEmissionFactor')
    
    factors = [
        # (Code, Label, Fab, Conso)
        # Valeurs issues de apps/numerique/models.py (ancien hardcode)
        ('LAPTOP', 'Ordinateur Portable', 250, 30),
        ('DESKTOP_SCREEN', 'Ordinateur Fixe + Écran', 350, 170),
        ('SMARTPHONE', 'Smartphone / Tablette', 50, 5),
        ('BORNE_WIFI', 'Borne Wi-Fi', 20, 50),
        ('SWITCH', 'Switch réseau', 80, 100),
        ('CLOUD_INSTANCE', 'Instance Cloud / Serveur virtuel', 500, 0),
        ('CLOUD_STORAGE', 'Stockage Cloud 1 To', 150, 0),
        ('PRINTER', 'Imprimante Laser', 500, 200),
        ('SCREEN_EXTRA', 'Écran supplémentaire', 200, 50),
    ]

    for code, label, fab, conso in factors:
        NumeriqueEmissionFactor.objects.create(
            type_equipement=code,
            nom=label,
            fabrication_kg_co2=fab,
            conso_kwh_an=conso
        )

def reverse_func(apps, schema_editor):
    NumeriqueEmissionFactor = apps.get_model('numerique', 'NumeriqueEmissionFactor')
    NumeriqueEmissionFactor.objects.all().delete()

class Migration(migrations.Migration):

    dependencies = [
        ('numerique', '0003_numeriqueemissionfactor_and_more'),
    ]

    operations = [
        migrations.RunPython(populate_factors, reverse_func),
    ]
