# ==============================
# DATA CONTROLADA
# ==============================

VALID_DESTINATIONS = {
    "paris",
    "rome",
    "berlin",
    "rio de janeiro"
}

VALID_REGIONS = {
    "south america",
    "europe"
}


# ==============================
# NORMALIZACIÓN
# ==============================

def normalize_args(name, args):

    # -------- REGION --------
    if name == "get_destinations" and "region" in args:
        region = args["region"].lower().strip()

        aliases = {
            "southamerica": "south america",
            "sudamerica": "south america",
            "latam": "south america",
            "south-america": "south america",
            "america_south": "south america"
        }

        args["region"] = aliases.get(region, region)

    # -------- DESTINATION --------
    if "destination" in args and isinstance(args["destination"], str):
        dest = args["destination"].lower().strip()

        aliases = {
            "rio": "rio de janeiro",
            "paris france": "paris"
        }

        args["destination"] = aliases.get(dest, dest)

    return args


# ==============================
# VALIDACIÓN
# ==============================

def validate_tool_call(name, args):

    # ===== TOOL NAME =====
    if not name:
        return False, "tool name missing"

    # ===== VALIDACIÓN POR TOOL =====

    # --------------------------
    # get_destinations
    # --------------------------
    if name == "get_destinations":

        region = args.get("region")

        if not region:
            return False, "Missing parameter: region"

        if not isinstance(region, str) or not region.strip():
            return False, "Invalid region"

        if region not in VALID_REGIONS:
            return False, {
                "error": "Invalid region",
                "received": region,
                "allowed": list(VALID_REGIONS)
            }

    # --------------------------
    # get_weather
    # --------------------------
    elif name == "get_weather":

        dest = args.get("destination")

        if not dest:
            return False, "Missing parameter: destination"

        if not isinstance(dest, str) or not dest.strip():
            return False, "Invalid destination"

        if dest not in VALID_DESTINATIONS:
            return False, {
                "error": "Invalid destination",
                "received": dest,
                "allowed": list(VALID_DESTINATIONS)
            }

    # --------------------------
    # get_destination_info
    # --------------------------
    elif name == "get_destination_info":

        dest = args.get("destination")

        if not dest:
            return False, "Missing parameter: destination"

        if not isinstance(dest, str) or not dest.strip():
            return False, "Invalid destination"

        if dest not in VALID_DESTINATIONS:
            return False, {
                "error": "Invalid destination",
                "received": dest
            }

    else:
        return False, f"Tool '{name}' not allowed"

    # ===== VALIDACIÓN DE INPUT SOSPECHOSO =====
    suspicious_patterns = [";", "DROP", "SELECT", "--"]

    for value in args.values():
        if any(p in str(value).upper() for p in suspicious_patterns):
            return False, "suspicious input detected"

    return True, None