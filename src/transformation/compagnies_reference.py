"""
Référentiel de compagnies aériennes, indexé par code ICAO (3 lettres) —
c'est le code qui apparaît en préfixe dans le callsign OpenSky (ex: "AFR123").
"""

COMPAGNIES = {
    "AFR": {"code_iata": "AF", "nom": "Air France"},
    "TVF": {"code_iata": "TO", "nom": "Transavia France"},
    "EZY": {"code_iata": "U2", "nom": "easyJet"},
    "RYR": {"code_iata": "FR", "nom": "Ryanair"},
    "VLG": {"code_iata": "VY", "nom": "Vueling"},
    "WZZ": {"code_iata": "W6", "nom": "Wizz Air"},
    "BAW": {"code_iata": "BA", "nom": "British Airways"},
    "DLH": {"code_iata": "LH", "nom": "Lufthansa"},
    "KLM": {"code_iata": "KL", "nom": "KLM"},
    "IBE": {"code_iata": "IB", "nom": "Iberia"},
    "SWR": {"code_iata": "LX", "nom": "Swiss International Air Lines"},
    "BEL": {"code_iata": "SN", "nom": "Brussels Airlines"},
    "TAP": {"code_iata": "TP", "nom": "TAP Air Portugal"},
    "THY": {"code_iata": "TK", "nom": "Turkish Airlines"},
    "UAE": {"code_iata": "EK", "nom": "Emirates"},
    "QTR": {"code_iata": "QR", "nom": "Qatar Airways"},
    "DAL": {"code_iata": "DL", "nom": "Delta Air Lines"},
    "UAL": {"code_iata": "UA", "nom": "United Airlines"},
    "ACA": {"code_iata": "AC", "nom": "Air Canada"},
    "FDX": {"code_iata": "FX", "nom": "FedEx Express (cargo)"},
    "UPS": {"code_iata": "5X", "nom": "UPS Airlines (cargo)"},
    # Ajoutées après analyse des codes "Inconnue" les plus fréquents dans
    # les vraies données OpenSky
    "EJU": {"code_iata": "EC", "nom": "easyJet Europe"},
    "EZS": {"code_iata": "DS", "nom": "easyJet Switzerland"},
    "AEA": {"code_iata": "UX", "nom": "Air Europa"},
    "EWG": {"code_iata": "EW", "nom": "Eurowings"},
    "CCM": {"code_iata": "XK", "nom": "Air Corsica"},
    "VOE": {"code_iata": "V7", "nom": "Volotea"},
    "DAH": {"code_iata": "AH", "nom": "Air Algérie"},
    "TRA": {"code_iata": "HV", "nom": "Transavia (Pays-Bas)"},
    "SAS": {"code_iata": "SK", "nom": "SAS Scandinavian Airlines"},
    "WMT": {"code_iata": "W9", "nom": "Wizz Air Malta"},
    "JAF": {"code_iata": "TB", "nom": "TUI Airlines Belgium"},
    "TOM": {"code_iata": "BY", "nom": "TUI Airways"},
    "ENT": {"code_iata": "E4", "nom": "Enter Air"},
    "FIN": {"code_iata": "AY", "nom": "Finnair"},
    "EXS": {"code_iata": "LS", "nom": "Jet2.com"},
    "LGL": {"code_iata": "LG", "nom": "Luxair"},
    "BTI": {"code_iata": "BT", "nom": "airBaltic"},
    # Aviation d'affaires (jets privés) : pas de code IATA, mais des codes
    # ICAO connus et fréquents dans le ciel français (Nice/Cannes notamment).
    "NJE": {"code_iata": None, "nom": "NetJets (aviation d'affaires)"},
    "VJT": {"code_iata": None, "nom": "VistaJet (aviation d'affaires)"},
}


def identifier_compagnie(callsign: str) -> dict:
    """
    À partir du callsign, retourne les infos de la
    compagnie si son préfixe ICAO (3 premières lettres) est reconnu.

    Retourne toujours un dictionnaire avec les mêmes clés, même si la
    compagnie n'est pas reconnue (ex: vols privés, militaires, 
    ou compagnies étrangères non listées).   
    """
    if not isinstance(callsign, str) or len(callsign) < 3:
        return {"code_icao": None, "code_iata": None, "nom": "Inconnue / privé"}
 
    prefixe = callsign[:3].upper()
    compagnie = COMPAGNIES.get(prefixe)
 
    if compagnie is None:
        return {"code_icao": prefixe, "code_iata": None, "nom": "Inconnue / privé"}
 
    return {"code_icao": prefixe, "code_iata": compagnie["code_iata"], "nom": compagnie["nom"]}