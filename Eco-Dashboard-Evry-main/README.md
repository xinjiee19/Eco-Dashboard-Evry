# Bilan Carbone - Mairie d'Évry-Courcouronnes

Application web interne pour la construction automatisée du bilan carbone municipal.

## � Description

Cette application Django permet aux différents services de la mairie de saisir leurs données de consommation (véhicules, bâtiments, alimentation, achats) et de calculer automatiquement l'impact carbone avec les facteurs d'émission officiels ADEME.

## 🛠️ Stack Technique

- **Backend** : Django 6.0.1
- **Base de données** : PostgreSQL 15+ (production) / SQLite (développement)
- **Frontend** : Django Templates + Vanilla CSS + JavaScript ES6
- **Serveur** : Gunicorn + Nginx (production)

## 🚀 Installation

### Prérequis

- Python 3.12+
- PostgreSQL 15+ (production) ou SQLite (développement)
- Git

### Étapes

```bash
# 1. Cloner le repository
git clone https://github.com/xinjiee19/Eco-Dashboard-Evry.git
cd Eco-Dashboard-Evry

# 2. Créer l'environnement virtuel
python3 -m venv rse-evry
source rse-evry/bin/activate  # Linux/Mac
# rse-evry\Scripts\activate   # Windows

# 3. Installer les dépendances
pip install -r requirements.txt

# 4. Configurer les variables d'environnement (optionnel pour dev)
cp .env.example .env
# Éditer .env avec vos valeurs si nécessaire

# 5. Initialiser la base de données
# OPTION A : Script automatique (recommandé pour dev/démo)
python init_project.py
# Ce script va :
#  - Créer la base de données
#  - Appliquer les migrations
#  - Créer un superuser (admin/admin)
#  - Vous demander si vous voulez générer des données de démo

# OPTION B : Initialisation manuelle
python manage.py migrate
python manage.py createsuperuser

# 6. Lancer le serveur de développement
python manage.py runserver
```

L'application sera accessible sur http://127.0.0.1:8000

### 🎲 Générer des données de démonstration

> ⚠️ **Important** : Aucun script ne se lance automatiquement après le clone.  
> Vous devez **manuellement** lancer les commandes ci-dessous.

#### Méthode 1 : Via le script d'initialisation

```bash
python init_project.py
```

Le script vous demandera si vous voulez générer des données de démo :
- Tapez `o` (oui) pour générer automatiquement des exemples de données
- Tapez `n` (non) pour une base vide

#### Méthode 2 : Via l'interface admin

1. Lancez le serveur : `python manage.py runserver`
2. Connectez-vous à http://127.0.0.1:8000/admin/
3. Créez manuellement des entrées dans chaque module

#### Méthode 3 : Via le shell Django

```bash
python manage.py shell
```

```python
from django.contrib.auth import get_user_model
from apps.vehicles.models import VehicleData

User = get_user_model()
admin = User.objects.first()

# Exemple : Créer une donnée véhicule
VehicleData.objects.create(
    user=admin,
    year=2025,
    service="Direction Générale",
    calculation_method="fuel",
    essence_liters=500,
    gazole_liters=1200
)
```

## 📂 Structure du projet

```
Eco-Dashboard-Evry/
├── manage.py              # Script Django principal
├── requirements.txt       # Dépendances
├── init_project.py        # Script d'initialisation avec données démo
├── config/                # Configuration Django
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── apps/                  # Applications Django
│   ├── core/             # App principale (dashboard, config ADEME)
│   ├── vehicles/         # Module véhicules
│   ├── batiment/         # Module bâtiments
│   ├── purchases/        # Module achats
│   ├── alimentation/     # Module alimentation
│   ├── numerique/        # Module numérique
│   └── sensibilisation/  # Module sensibilisation
├── static/                # Fichiers statiques (CSS, JS, images)
├── templates/             # Templates Django globaux
└── rse-evry/              # Environnement virtuel (git-ignored)
```

## 🎯 Modules

### ✅ Module Véhicules
- Saisie consommation carburant (essence, gazole)
- Calcul automatique émissions CO₂
- Facteurs ADEME : 2.79 kg CO₂e/L (essence), 3.16 kg CO₂e/L (gazole)

### ✅ Module Bâtiments
- Suivi consommations énergétiques (électricité, gaz, chauffage)
- Surface des bâtiments
- Calcul CO₂ selon facteurs ADEME

### ✅ Module Achats
- Catégorisation des achats publics
- Facteurs d'émission par catégorie
- Calcul basé sur montants (€)

### ✅ Module Alimentation
- Suivi des repas par type (bœuf, végétarien, poisson...)
- Facteurs ADEME Agribalyse
- Calcul émissions restauration collective

### ✅ Module Numérique
- Inventaire équipements IT (ordinateurs, serveurs, smartphones)
- Impact fabrication + usage
- Facteurs ADEME secteur numérique

### ✅ Module Sensibilisation
- Actions et initiatives éco-responsables
- Conseils personnalisés
- Équivalences pédagogiques (km voiture, arbres...)

## � Données ADEME

Les facteurs d'émission sont issus de la **Base Carbone® ADEME** (version vérifiée janvier 2026).

Documentation : [ADEME_VERIFIED_VALUES.md](ADEME_VERIFIED_VALUES.md)

## 🧪 Tests

```bash
# Lancer les tests
pytest

# Avec couverture
pytest --cov=apps
```

## 🔄 Réinitialiser le projet

```bash
# Supprimer la base de données
rm db.sqlite3

# Relancer le script d'init
python init_project.py
```

## � Licence

Projet interne - Mairie d'Évry-Courcouronnes

---

**Éco-conçu avec ❤️ pour la transition écologique**
