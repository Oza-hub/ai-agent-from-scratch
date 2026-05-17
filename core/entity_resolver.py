KNOWN_DESTINATIONS = {
    "paris": "Paris",
    "tokio": "Tokyo",
    "berlin": "Berlin",
    "rio": "Rio de Janeiro",
    "bogota": "Bogotá"
}


def resolve_destination(name: str) -> str:

    if not name:
        return name

    clean = name.lower().strip()

    return KNOWN_DESTINATIONS.get(clean, name)