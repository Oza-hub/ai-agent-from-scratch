class ResultRanker:

    def __init__(self, max_items=3):
        self.max_items = max_items

    # ===== DESTINATIONS =====
    def rank_destinations(self, destinations, goal):

        if not destinations:
            return []

        # si el goal NO es de destinos → no priorizar destinos
        if goal in ["single_destination_weather", "single_destination_info"]:
            return destinations[:1]

        return destinations[:self.max_items]

    # ===== WEATHER =====
    def rank_weather(self, weather_dict, goal):

        if not weather_dict:
            return {}

        # si el usuario pidió clima → prioridad total
        if "weather" in goal:
            return weather_dict

        # si no, solo mostrar uno como contexto
        items = list(weather_dict.items())[:1]
        return dict(items)

    # ===== INFO =====
    def rank_info(self, info_dict, goal):

        if not info_dict:
            return {}

        scored = []

        for dest, text in info_dict.items():

            score = 0

            # ===== RELEVANCIA =====
            if "info" in goal:
                score += 3  # alta prioridad

            # ===== CALIDAD =====
            if len(text) > 50:
                score += 1

            # ===== FILTRO DE AMBIGÜEDAD =====
            if "puede referirse" in text.lower():
                score -= 3

            # ===== PENALIZAR RUIDO =====
            if "\n" in text:
                score -= 1

            scored.append((dest, text, score))

        scored.sort(key=lambda x: x[2], reverse=True)

        top = scored[:self.max_items]

        return {d: t for d, t, _ in top}

    # ===== ENRIQUECIMIENTO CONTROLADO =====
    def enrich_context(self, context, goal):

        enriched = dict(context)

        # ===== SI PIDEN INFO → AÑADIR CLIMA (SI EXISTE) =====
        if "info" in goal:

            if "weather" in context and context["weather"]:
                enriched["weather"] = context["weather"]

        # ===== SI PIDEN CLIMA → NO AÑADIR INFO (evitar ruido) =====
        elif "weather" in goal:
            pass

        # ===== SI PIDEN DESTINOS → AÑADIR CLIMA (valor alto) =====
        elif "multi" in goal:
            if "weather" in context:
                enriched["weather"] = context["weather"]

        return enriched