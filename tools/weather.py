import os
import requests
from dotenv import load_dotenv


load_dotenv()

API_KEY = os.getenv("OPENWEATHER_API_KEY")

print(f"[DEBUG] API KEY LOADED: {API_KEY[:5]}..." if API_KEY else "[DEBUG] API KEY LOADED: None")


# ===== HELPERS =====
def build_success(data):
    return {
        "status": "success",
        "data": data,
        "meta": {
            "source": "openweather"
        }
    }


def build_error(error_type, message, code=None, retryable=False):
    return {
        "status": "error",
        "error": {
            "type": error_type,
            "message": message,
            "code": code,
            "retryable": retryable
        },
        "meta": {
            "source": "openweather"
        }
    }


# ===== MAIN TOOL =====
def get_weather(destination: str):

    print(f"[WEATHER API] calling real API for: {destination}")

    # ===== VALIDACIÓN =====
    if not destination:
        return build_error("INPUT_ERROR", "missing destination")

    if not API_KEY:
        return build_error("CONFIG_ERROR", "missing_api_key")

    try:
        url = "https://api.openweathermap.org/data/2.5/weather"

        params = {
            "q": destination,
            "appid": API_KEY,
            "units": "metric",
            "lang": "es"
        }

        response = requests.get(url, params=params, timeout=5)

        # ===== ERRORES HTTP =====
        if response.status_code != 200:

            if response.status_code == 404:
                return build_error(
                    "HTTP_ERROR",
                    "city not found",
                    404,
                    retryable=False
                )

            if response.status_code == 401:
                return build_error(
                    "AUTH_ERROR",
                    "invalid api key",
                    401,
                    retryable=False
                )

            if response.status_code == 429:
                return build_error(
                    "RATE_LIMIT",
                    "rate limit exceeded",
                    429,
                    retryable=True
                )

            if response.status_code >= 500:
                return build_error(
                    "SERVER_ERROR",
                    "provider failure",
                    response.status_code,
                    retryable=True
                )

            return build_error(
                "HTTP_ERROR",
                f"unexpected status {response.status_code}",
                response.status_code,
                retryable=False
            )

        data = response.json()

        # ===== VALIDACIÓN DE DATOS =====
        try:
            weather_desc = data["weather"][0]["description"]
            temp = data["main"]["temp"]
        except Exception:
            return build_error(
                "DATA_ERROR",
                "invalid response structure",
                retryable=False
            )

        return build_success({
            "destination": destination,
            "weather": f"{weather_desc}, {temp}°C"
        })

    # ===== ERRORES DE RED =====
    except requests.exceptions.Timeout:
        return build_error("NETWORK_ERROR", "timeout", retryable=True)

    except requests.exceptions.ConnectionError:
        return build_error("NETWORK_ERROR", "connection_error", retryable=True)

    except Exception as e:
        return build_error("UNKNOWN_ERROR", str(e), retryable=False)