from agent.tool_executor import execute_tool

from core.normalizer import (
    normalize_destination,
    normalize_destinations_list,
    normalize_region
)


# =========================================================
# GOAL DETECTION
# =========================================================
def detect_goal(user_input: str):

    text = user_input.lower()

    has_destinations = "destino" in text or "destinos" in text
    has_weather = "clima" in text or "temperatura" in text
    has_info = (
        "info" in text
        or "informacion" in text
        or "información" in text
    )

    # ===== PRIORIDAD MULTI =====
    if has_destinations and has_weather and has_info:
        return "multi_destination_full"

    if has_destinations and has_weather:
        return "multi_destination_weather"

    if has_destinations and has_info:
        return "multi_destination_info"

    # ===== SINGLE =====
    if has_weather:
        return "single_destination_weather"

    if has_info:
        return "single_destination_info"

    if has_destinations:
        return "multi_destination"

    return "simple"


# =========================================================
# REGION EXTRACTION
# =========================================================
def extract_regions(user_input: str):

    text = user_input.lower()

    possible_regions = [
        "asia",
        "africa",
        "europa",
        "europe",
        "america",
        "américa",
        "latam",
        "sudamerica",
        "suramerica",
        "south america"
    ]

    regions = []

    for item in possible_regions:

        if item in text:

            normalized = normalize_region(item)

            if normalized not in regions:
                regions.append(normalized)

    return regions


# =========================================================
# PLAN CREATION
# =========================================================
def create_plan(goal: str, user_input: str):

    regions = extract_regions(user_input)

    print("[DEBUG] regions detected:", regions)

    text = user_input.lower()

    # =====================================================
    # SINGLE DESTINATION
    # =====================================================
    if goal in [
        "single_destination_weather",
        "single_destination_info"
    ]:

        words = text.split()

        city = words[-1] if words else None

        if not city:
            return None

        city_entity = normalize_destination(city)

        plan = []

        # ===== WEATHER =====
        if goal == "single_destination_weather":

            plan.append({
                "type": "tool",
                "tool": "get_weather",
                "args": {
                    "destination": city_entity["city"]
                },
                "save_as": "weather_single"
            })

        # ===== INFO =====
        elif goal == "single_destination_info":

            plan.append({
                "type": "tool",
                "tool": "get_destination_info",
                "args": {
                    "destination": city_entity["city"]
                },
                "save_as": "info_single"
            })

        return plan

    # =====================================================
    # MULTI DESTINATION
    # =====================================================
    if not regions:
        return None

    plan = []

    for region in regions:

        # ===== DESTINATIONS =====
        plan.append({
            "type": "tool",
            "tool": "get_destinations",
            "args": {
                "region": region
            },
            "save_as": f"destinations_{region}"
        })

        # ===== WEATHER =====
        if goal in [
            "multi_destination_weather",
            "multi_destination_full"
        ]:

            plan.append({
                "type": "map",
                "input": f"destinations_{region}",
                "tool": "get_weather",
                "arg_map": {
                    "destination": "item"
                },
                "save_as": f"weather_{region}"
            })

        # ===== INFO =====
        if goal in [
            "multi_destination_info",
            "multi_destination_full"
        ]:

            plan.append({
                "type": "map",
                "input": f"destinations_{region}",
                "tool": "get_destination_info",
                "arg_map": {
                    "destination": "item"
                },
                "save_as": f"info_{region}"
            })

    return plan


# =========================================================
# PLAN EXECUTION
# =========================================================
def execute_plan(plan):

    context = {}

    metrics = {
        "tool_calls": 0,
        "tool_errors": 0,
        "error_types": []
    }

    for step in plan:

        # =================================================
        # TOOL STEP
        # =================================================
        if step["type"] == "tool":

            metrics["tool_calls"] += 1

            result = execute_tool(
                step["tool"],
                step["args"]
            )

            # ===== ERROR =====
            if result["status"] == "error":

                metrics["tool_errors"] += 1

                metrics["error_types"].append(
                    result["error"]["type"]
                )

                continue

            data = result.get("data")

            # ===== NORMALIZE DESTINATIONS =====
            if (
                isinstance(data, dict)
                and "destinations" in data
            ):

                normalized = normalize_destinations_list(
                    data["destinations"]
                )

                context[step["save_as"]] = normalized

            else:
                context[step["save_as"]] = data

        # =================================================
        # MAP STEP
        # =================================================
        elif step["type"] == "map":

            input_data = context.get(
                step["input"],
                []
            )

            # ===== NORMALIZATION =====
            input_data = normalize_destinations_list(
                input_data
            )

            # ===== VALIDATION =====
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

            # =============================================
            # MAP ITERATION
            # =============================================
            for item in input_data:

                destination_value = item["city"]

                key = item["id"]

                args = {
                    k: (
                        destination_value
                        if v == "item"
                        else v
                    )
                    for k, v in step["arg_map"].items()
                }

                metrics["tool_calls"] += 1

                result = execute_tool(
                    step["tool"],
                    args
                )

                # ===== SUCCESS =====
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

                # ===== ERROR =====
                else:

                    metrics["tool_errors"] += 1

                    metrics["error_types"].append(
                        result["error"]["type"]
                    )

                    output[key] = {
                        "error": result["error"]
                    }

            context[step["save_as"]] = output

        # =================================================
        # UNKNOWN STEP
        # =================================================
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

    # =====================================================
    # FINAL NORMALIZATION
    # =====================================================
    final_weather = {}
    final_info = {}
    final_destinations = []

    for key, value in context.items():

        # ===== WEATHER =====
        if key.startswith("weather_"):

            if (
                isinstance(value, dict)
                and "destination" in value
                and "weather" in value
            ):

                normalized = normalize_destination(
                    value["destination"]
                )

                final_weather[
                    normalized["id"]
                ] = value["weather"]

            elif isinstance(value, dict):

                final_weather.update(value)

        # ===== INFO =====
        elif key.startswith("info_"):

            if (
                isinstance(value, dict)
                and "destination" in value
                and "info" in value
            ):

                normalized = normalize_destination(
                    value["destination"]
                )

                final_info[
                    normalized["id"]
                ] = value["info"]

            elif isinstance(value, dict):

                final_info.update(value)

        # ===== DESTINATIONS =====
        elif (
            key.startswith("destinations_")
            and isinstance(value, list)
        ):

            final_destinations.extend(value)

    # =====================================================
    # FINAL RESPONSE
    # =====================================================
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