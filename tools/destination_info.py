def get_destination_info(destination: str):

    data = {
        "bogota": {
            "country": "Colombia",
            "language": "Spanish",
            "description": "Capital city, cultural and historical center"
        },
        "rio de janeiro": {
            "country": "Brazil",
            "language": "Portuguese",
            "description": "Famous for beaches and carnival"
        },
        "paris": {
            "country": "France",
            "language": "French",
            "description": "City of lights, art and culture"
        },
        "barcelona": {
            "country": "Spain",
            "language": "Spanish",
            "description": "Famous for architecture and beaches"
        },

        "berlin": {
             "country": "Germany",
            "language": "German",
            "description": "Capital of Germany, rich in history"
}
    }

    if not destination:
        return {
            "success": False,
            "error": "missing destination"
        }

    destination = destination.lower().strip()

    if destination not in data:
        return {
            "success": False,
            "error": f"unknown destination '{destination}'"
        }

    return {
        "success": True,
        "data": data[destination]
    }