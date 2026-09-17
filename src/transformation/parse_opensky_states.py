"""
Transformation: lit le dernier instantané brut Opensky (JSON) et le transforme en tableau structuré
(colonnes nommées), sauvegardé dans un fichier CSV.
"""

import json
from pathlib import Path

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[2]
RAW_STATES_DIR = PROJECT_ROOT / "data" / "raw" / "opensky_states"
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"

# Ordre officiel des champs d'un "state vector" Opensky, tel que documenté dans l'API:
STATE_VECTOR_COLUMNS = [
    "icao24",  # identifiant unique de l'avion (hexadécimal)
    "callsign",  # indicatif de l'avion (peut être vide)
    "origin_country",  # pays d'origine de l'avion (selon la base de données ICAO)
    "time_position",  # timestamp de la dernière position connue (en secondes depuis l'époque Unix)
    "last_contact",  # timestamp du dernier contact avec l'avion (en secondes depuis l'époque Unix)
    "longitude",  # longitude de l'avion (en degrés décimaux)
    "latitude",  # latitude de l'avion (en degrés décimaux)
    "baro_altitude",  # altitude barométrique de l'avion (en mètres)
    "on_ground",  # True si l'avion est au sol, False sinon
    "velocity",  # vitesse de l'avion (en m/s)
    "true_track",  # cap vrai de l'avion (en degrés)
    "vertical_rate",  # taux de montée/descente de l'avion (en m/s)
    "sensors",  # identifiants des capteurs ayant détecté l'avion (peut être vide)
    "geo_altitude",  # altitude géométrique de l'avion (en mètres)
    "squawk",  # code transpondeur de l'avion (peut être vide)
    "spi",  # True si l'avion est en mode "special position indicator",
    "position_source",  # source de la position (0=ADS-B, 1=ASTERIX, 2=MLAT)
]


def find_latest_raw_file() -> Path:
    """
    Retorune le fichier JSON le plus récent dans data/raw/opensky_states/.
    """
    fichiers = sorted(RAW_STATES_DIR.glob("states_*.json"))
    if not fichiers:
        raise FileNotFoundError(
            f"Aucun fichier JSON trouvé dans {RAW_STATES_DIR}. "
            "Lancez d'abord src/ingestion/opensky_states.py."
        )
    return fichiers[-1] # le dernier fichier après tri est le plus récent


def raw_json_to_dataframe(raw_data: dict) -> pd.DataFrame:
    """
    Convertit le JSON brut Opensky en Dataframe pandas avec colonnes nommées.
    """
    states = raw_data.get("states") or []

    # Chaque élément de "states" est une liste positionnelle.
    # On ne garde que les 17 premiers champs documentés: certains avions peuvent renvoyer
    # un champs supplémentaire ("catégory") qu'on ignore ici.
    lignes = [state[: len(STATE_VECTOR_COLUMNS)] for state in states]

    df = pd.DataFrame(lignes, columns=STATE_VECTOR_COLUMNS)
    return df


def clean_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """
    Nettoyage minimal mais justifié:
    - on enlève les avions sans position connue (longitude/latitude manquantes) car ils ne servent
    à rien  pour nos questions business (impossible de savoir  de quel aéroport ils viennent).
    - on enlève les espaces parasitesautour des indicateurs d'appel (callsign), un défaut connu
    et documenté de l'API Opensky.
    """
    df = df.dropna(subset=["longitude", "latitude"]).copy()
    df["callsign"] = df["callsign"].str.strip()
    return df


def main():
    latest_file = find_latest_raw_file()
    print(f"Lecture du fichier : {latest_file}")

    with open(latest_file, "r", encoding="utf-8") as f:
        raw_data = json.load(f)

    df = raw_json_to_dataframe(raw_data)
    print(f"{len(df)} avions avant nettoyage")

    df = clean_dataframe(df)
    print(f"{len(df)} avions après nettoyage (positions valides)")

    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    output_path = PROCESSED_DIR / f"{latest_file.stem}.clean.csv"
    df.to_csv(output_path, index=False)

    print(f"Tableau structuré sauvegardédans : {output_path}")
    print("nApperçu : ")
    print(df.head())


if __name__ == "__main__":
    main()