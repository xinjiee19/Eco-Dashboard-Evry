#!/usr/bin/env python
"""
Script d'initialisation du projet Eco-Dashboard-Evry
À exécuter après un clone fresh pour :
1. Créer la base de données
2. Créer un superuser
3. Générer des données de démonstration (optionnel)
"""
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth import get_user_model
from django.core.management import call_command

User = get_user_model()

def main():
    print("=" * 60)
    print("🌱 INITIALISATION ECO-DASHBOARD EVRY")
    print("=" * 60)
    
    # 1. Migrations
    print("\n📦 Application des migrations...")
    call_command('migrate', '--noinput')
    print("✅ Migrations appliquées")
    
    # 2. Superuser
    print("\n👤 Création du superuser...")
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser(
            username='admin',
            email='admin@evry.fr',
            password='admin'
        )
        print("✅ Superuser créé (admin/admin)")
    else:
        print("ℹ️  Superuser existe déjà")
    
    # 3. Données de démo (optionnel)
    print("\n📊 Générer des données de démonstration ? (o/n): ", end='')
    generate_demo = input().strip().lower()
    
    if generate_demo in ['o', 'oui', 'y', 'yes']:
        print("\n🎲 Utilisation du script de génération de données...")
        try:
            call_command('populate_fake_data')
            print("\n✅ Données de démonstration générées !")
        except Exception as e:
            print(f"⚠️  Erreur lors de la génération : {e}")
            print("Vous pouvez créer des données manuellement via l'admin.")
    
    print("\n" + "=" * 60)
    print("✨ INITIALISATION TERMINÉE !")
    print("=" * 60)
    print("\n📝 Prochaines étapes :")
    print("  1. Démarrer le serveur : python manage.py runserver")
    print("  2. Accéder à l'admin : http://127.0.0.1:8000/admin/")
    print("  3. Identifiants : admin / admin")
    print("\n🎯 Dashboard : http://127.0.0.1:8000/\n")

if __name__ == '__main__':
    main()
