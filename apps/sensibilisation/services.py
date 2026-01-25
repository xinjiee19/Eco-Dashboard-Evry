from decimal import Decimal
from django.db.models import Sum

class SensibilisationService:
    # Facteurs ADEME (Moyennes approximatives)
    FACTEUR_VOITURE_KM = 0.218  # kgCO2e/km (Voiture thermique moyenne)
    FACTEUR_REPAS_BOEUF = 7.0   # kgCO2e (Repas avec boeuf)
    FACTEUR_REPAS_VEGE = 0.5    # kgCO2e (Repas végétarien)
    FACTEUR_SMARTPHONE = 30.0   # kgCO2e (Fabrication smartphone)
    ABSORPTION_ARBRE = 25.0     # kgCO2e/an (Absorption moyenne arbre adulte)

    @staticmethod
    def get_equivalences(total_co2_kg):
        """Convertit une quantité de CO2 (kg) en équivalences parlantes"""
        if not total_co2_kg:
            return None
        
        total = float(total_co2_kg)
        
        return {
            'km_voiture': int(total / SensibilisationService.FACTEUR_VOITURE_KM),
            'repas_boeuf': int(total / SensibilisationService.FACTEUR_REPAS_BOEUF),
            'repas_vege': int(total / SensibilisationService.FACTEUR_REPAS_VEGE),
            'smartphones': int(total / SensibilisationService.FACTEUR_SMARTPHONE),
            'arbres': int(total / SensibilisationService.ABSORPTION_ARBRE)
        }

    @staticmethod
    def get_conseils_automatiques(stats_par_module):
        """Génère des conseils basés sur les données réelles"""
        conseils = []
        
        total = stats_par_module.get('total', 0)
        transport = stats_par_module.get('vehicles', 0)
        numerique = stats_par_module.get('numerique', 0)
        batiment = stats_par_module.get('batiment', 0)
        
        if total > 0:
            part_transport = (transport / total) * 100
            part_numerique = (numerique / total) * 100
            part_batiment = (batiment / total) * 100
            
            # Conseils Transport
            if part_transport > 40:
                conseils.append({
                    'type': 'transport',
                    'titre': '🚗 Mobilité',
                    'texte': f"Le transport représente {int(part_transport)}% de votre empreinte. Avez-vous pensé au forfait mobilité durable ou au covoiturage ?"
                })
            
            # Conseils Numérique
            if numerique > 2000: # Seuil arbitraire 2 tonnes
                conseils.append({
                    'type': 'numerique',
                    'titre': '💻 Numérique',
                    'texte': "Votre empreinte numérique est importante. Allonger la durée de vie de vos équipements de 3 à 5 ans réduit leur impact de 40%."
                })
                
            # Conseils Bâtiment
            if part_batiment > 50:
                conseils.append({
                    'type': 'batiment',
                    'titre': '🏢 Bâtiments',
                    'texte': "Le chauffage est votre premier poste d'émission. Baisser la température de 1°C permet d'économiser 7% d'énergie."
                })
                
        # Fallback si pas assez de données
        if not conseils:
            conseils.append({
                'type': 'general',
                'titre': '🌱 Astuce',
                'texte': "Commencez par mesurer l'ensemble de vos postes pour identifier les gisements d'économies les plus impactants."
            })
            
        return conseils[:3] # Max 3 conseils
