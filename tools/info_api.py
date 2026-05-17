import requests
import urllib.parse


def get_info_from_api(destination: str):

    print(f"[INFO API] fetching info for: {destination}")

    try:
        # ===== ENCODING =====
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

        extract = data.get("extract", "").strip()

        # ===== VALIDACIÓN: CONTENIDO VACÍO =====
        if not extract:
            return {
                "status": "error",
                "error": {
                    "type": "NO_CONTENT",
                    "message": "empty extract",
                    "retryable": True
                }
            }

        # ===== FILTRO DE DESAMBIGUACIÓN (CLAVE) =====
        bad_patterns = [
            "puede referirse a",
            "puede significar",
            "puede hacer referencia a",
            "en la mitología",
            "puede ser"
        ]

        extract_lower = extract.lower()

        if any(p in extract_lower for p in bad_patterns):
            return {
                "status": "error",
                "error": {
                    "type": "AMBIGUOUS_RESULT",
                    "message": "ambiguous wikipedia result",
                    "retryable": True
                }
            }

        # ===== RESPUESTA EXITOSA =====
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

    # ===== ERRORES DE RED =====
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