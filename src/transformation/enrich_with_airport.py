"""
Enrichissement — associe à chaque avion l'aéroport français le plus proche,
en se basant sur ses coordonnées GPS actuelles.

Ce script lit le CSV déjà nettoyé (produit par parse_opensky_states.py) et
ajoute deux colonnes : l'aéroport le plus proche et la distance en km.
"""

import math
from pathlib import Path

import pandas as pd

from aeroports_reference import AEROPORTS_FRANCE

PROJECT_ROOT = Path(__file__).resolve().parents[2]
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"

# Au-delà de cette distance, on considère qu'aucun aéroport n'est "pertinent"
# pour cet avion (il est probablement en croisière, loin de tout aéroport).
# Pourquoi 50 km et pas 500 ? Parce qu'on veut capturer les avions au sol,
# en approche ou au décollage; pas tout le ciel français. 50 km est une
# valeur de départ raisonnable, à ajuster si on observe trop/pas assez de
# correspondances une fois les vraies données regardées.
DISTANCE_MAX_KM = 50


def distance_haversine_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """
    Calcule la distance réelle en kilomètres entre deux points GPS, en
    tenant compte de la courbure de la Terre (formule de Haversine).

    Haversine calcule la distance sur la sphère terrestre, pas sur un plan.
    """
    RAYON_TERRE_KM = 6371.0

    # On convertit les degrés en radians car les fonctions trigonométriques
    # de Python (math.sin, math.cos...) attendent des radians, pas des degrés.
    lat1_rad, lon1_rad = math.radians(lat1), math.radians(lon1)
    lat2_rad, lon2_rad = math.radians(lat2), math.radians(lon2)

    delta_lat = lat2_rad - lat1_rad
    delta_lon = lon2_rad - lon1_rad

    a = (
        math.sin(delta_lat / 2) ** 2
        + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(delta_lon / 2) ** 2
    )
    c = 2 * math.asin(math.sqrt(a))

    return RAYON_TERRE_KM * c


def trouver_aeroport_le_plus_proche(latitude: float, longitude: float) -> tuple[str, float]:
    """
    Compare la position donnée à tous les aéroports de référence, et retourne
    (code_iata, distance_km) de celui le plus proche.

    On boucle sur une liste de 10 aéroports seulement, donc pas besoin d'optimisation particulière.
    """
    meilleur_aeroport = None
    meilleure_distance = float("inf")  # on part d'une distance "infinie"

    for aeroport in AEROPORTS_FRANCE:
        distance = distance_haversine_km(
            latitude, longitude, aeroport["latitude"], aeroport["longitude"]
        )
        if distance < meilleure_distance:
            meilleure_distance = distance
            meilleur_aeroport = aeroport["code_iata"]

    return meilleur_aeroport, meilleure_distance


def enrichir_avec_aeroport(df: pd.DataFrame) -> pd.DataFrame:
    """
    Ajoute deux colonnes au DataFrame : aeroport_proche et distance_aeroport_km.

    On utilise .apply() avec une fonction ligne par ligne : pour chaque ligne
    du tableau, on calcule l'aéroport le plus proche et on répartit le
    résultat (un tuple) dans deux nouvelles colonnes.
    """
    resultats = df.apply(
        lambda ligne: trouver_aeroport_le_plus_proche(ligne["latitude"], ligne["longitude"]),
        axis=1,
    )

    df = df.copy()
    df["aeroport_proche"] = resultats.apply(lambda r: r[0])
    df["distance_aeroport_km"] = resultats.apply(lambda r: round(r[1], 1))

    return df


def filtrer_avions_proches_aeroport(df: pd.DataFrame) -> pd.DataFrame:
    """Ne garde que les avions à moins de DISTANCE_MAX_KM d'un aéroport."""
    return df[df["distance_aeroport_km"] <= DISTANCE_MAX_KM].copy()


def main():
    fichiers_traites = sorted(PROCESSED_DIR.glob("states_*clean.csv"))
    if not fichiers_traites:
        raise FileNotFoundError(
            f"Aucun fichier trouvé dans {PROCESSED_DIR}. "
            "Lancez d'abord parse_opensky_states.py."
        )
    dernier_fichier = fichiers_traites[-1]

    print(f"Lecture de : {dernier_fichier}")
    df = pd.read_csv(dernier_fichier)

    df = enrichir_avec_aeroport(df)
    print(f"{len(df)} avions enrichis avec l'aéroport le plus proche")

    df_proches = filtrer_avions_proches_aeroport(df)
    print(f"{len(df_proches)} avions à moins de {DISTANCE_MAX_KM} km d'un aéroport français")

    output_path = PROCESSED_DIR / f"{dernier_fichier.stem}_avec_aeroport.csv"
    df_proches.to_csv(output_path, index=False)
    print(f"Sauvegardé dans : {output_path}")

    print("\nRépartition par aéroport :")
    print(df_proches["aeroport_proche"].value_counts())


if __name__ == "__main__":
    main()