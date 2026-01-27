from django.db import migrations

def populate_factors(apps, schema_editor):
    BuildingEmissionFactor = apps.get_model('batiment', 'BuildingEmissionFactor')
    
    factors = [
        ('ELEC', 0.052),
        ('GAZ', 0.227),
        ('HEAT', 0.150),
        ('COOL', 0.052),
    ]

    for code, val in factors:
        BuildingEmissionFactor.objects.create(
            type_energie=code,
            facteur=val
        )

def reverse_func(apps, schema_editor):
    BuildingEmissionFactor = apps.get_model('batiment', 'BuildingEmissionFactor')
    BuildingEmissionFactor.objects.all().delete()

class Migration(migrations.Migration):

    dependencies = [
        ('batiment', '0004_buildingemissionfactor'),
    ]

    operations = [
        migrations.RunPython(populate_factors, reverse_func),
    ]
