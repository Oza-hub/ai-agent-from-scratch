def get_destinations(region: str = None):

    data = {
        "south america": ["bogota", "rio de janeiro"],
        "europe": ["paris", "barcelona", "berlin"],
        "asia": ["tokio", "bali"]
    }

    aliases = {
        "sur america": "south america",
        "sudamerica": "south america",
        "europa": "europe"
    }

    # ===== VALIDACIÓN =====
    if not region:
        return {
            "success": False,
            "error": "missing_region",
            "data": None
        }

    # ===== NORMALIZACIÓN =====
    region_clean = region.lower().strip()
    region_clean = aliases.get(region_clean, region_clean)

    if region_clean not in data:
        return {
            "success": False,
            "error": "unknown_region",
            "data": None,
            "input": region
        }

    # ===== FORMATEO =====
    formatted = [d.title() for d in data[region_clean]]

    return {
        "success": True,
        "data": {
            "region": region_clean,
            "destinations": formatted
        }
    }