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
        "tool_errors": 0
    }

    for step in plan:

        # ===== TOOL STEP =====
        if step["type"] == "tool":

            metrics["tool_calls"] += 1

            result = execute_tool(step["tool"], step["args"])

            if not result.get("success"):
                metrics["tool_errors"] += 1
                return {
                    "success": False,
                    "error": result.get("error", "tool_failed"),
                    "metrics": metrics
                }

            data = result.get("data")

            # 🔹 Simplificación SOLO para map posterior
            if step["tool"] == "get_destinations":
                data = data.get("destinations", [])

            context[step["save_as"]] = data

        # ===== MAP STEP =====
        elif step["type"] == "map":

            input_data = context.get(step["input"], [])

            if not isinstance(input_data, list):
                return {
                    "success": False,
                    "error": f"invalid_map_input: {step['input']}",
                    "metrics": metrics
                }

            output = {}

            for item in input_data:

                args = {
                    k: (item if v == "item" else v)
                    for k, v in step["arg_map"].items()
                }

                metrics["tool_calls"] += 1

                result = execute_tool(step["tool"], args)

                if result.get("success"):

                    data = result.get("data")

                    # 🔹 Normalización de salida
                    if isinstance(data, dict) and "weather" in data:
                        output[item] = data["weather"]
                    else:
                        output[item] = data

                else:
                    metrics["tool_errors"] += 1
                    output[item] = None

            context[step["save_as"]] = output

        else:
            return {
                "success": False,
                "error": f"unknown_step_type: {step['type']}",
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
        "success": True,
        "data": final_data,
        "metrics": metrics
    }