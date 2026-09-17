"""
Ajoute le nom de la compagnie aérienne, déduit du callsign,
au tableau déjà enrichi (aéroport + météo).
"""

from pathlib import Path

import pandas as pd

from compagnies_reference import identifier_compagnie

PROJECT_ROOT = Path(__file__).resolve().parents[2]
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"


def trouver_dernier_fichier(dossier: Path, motif: str) -> Path:
    fichiers = sorted(dossier.glob(motif))
    if not fichiers:
        raise FileNotFoundError(f"Aucun fichier '{motif}' trouvé dans {dossier}.")
    return fichiers[-1]


def enrichir_avec_compagnie(df: pd.DataFrame) -> pd.DataFrame:
    """
    Applique identifier_compagnie() à chaque callsign du tableau, et
    éclate le dictionnaire résultat en 3 colonnes séparées.
    """
    df = df.copy()
    resultats = df["callsign"].apply(identifier_compagnie)
    colonnes_compagnie = pd.DataFrame(resultats.tolist(), index=df.index)
    return pd.concat([df, colonnes_compagnie], axis=1)


def main():
    fichier = trouver_dernier_fichier(PROCESSED_DIR, "states_*avec_meteo.csv")
    print(f"Lecture de : {fichier}")

    df = pd.read_csv(fichier)
    df = enrichir_avec_compagnie(df)

    n_reconnues = (df["nom"] != "Inconnue / privé").sum()
    print(f"{n_reconnues} / {len(df)} compagnies reconnues")

    output_path = PROCESSED_DIR / f"{fichier.stem}_avec_compagnie.csv"
    df.to_csv(output_path, index=False)
    print(f"Sauvegardé dans : {output_path}")

    print("\nRépartition par compagnie :")
    print(df["nom"].value_counts())


if __name__ == "__main__":
    main()