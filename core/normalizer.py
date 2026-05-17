# core/normalizer.py

import unicodedata


# =========================================================
# CANONICAL DESTINATIONS
# =========================================================

DESTINATION_ALIASES = {

    # ===== EUROPE =====
    "paris": "paris",
    "paris france": "paris",

    "barcelona": "barcelona",

    "berlin": "berlin",

    "madrid": "madrid",

    "rome": "rome",
    "roma": "rome",

    "london": "london",
    "londres": "london",

    # ===== ASIA =====
    "tokio": "tokyo",
    "tokyo": "tokyo",

    "bangkok": "bangkok",

    "seoul": "seoul",
    "seul": "seoul",

    "bali": "bali",

    # ===== SOUTH AMERICA =====
    "bogota": "bogota",
    "bogotá": "bogota",

    "rio": "rio_de_janeiro",
    "rio de janeiro": "rio_de_janeiro"
}


# =========================================================
# DISPLAY NAMES
# =========================================================

DISPLAY_NAMES = {

    "paris": "Paris",
    "barcelona": "Barcelona",
    "berlin": "Berlin",
    "madrid": "Madrid",
    "rome": "Rome",
    "london": "London",

    "tokyo": "Tokyo",
    "bangkok": "Bangkok",
    "seoul": "Seoul",
    "bali": "Bali",

    "bogota": "Bogota",
    "rio_de_janeiro": "Rio de Janeiro"
}


# =========================================================
# REGIONS
# =========================================================

REGION_ALIASES = {

    "europa": "europe",
    "europe": "europe",

    "asia": "asia",

    "sudamerica": "south america",
    "suramerica": "south america",
    "south america": "south america",
    "latam": "south america",
    "america": "south america",
    "américa": "south america",

}


# =========================================================
# HELPERS
# =========================================================

def clean_text(text: str) -> str:

    if not isinstance(text, str):
        return ""

    text = text.strip().lower()

    # remover acentos
    text = unicodedata.normalize("NFD", text)
    text = text.encode("ascii", "ignore").decode("utf-8")

    return text


# =========================================================
# CANONICAL ID
# =========================================================

def canonical_id(name: str) -> str:

    clean = clean_text(name)

    return DESTINATION_ALIASES.get(clean, clean)


# =========================================================
# NORMALIZE DESTINATION
# =========================================================

def normalize_destination(destination):

    # =====================================================
    # STRING INPUT
    # =====================================================
    if isinstance(destination, str):

        canonical = canonical_id(destination)

        return {
            "id": canonical,
            "name": DISPLAY_NAMES.get(
                canonical,
                destination.title()
            ),
            "city": DISPLAY_NAMES.get(
                canonical,
                destination.title()
            )
        }

    # =====================================================
    # DICT INPUT
    # =====================================================
    if isinstance(destination, dict):

        raw_name = (
            destination.get("city")
            or destination.get("name")
            or ""
        )

        canonical = canonical_id(raw_name)

        return {
            "id": canonical,

            "name": destination.get(
                "name",
                DISPLAY_NAMES.get(canonical, raw_name.title())
            ),

            "city": destination.get(
                "city",
                DISPLAY_NAMES.get(canonical, raw_name.title())
            )
        }

    # =====================================================
    # INVALID
    # =====================================================
    return {
        "id": "unknown",
        "name": "Unknown",
        "city": "Unknown"
    }


# =========================================================
# NORMALIZE DESTINATIONS LIST
# =========================================================

def normalize_destinations_list(destinations):

    if not isinstance(destinations, list):
        return []

    normalized = []

    seen = set()

    for item in destinations:

        entity = normalize_destination(item)

        entity_id = entity["id"]

        # evitar duplicados
        if entity_id in seen:
            continue

        seen.add(entity_id)

        normalized.append(entity)

    return normalized


# =========================================================
# NORMALIZE REGION
# =========================================================

def normalize_region(region: str):

    clean = clean_text(region)

    return REGION_ALIASES.get(clean, clean)
