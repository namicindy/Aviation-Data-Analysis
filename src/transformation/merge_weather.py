"""
Fusion: ajoute la météo de l'aéroport à chaque avion, en se basant sur la
colonne aeroport_proche déjà calculée par enrich_with_airport.py.
"""

import json
import sys
from pathlib import Path

import pandas as pd

sys.path.append(str(Path(__file__).resolve().parent))
from aeroports_reference import AEROPORTS_FRANCE

PROJECT_ROOT = Path(__file__).resolve().parents[2]
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"
RAW_METEO_DIR = PROJECT_ROOT / "data" / "raw" / "meteo"


def trouver_dernier_fichier(dossier: Path, motif: str) -> Path:
    fichiers = sorted(dossier.glob(motif))
    if not fichiers:
        raise FileNotFoundError(f"Aucun fichier '{motif}' trouvé dans {dossier}.")
    return fichiers[-1]


def construire_table_meteo_par_aeroport(meteo_brute: list[dict]) -> pd.DataFrame:
    lignes = []
    for aeroport, reponse_meteo in zip(AEROPORTS_FRANCE, meteo_brute):
        courant = reponse_meteo.get("current", {})
        lignes.append({
            "aeroport_proche": aeroport["code_iata"],
            "temperature_c": courant.get("temperature_2m"),
            "vent_kmh": courant.get("wind_speed_10m"),
            "precipitation_mm": courant.get("precipitation"),
            "weather_code": courant.get("weather_code"),
        })

    return pd.DataFrame(lignes)


def main():
    fichier_positions = trouver_dernier_fichier(PROCESSED_DIR, "states_*avec_aeroport.csv")
    fichier_meteo = trouver_dernier_fichier(RAW_METEO_DIR, "meteo_*.json")

    print(f"Positions : {fichier_positions}")
    print(f"Météo : {fichier_meteo}")

    df_positions = pd.read_csv(fichier_positions)

    with open(fichier_meteo, "r", encoding="utf-8") as f:
        meteo_brute = json.load(f)

    df_meteo = construire_table_meteo_par_aeroport(meteo_brute)

    # On associe chaque ligne de df_positions à la
    # ligne de df_meteo qui a le même aeroport_proche.
    df_final = df_positions.merge(df_meteo, on="aeroport_proche", how="left")

    output_path = PROCESSED_DIR / f"{fichier_positions.stem}_avec_meteo.csv"
    df_final.to_csv(output_path, index=False)

    print(f"\n{len(df_final)} lignes sauvegardées dans : {output_path}")
    print("\nAperçu météo par aéroport :")
    print(df_final[["aeroport_proche", "temperature_c", "vent_kmh", "weather_code"]].drop_duplicates())


if __name__ == "__main__":
    main()