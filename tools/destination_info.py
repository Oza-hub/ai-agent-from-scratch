from services.info_service import get_info_service
from core.entity_resolver import resolve_destination


def get_destination_info(destination: str):
    
    print("=== DEBUG DESTINATION INFO ===")
    print("INPUT:", destination)

    resolved = resolve_destination(destination)

    print("RESOLVED:", resolved)

    # ===== MAPA A ESPAÑOL (CLAVE) =====
    translation_map = {
        "Tokyo": "Tokio",
        "Paris": "Paris",
        "Rio de Janeiro": "Rio de Janeiro",
        "Berlin": "Berlin",
        "Bogotá": "Bogotá"
    }

    resolved_es = translation_map.get(resolved, resolved)

    print("RESOLVED_ES:", resolved_es)

    # ===== INTENTO BASE =====
    result = get_info_service(resolved_es)

    if result.get("status") == "success":
        return result

    error = result.get("error", {})

    # ===== RETRY DESAMBIGUACIÓN =====
    if error.get("type") == "AMBIGUOUS_RESULT":

        print("[RETRY] estrategia wikipedia (ciudad)")

        refined = f"{resolved_es} (ciudad)"
        print("TRY:", refined)

        retry_result = get_info_service(refined)

        if retry_result.get("status") == "success":
            return retry_result

    return result