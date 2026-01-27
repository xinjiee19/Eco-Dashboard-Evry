from django.db import migrations

def populate_factors(apps, schema_editor):
    EmissionFactor = apps.get_model('vehicles', 'EmissionFactor')
    
    # Données par défaut (valeurs actuelles hardcodées)
    factors = [
        # (Name, Category, Unit, Value)
        ('Essence', 'fuel', 'L', 2.79),
        ('Gazole', 'fuel', 'L', 3.16),
        ('Voiture thermique moyenne', 'vehicle_km', 'km', 0.192),
    ]

    for name, cat, unit, val in factors:
        # On utilise get_or_create pour éviter doublons
        if not EmissionFactor.objects.filter(name=name).exists():
            EmissionFactor.objects.create(
                name=name,
                category=cat,
                unit=unit,
                factor_value=val,
                source="ADEME Base Carbone"
            )

def reverse_func(apps, schema_editor):
    pass

class Migration(migrations.Migration):

    dependencies = [
        ("vehicles", "0002_alter_vehicledata_year"),
    ]

    operations = [
        migrations.RunPython(populate_factors, reverse_func),
    ]
