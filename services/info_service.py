from tools.info_api import get_info_from_api
from core.cache import get_cache, set_cache


def get_info_service(destination):

    cache_key = f"info:{destination.lower()}"

    cached = get_cache(cache_key)
    if cached:
        print("[CACHE] info hit")
        return cached

    result = get_info_from_api(destination)

    if result.get("status") == "success":
        set_cache(cache_key, result)
        return result

    return result  # IMPORTANTE: NO None