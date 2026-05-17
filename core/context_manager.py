class ContextManager:

    def __init__(self, max_destinations=5, max_info_length=300):
        self.max_destinations = max_destinations
        self.max_info_length = max_info_length

    def build_context(self, state):

        context = {}

        last_results = state.results.get("last", {})
        destinations = list(state.entities.keys())

        # ===== CASO: SIN ENTIDADES → USAR RESULTADOS DIRECTOS =====
        if not destinations:

            # ===== WEATHER =====
            if "weather" in last_results and isinstance(last_results["weather"], dict):
                context["weather"] = last_results["weather"]
                context["destinations"] = list(last_results["weather"].keys())
                return context

            # ===== INFO =====
            if "info" in last_results and isinstance(last_results["info"], dict):
                context["info"] = {
                    k: self._truncate(v)
                    for k, v in last_results["info"].items()
                }
                context["destinations"] = list(last_results["info"].keys())
                return context

        # ===== NORMAL FLOW =====
        context["destinations"] = destinations[:self.max_destinations]

        # ===== WEATHER =====
        if "weather" in last_results:

            weather_data = last_results["weather"]

            if isinstance(weather_data, dict):
                context["weather"] = {
                    k: v for k, v in weather_data.items()
                    if k in context["destinations"]
                }

        # ===== INFO =====
        if "info" in last_results:

            info_data = last_results["info"]

            if isinstance(info_data, dict):
                context["info"] = {
                    k: self._truncate(v)
                    for k, v in info_data.items()
                    if k in context["destinations"]
                }

        return context

    # ===== UTILIDAD =====
    def _truncate(self, text):
        if not isinstance(text, str):
            return text

        text = text.replace("\xa0", " ").strip()

        if len(text) <= self.max_info_length:
            return text

        return text[:self.max_info_length] + "..."