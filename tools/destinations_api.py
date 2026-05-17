import requests


def get_destinations_from_api(region: str):

    print(f"[DEST API] calling external API for region: {region}")

    try:
        # ajuste: REST Countries usa "americas"
        if region in ["north america", "south america"]:
            region_api = "americas"
        else:
            region_api = region

        url = f"https://restcountries.com/v3.1/region/{region_api}"

        response = requests.get(url, timeout=5)

        if response.status_code != 200:
            return {
                "status": "error",
                "error": {
                    "type": "HTTP_ERROR",
                    "message": f"status {response.status_code}",
                    "retryable": True
                }
            }

        data = response.json()

        # CAMBIO CLAVE: usar capitales como ciudades
        destinations = []

        for item in data[:5]:
            name = item.get("name", {}).get("common")
            capital = item.get("capital", [None])[0]

            if name and capital:
                destinations.append({
                    "name": name,
                    "city": capital
                })

        # fallback si ninguna capital válida
        if not destinations:
            return {
                "status": "error",
                "error": {
                    "type": "NO_VALID_DESTINATIONS",
                    "message": "no countries with capital found",
                    "retryable": True
                }
            }

        return {
            "status": "success",
            "data": {
                "region": region,
                "destinations": destinations
            },
            "meta": {
                "source": "restcountries"
            }
        }

    except requests.exceptions.Timeout:
        return {
            "status": "error",
            "error": {
                "type": "NETWORK_ERROR",
                "message": "timeout",
                "retryable": True
            }
        }

    except Exception as e:
        return {
            "status": "error",
            "error": {
                "type": "UNKNOWN_ERROR",
                "message": str(e),
                "retryable": False
            }
        }