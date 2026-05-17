# core/cache.py

import time

CACHE = {}
TTL = 300  # 5 minutos


def get_cache(key):
    entry = CACHE.get(key)

    if not entry:
        return None

    if time.time() > entry["expires"]:
        del CACHE[key]
        return None

    return entry["value"]


def set_cache(key, value, ttl=TTL):
    CACHE[key] = {
        "value": value,
        "expires": time.time() + ttl
    }