# Architecture du projet — Pipeline de données aviation

## 1. Objectif business

**Question principale**
> Quels facteurs (météo, saison, aéroport, compagnie) expliquent le mieux les retards
> sur le trafic aérien commercial français, et peut-on les anticiper ?

**Questions secondaires**
1. Quels sont les 5 aéroports français avec le taux de retard le plus élevé, et cela
   varie-t-il selon la saison ?
2. Existe-t-il une corrélation mesurable entre conditions météo (vent, visibilité,
   précipitations) et retards ?
3. Quel est l'impact estimé en coût / passagers affectés pour une compagnie type si
   elle réduisait de 10% ses retards sur les aéroports les plus touchés ?

## 2. Sources de données

| Source | Donnée | Fréquence | Lien |
|---|---|---|---|
| OpenSky Network | Trafic aérien réel (ADS-B, positions, vols) | Temps réel + historique | opensky-network.org |
| DGAC / data.gouv.fr | Trafic commercial mensuel par aérodrome, émissions CO2 | Mensuelle/annuelle | data.gouv.fr |
| Open-Meteo | Météo par aéroport (vent, température, précipitations) | Horaire | open-meteo.com |

## 3. Modèle de données — schéma en étoile

Une table de faits (`vols`) au centre, entourée de 4 tables de dimension
(`compagnies`, `aeroports`, `dates`, `meteo`). 


### Table de faits `vols`
| Colonne | Description |
|---|---|
| vol_id | Identifiant unique du vol |
| date_id | Référence vers `dates` |
| compagnie_id | Référence vers `compagnies` |
| aeroport_depart_id | Référence vers `aeroports` |
| aeroport_arrivee_id | Référence vers `aeroports` |
| meteo_id | Référence vers `meteo` |
| retard_minutes | Mesure principale |
| distance_km | Distance du vol |
| nb_passagers_estime | Utilisé pour l'estimation d'impact |

### Dimension `dates`
| Colonne | Description |
|---|---|
| date_id | Identifiant |
| date_complete | Date brute |
| mois | Mois (1-12) |
| saison | Hiver / Printemps / Été / Automne |
| jour_semaine | Lundi...Dimanche |
| est_periode_vacances | Booléen |

### Dimension `aeroports`
| Colonne | Description |
|---|---|
| aeroport_id | Identifiant |
| code_iata | Code IATA (ex: CDG) |
| nom | Nom complet |
| ville | Ville |
| latitude / longitude | Coordonnées GPS |

### Dimension `compagnies`
| Colonne | Description |
|---|---|
| compagnie_id | Identifiant |
| code_icao | Code ICAO (3 lettres, ex: AFR): extrait du callsign Opensky |
| code_iata | Code IATA compagnie (2 caractères, ex: AF): connu pour les compagnies référencées |
| nom | Nom complet, ou "Inconnue/privé" si le code ICAO n'est pas reconnu |

### Dimension `meteo`
| Colonne | Description |
|---|---|
| meteo_id | Identifiant |
| aeroport_id | Référence vers `aeroports` |
| date_heure | Horodatage |
| temperature_c | En °C |
| vent_kmh | Vitesse du vent |
| precipitation_mm | Précipitations |
| weather_code | Code météo standardisé WMO (0 = ciel dégagé, 61-67 = pluie, 95+ = orage...) |


## 4. Stack technique

| Étape | Outil |
|---|---|
| Ingestion | Python (requests) + Airflow |
| Stockage | Google BigQuery (free tier) |
| Transformation | dbt |
| Analyse | Python (Pandas, scikit-learn) |
| Visualisation | Power BI Desktop / Streamlit |
