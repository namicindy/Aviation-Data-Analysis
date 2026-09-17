"""
Référentiel des principaux aéroports commerciaux français.

Liste volontairement limitée aux aéroports à fort trafic commercial : couvrir
les ~10 premiers suffit pour répondre aux questions business du projet, et
évite d'alourdir les calculs avec des centaines de petits aérodromes.
"""

# Coordonnées issues des données publiques DGAC / OurAirports.
AEROPORTS_FRANCE = [
    {"code_iata": "CDG", "nom": "Paris - Charles de Gaulle", "ville": "Paris", "latitude": 49.0097, "longitude": 2.5479},
    {"code_iata": "ORY", "nom": "Paris - Orly", "ville": "Paris", "latitude": 48.7233, "longitude": 2.3794},
    {"code_iata": "NCE", "nom": "Nice - Côte d'Azur", "ville": "Nice", "latitude": 43.6584, "longitude": 7.2159},
    {"code_iata": "LYS", "nom": "Lyon - Saint-Exupéry", "ville": "Lyon", "latitude": 45.7256, "longitude": 5.0811},
    {"code_iata": "MRS", "nom": "Marseille - Provence", "ville": "Marseille", "latitude": 43.4393, "longitude": 5.2214},
    {"code_iata": "TLS", "nom": "Toulouse - Blagnac", "ville": "Toulouse", "latitude": 43.6291, "longitude": 1.3638},
    {"code_iata": "BOD", "nom": "Bordeaux - Mérignac", "ville": "Bordeaux", "latitude": 44.8283, "longitude": -0.7156},
    {"code_iata": "NTE", "nom": "Nantes Atlantique", "ville": "Nantes", "latitude": 47.1532, "longitude": -1.6108},
    {"code_iata": "BSL", "nom": "Bâle-Mulhouse", "ville": "Mulhouse", "latitude": 47.5896, "longitude": 7.5299},
    {"code_iata": "LIL", "nom": "Lille - Lesquin", "ville": "Lille", "latitude": 50.5633, "longitude": 3.0894},
]