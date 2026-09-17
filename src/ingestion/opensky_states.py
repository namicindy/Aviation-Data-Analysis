"""
Ingestion Opensky States: récupération instantanée des avions détectés au-dessus de la France
et les stocke dans un fichier JSON brut.
"""

import requests
import json
from datetime import datetime, timezone
from pathlib import Path

# Bounding box approximative de la France métropolitaine
# (lamin, lomin, lamax, lomax) = (latitude_min, longitude_min, latitude_max, longitude_max)
# Pourquoi une bounding box approximative ? Parce que l'API OpenSky ne permet pas de filtrer par pays directement sur cet endpoint:
# elle raisonne en termes de coordonnées géographiques. Donc on prends une boite englobante qui couvre la France métropolitaine.
France_BBOX = {
    "lamin": 41.0,
    "lomin": -5.5,
    "lamax": 51.5,
    "lomax": 9.8,
}

RAW_DATA_DIR = Path(__file__).resolve().parents[2] / "data" / "raw" / "opensky_states"

def fetch_france_states() -> dict:
    """
    Interroge l'api Opensky pour récupérer les états (positions) des avions actuellement détectés
    dans la bounding box France.
    Retourne le JSON brut tel que renvoyé par l'API.
    """
    url = "https://opensky-network.org/api/states/all"
    params = {
        "lamin": France_BBOX["lamin"],
        "lomin": France_BBOX["lomin"],
        "lamax": France_BBOX["lamax"],
        "lomax": France_BBOX["lomax"],
    }

    # timeout=30: évite que le script reste bloqué indéfiniment si l'API ne réponds pas.
    response = requests.get(url,params=params, timeout=30)
    response.raise_for_status()  # lève une erreur claire si le code HTTP n'est pas 200

    return response.json()


def save_raw_snapshot(data:dict) -> Path:
    """
    Sauvegarde le JSON brut avec un nom de fichier horodaté, pour pouvoir accumuler plusieurs
    instantanés dans le temps sans écraser les précédents.
    """
    RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    output_path = RAW_DATA_DIR / f"states_{timestamp}.json"

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    return output_path


def main():
    print("Récupération des états/positions des avions au-dessus de la France...")
    data = fetch_france_states()

    n_aircraft = len(data.get("states", []))
    print(f"Nombre d'avions détectés: {n_aircraft}")

    output_path = save_raw_snapshot(data)
    print(f"Données brutes sauvegardées dans: {output_path}")


if __name__ == "__main__":
    main()