from services.info_service import get_info_service


def get_destination_info(destination: str):

    print(f"[INFO TOOL] processing: {destination}")

    return get_info_service(destination)