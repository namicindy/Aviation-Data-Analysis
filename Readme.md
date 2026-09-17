# Pipeline de données aviation — France

Projet portfolio : pipeline de données de bout en bout (ingestion → stockage →
transformation → analyse → visualisation) sur le trafic aérien commercial français,
pour identifier les facteurs qui expliquent les retards et estimer leur impact
business.

> Documentation complète de l'architecture et des choix techniques : [docs/architecture.md](docs/architecture.md)

## Question traitée

Quels facteurs (météo, saison, aéroport, compagnie) expliquent le mieux les retards
sur le trafic aérien commercial français, et peut-on les anticiper ?

## Statut du projet

En cours — voir [docs/architecture.md](docs/architecture.md#5-statut) pour l'avancement détaillé.

## Structure du repo

```
├── docs/              Documentation (architecture, décisions techniques)
├── src/
│   ├── ingestion/      Scripts de collecte des données (OpenSky, DGAC, Open-Meteo)
│   ├── transformation/ Nettoyage et modélisation des données
│   └── analysis/       Analyses et modèles
├── notebooks/          Exploration (Jupyter) 
└── data/                Données brutes et traitées (non versionnées dans git)
```

## Sources de données

- [OpenSky Network](https://opensky-network.org) — trafic aérien réel
- [DGAC / data.gouv.fr](https://www.data.gouv.fr/organizations/direction-generale-de-laviation-civile/datasets) — statistiques officielles
- [Open-Meteo](https://open-meteo.com) — données météo