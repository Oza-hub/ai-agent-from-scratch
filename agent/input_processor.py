from difflib import get_close_matches


# ===== PALABRAS VÁLIDAS =====
VALID_REGIONS = ["asia", "europe", "south america"]
VALID_KEYWORDS = ["destinos", "clima", "info"]

# ===== TYPOS COMUNES CONTROLADOS =====
COMMON_TYPOS = {
    "euorpa": "europa",
    "eurpa": "europa",
    "asai": "asia",
    "sudamerica": "south america",
    "suramerica": "south america"
}


# ===== CORRECCIÓN SEGURA =====
def safe_correct(word, valid_words, cutoff=0.75):
    matches = get_close_matches(word, valid_words, n=1, cutoff=cutoff)
    return matches[0] if matches else word


def normalize_input(user_input: str) -> str:

    text = user_input.lower()

    # ===== SINÓNIMOS =====
    synonyms = {
        "lugares": "destinos",
        "sitios": "destinos",
        "locales": "destinos",

        "temperatura": "clima",
        "tiempo": "clima",

        "informacion": "info",
        "información": "info",
        "detalles": "info",
        "datos": "info"
    }

    for word, normalized in synonyms.items():
        text = text.replace(word, normalized)

    # ===== NORMALIZACIÓN DE FRASES =====
    text = text.replace("sur america", "south america")
    text = text.replace("sud america", "south america")

    # ===== TOKENIZACIÓN =====
    tokens = text.split()

    corrected_tokens = []

    for token in tokens:

        # ===== CORRECCIÓN POR DICCIONARIO (PRIORIDAD ALTA) =====
        if token in COMMON_TYPOS:
            corrected_tokens.append(COMMON_TYPOS[token])
            continue

        # ===== CORRECCIÓN DIFUSA =====
        corrected = safe_correct(
            token,
            VALID_REGIONS + VALID_KEYWORDS
        )

        corrected_tokens.append(corrected)

    return " ".join(corrected_tokens)