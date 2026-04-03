def get_weather(destination: str):

    data = {
        "Bogota": "templado, 18°C",
        "Rio de Janeiro": "caluroso, 30°C",
        "Paris": "Fresco, 15°C",
        "Barcelona": "Soleado, 22°C",
        "Tokio": "Humedo, 27°C",
       # "Bali": "Tropical, 31°C",
        "Berlin": "Frío, 10°C"
    }

    # ===== VALIDACIÓN BÁSICA =====
    if not destination:
        return {
            "success": False,
            "error": "missing_destination",
            "data": None
        }

    # ===== NORMALIZACIÓN =====
    destination_clean = destination.strip().lower()

    # ===== MAPEO CASE-INSENSITIVE =====
    lookup = {k.lower(): k for k in data}

    if destination_clean not in lookup:
        return {
            "success": False,
            "error": "unknown_destination",
            "data": None,
            "input": destination
        }

    # ===== RECUPERAR CLAVE ORIGINAL =====
    real_key = lookup[destination_clean]

    return {
        "success": True,
        "data": {
            "destination": real_key,
            "weather": data[real_key]
        }
    }