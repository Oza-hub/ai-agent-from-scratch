from tools.weather import get_weather
from tools.destinations import get_destinations
from tools.storage import save_to_file

tool_registry = {
    "get_destinations": {
        "function": get_destinations,
        "schema": {"region": "string"},
        "source": "local"
    },
    "get_weather": {
        "function": get_weather,
        "schema": {"destination": "string"},
        "source": "local"
    },
    "save_to_file": {
        "function": save_to_file,
        "schema": {
            "content": "string",
            "filename": "string(optional)"
        },
        "source": "local"
    }
}