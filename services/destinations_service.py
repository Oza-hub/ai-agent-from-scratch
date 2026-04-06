from tools.destinations_local import get_local_destinations
from tools.destinations_api import get_destinations_from_api
from core.cache import get_cache, set_cache

def get_destinations_service(region):

    cache_key = f"destinations:{region}"

    cached = get_cache(cache_key)
    if cached:
        print("[CACHE] destinations hit")
        return cached

    # ===== 1. LOCAL =====
    local_result = get_local_destinations(region)

    if local_result.get("status") == "success":
        data = local_result.get("data", {}).get("destinations", [])

        if data:
            set_cache(cache_key, local_result)
            return local_result

    # ===== 2. FALLBACK API =====
    print("[DEST SERVICE] local miss → using API")

    api_result = get_destinations_from_api(region)

    if api_result.get("status") == "success":
        set_cache(cache_key, api_result)
    
    return api_result