import json
from agent.tool_executor import execute_tool


# ===== GOAL DETECTION =====
def detect_goal(user_input: str):

    text = user_input.lower()

    has_destinations = "destino" in text or "destinos" in text
    has_weather = "clima" in text or "temperatura" in text
    has_info = "info" in text or "informacion" in text or "información" in text

    if has_destinations and has_weather and has_info:
        return "multi_destination_full"

    if has_destinations and has_weather:
        return "multi_destination_weather"

    if has_destinations and has_info:
        return "multi_destination_info"

    return "simple"


# ===== REGION EXTRACTION =====
def extract_regions(user_input: str):

    text = user_input.lower()
    words = set(text.split())

    regions = []

    if "asia" in words:
        regions.append("asia")

    if "africa" in words or "áfrica" in words:
        regions.append("africa")

    if "europa" in words or "europe" in words:
        regions.append("europe")

    if (
        "america" in words
        or "américa" in words
        or "latam" in words
        or "sudamerica" in words
        or "suramerica" in words
        or "south america" in text
    ):
        regions.append("south america")

    return regions


# ===== PLAN CREATION =====
def create_plan(goal: str, user_input: str):

    regions = extract_regions(user_input)
    print("[DEBUG] regions detected:", regions)

    if not regions:
        return None

    plan = []

    for region in regions:

        # ===== DESTINATIONS =====
        plan.append({
            "type": "tool",
            "tool": "get_destinations",
            "args": {"region": region},
            "save_as": f"destinations_{region}"
        })

        # ===== WEATHER =====
        if goal in ["multi_destination_weather", "multi_destination_full"]:
            plan.append({
                "type": "map",
                "input": f"destinations_{region}",
                "tool": "get_weather",
                "arg_map": {"destination": "item"},
                "save_as": f"weather_{region}"
            })

        # ===== INFO =====
        if goal in ["multi_destination_info", "multi_destination_full"]:
            plan.append({
                "type": "map",
                "input": f"destinations_{region}",
                "tool": "get_destination_info",
                "arg_map": {"destination": "item"},
                "save_as": f"info_{region}"
            })

    return plan


# ===== PLAN EXECUTION =====
def execute_plan(plan):

    context = {}

    metrics = {
        "tool_calls": 0,
        "tool_errors": 0,
        "error_types": []
    }

    for step in plan:

        # ===== TOOL STEP =====
        if step["type"] == "tool":

            metrics["tool_calls"] += 1

            result = execute_tool(step["tool"], step["args"])

            if result["status"] == "error":

                metrics["tool_errors"] += 1
                metrics["error_types"].append(result["error"]["type"])

                return {
                    "status": "error",
                    "error": result["error"],
                    "metrics": metrics
                }

            data = result.get("data")

            if step["tool"] == "get_destinations":
                data = data.get("destinations", [])

            context[step["save_as"]] = data

        # ===== MAP STEP =====
        elif step["type"] == "map":

            input_data = context.get(step["input"], [])

            if not isinstance(input_data, list):
                return {
                    "status": "error",
                    "error": {
                        "type": "invalid_map_input",
                        "message": step["input"],
                        "retryable": False
                    },
                    "metrics": metrics
                }

            output = {}

            for item in input_data:

                # FIX 1: obtener ciudad correctamente
                if isinstance(item, dict) and "city" in item:
                    destination_value = item["city"]
                    key = item.get("name") or item["city"]
                else:
                    destination_value = item
                    key = item

                args = {
                    k: (destination_value if v == "item" else v)
                    for k, v in step["arg_map"].items()
                }

                metrics["tool_calls"] += 1

                result = execute_tool(step["tool"], args)

                if result["status"] == "success":

                    data = result.get("data")

                    if isinstance(data, dict):

                        if "weather" in data:
                            output[key] = data["weather"]

                        elif "info" in data:
                            output[key] = data["info"]

                        else:
                            output[key] = data

                    else:
                        output[key] = data

                else:
                    metrics["tool_errors"] += 1
                    metrics["error_types"].append(result["error"]["type"])

                    output[key] = {
                        "error": result["error"]
                    }

            context[step["save_as"]] = output

        else:
            return {
                "status": "error",
                "error": {
                    "type": "unknown_step_type",
                    "message": step["type"],
                    "retryable": False
                },
                "metrics": metrics
            }

    # ===== NORMALIZATION FINAL =====
    final_weather = {}
    final_info = {}
    final_destinations = []

    for key, value in context.items():

        if key.startswith("weather_") and isinstance(value, dict):
            final_weather.update(value)

        elif key.startswith("info_") and isinstance(value, dict):
            final_info.update(value)

        elif key.startswith("destinations_") and isinstance(value, list):
            final_destinations.extend(value)

    final_data = {}

    if final_destinations:
        final_data["destinations"] = final_destinations

    if final_weather:
        final_data["weather"] = final_weather

    if final_info:
        final_data["info"] = final_info

    return {
        "status": "success",
        "data": final_data,
        "metrics": metrics
    }