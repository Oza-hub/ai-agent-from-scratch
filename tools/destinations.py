from services.destinations_service import get_destinations_service


def get_destinations(region: str):
    return get_destinations_service(region)