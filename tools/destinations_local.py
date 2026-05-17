def get_local_destinations(region: str):

    data = {
        "europe": ["Paris", "Barcelona", "Berlin"],
        "asia": ["Tokio", "Bangkok", "Seoul"],
        "south america": ["Bogota", "Rio de Janeiro"]
    }

    region_clean = region.strip().lower()

    if region_clean not in data:
        return {
            "status": "error",
            "error": {
                "type": "unknown_region",
                "message": region,
                "retryable": False
            }
        }

    return {
        "status": "success",
        "data": {
            "region": region,
            "destinations": data[region_clean]
        },
        "meta": {
            "source": "local"
        }
    }