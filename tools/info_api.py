import requests
import urllib.parse


def get_info_from_api(destination: str):

    print(f"[INFO API] fetching info for: {destination}")

    try:
        # FIX: encoding obligatorio
        encoded = urllib.parse.quote(destination)

        url = f"https://es.wikipedia.org/api/rest_v1/page/summary/{encoded}"

        headers = {
                "User-Agent": "AI-Agent/1.0 (learning project)",
                "Accept": "application/json"
            }

        response = requests.get(url, headers=headers, timeout=5)

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

        extract = data.get("extract")

        # VALIDACIÓN REAL
        if not extract or len(extract.strip()) == 0:
            return {
                "status": "error",
                "error": {
                    "type": "NO_CONTENT",
                    "message": "empty extract",
                    "retryable": True
                }
            }

        return {
            "status": "success",
            "data": {
                "destination": destination,
                "info": extract
            },
            "meta": {
                "source": "wikipedia"
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