"""
Ingestion météo: on récupère la météo actuelle pour tous les aéroports de
référence en UN SEUL appel à l'API Open-Meteo (batch par coordonnées). 
"""

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

import requests

# Importation du référentiel d'aéroports déjà créé, pour ne pas dupliquer
# les coordonnées à un autre endroit.
sys.path.append(str(Path(__file__).resolve().parents[1] / "transformation"))
from aeroports_reference import AEROPORTS_FRANCE

PROJECT_ROOT = Path(__file__).resolve().parents[2]
RAW_METEO_DIR = PROJECT_ROOT / "data" / "raw" / "meteo"

# Les variables météo qu'on demande à l'API. On reste sur celles disponibles
# dans l'endpoint "current" 
VARIABLES_METEO = "temperature_2m,wind_speed_10m,precipitation,weather_code"


def fetch_meteo_tous_aeroports() -> list[dict]:
    """
    Appelle l'API Open-Meteo une seule fois avec les coordonnées de tous
    les aéroports, séparées par des virgules.

    Retourne une liste de réponses météo, DANS LE MÊME ORDRE que
    AEROPORTS_FRANCE.
    """
    url = "https://api.open-meteo.com/v1/forecast"

    latitudes = ",".join(str(a["latitude"]) for a in AEROPORTS_FRANCE)
    longitudes = ",".join(str(a["longitude"]) for a in AEROPORTS_FRANCE)

    params = {
        "latitude": latitudes,
        "longitude": longitudes,
        "current": VARIABLES_METEO,
    }

    response = requests.get(url, params=params, timeout=30)
    response.raise_for_status()
    data = response.json()

    # Si une seule coordonnée était demandée, l'API renverrait un objet
    # unique plutôt qu'une liste. On s'assure donc que la sortie est toujours une liste, même si
    # un seul aéroport est demandé (pour éviter des erreurs de type dans le reste du code).
    if isinstance(data, dict):
        data = [data]

    return data


def save_raw_meteo(data: list[dict]) -> Path:
    RAW_METEO_DIR.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    output_path = RAW_METEO_DIR / f"meteo_{timestamp}.json"

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    return output_path


def main():
    print(f"Récupération météo pour {len(AEROPORTS_FRANCE)} aéroports (1 seul appel API)...")
    data = fetch_meteo_tous_aeroports()

    print(f"{len(data)} réponses reçues.")

    output_path = save_raw_meteo(data)
    print(f"Données brutes sauvegardées dans : {output_path}")


if __name__ == "__main__":
    main()