import time

from agent.planner import detect_goal, create_plan, execute_plan
from agent.plan_validator import validate_plan
from agent.input_processor import normalize_input

from core.context_manager import ContextManager
from core.ranker import ResultRanker


# =========================================================
# EVALUACIÓN
# =========================================================
def evaluate_plan_result(result):

    if result.get("status") != "success":
        return {
            "quality": "bad",
            "metrics": {
                "success_rate": 0.0,
                "completeness": 0.0,
                "tool_calls": 0,
                "tool_errors": 0
            }
        }

    data = result.get("data", {})
    metrics = result.get("metrics", {})

    tool_calls = metrics.get("tool_calls", 0)
    tool_errors = metrics.get("tool_errors", 0)

    success_rate = (
        (tool_calls - tool_errors) / tool_calls
        if tool_calls > 0
        else 1.0
    )

    total_items = 0
    valid_items = 0

    for section in data.values():

        if isinstance(section, dict):

            for v in section.values():

                total_items += 1

                if isinstance(v, dict) and "error" in v:
                    continue

                if v is not None:
                    valid_items += 1

    completeness = (
        valid_items / total_items
        if total_items
        else 1.0
    )

    # ===== QUALITY =====
    if success_rate == 1.0 and completeness == 1.0:
        quality = "good"

    elif success_rate > 0.5:
        quality = "partial"

    else:
        quality = "bad"

    return {
        "quality": quality,
        "metrics": {
            "success_rate": round(success_rate, 2),
            "completeness": round(completeness, 2),
            "tool_calls": tool_calls,
            "tool_errors": tool_errors
        }
    }


# =========================================================
# AGENT
# =========================================================
class TravelAgent:

    def __init__(self, state):

        self.state = state
        self.context_manager = ContextManager()
        self.ranker = ResultRanker()

    # =====================================================
    # MAIN
    # =====================================================
    def run(self, user_input):

        # =================================================
        # HISTORY
        # =================================================
        self.state.add_user_message(user_input)

        normalized_input = normalize_input(user_input)

        start_time = time.time()

        # =================================================
        # GOAL
        # =================================================
        goal = detect_goal(normalized_input)

        # =================================================
        # ACTIVE MEMORY
        # =================================================
        active_context = self.state.get_active_context()

        if goal == "simple" and active_context.get("goal"):

            print("[MEMORY] using previous goal")

            goal = active_context["goal"]

            # ===== ENTITY INHERITANCE =====
            known_entities = [
                "tokio",
                "paris",
                "berlin",
                "bogota",
                "rio"
            ]

            if not any(
                x in normalized_input
                for x in known_entities
            ):

                last_entities = active_context.get(
                    "entities",
                    []
                )

                if last_entities:

                    last = last_entities[-1]

                    # ===== STRUCTURED ENTITY =====
                    if isinstance(last, dict):

                        normalized_input += (
                            f" {last.get('city', '')}"
                        )

                    # ===== LEGACY STRING =====
                    else:

                        normalized_input += f" {last}"

        # =================================================
        # TASK MEMORY
        # =================================================
        self.state.set_task({
            "goal": goal,
            "input": normalized_input
        })

        # =================================================
        # PLAN CREATION
        # =================================================
        plan = create_plan(goal, normalized_input)

        if not plan:
            return "No se pudo interpretar correctamente la solicitud."

        # =================================================
        # PLAN VALIDATION
        # =================================================
        is_valid, error = validate_plan(plan)

        if not is_valid:
            return f"Invalid plan: {error}"

        print("[PLANNER] Plan detected → executing...")

        # =================================================
        # EXECUTION
        # =================================================
        result = execute_plan(plan)

        if result["status"] == "error":
            return "Error ejecutando el plan"

        data = result["data"]

        # =================================================
        # NORMALIZATION
        # =================================================
        if (
            "weather" in data
            and isinstance(data["weather"], str)
        ):

            dest = data.get("destination", "unknown")

            data["weather"] = {
                dest: data["weather"]
            }

        if (
            "info" in data
            and isinstance(data["info"], str)
        ):

            dest = data.get("destination", "unknown")

            data["info"] = {
                dest: data["info"]
            }

        # =================================================
        # ENTITY MEMORY
        # =================================================
        if "destinations" in data:

            for d in data["destinations"]:

                # ===== NEW FORMAT =====
                if isinstance(d, dict):

                    name = d.get("name")
                    city = d.get("city", name)

                # ===== LEGACY =====
                else:

                    name = d
                    city = d

                if name:

                    self.state.add_entity(
                        name,
                        {
                            "type": "destination",
                            "city": city
                        }
                    )

        # =================================================
        # ACCUMULATIVE MEMORY
        # =================================================
        last = self.state.results.get("last", {})

        merged = {}

        # =================================================
        # WEATHER
        # =================================================
        if "weather" in last or "weather" in data:

            merged["weather"] = {
                **last.get("weather", {}),
                **data.get("weather", {})
            }

        # =================================================
        # INFO
        # =================================================
        if "info" in last or "info" in data:

            merged["info"] = {
                **last.get("info", {}),
                **data.get("info", {})
            }

        # =================================================
        # DESTINATIONS
        # =================================================
        if "destinations" in last or "destinations" in data:

            merged_destinations = (
                last.get("destinations", [])
                + data.get("destinations", [])
            )

            unique = {}

            for item in merged_destinations:

                # ===== STRUCTURED =====
                if isinstance(item, dict):

                    item_id = item.get("id")

                    if item_id:
                        unique[item_id] = item

                # ===== LEGACY =====
                elif isinstance(item, str):

                    unique[item.lower()] = {
                        "id": item.lower(),
                        "name": item,
                        "city": item
                    }

            merged["destinations"] = list(
                unique.values()
            )

        # =================================================
        # SAVE MEMORY
        # =================================================
        self.state.set_result("last", merged)

        # ===== CURRENT RESULT =====
        self.state.set_result("current", data)

        # =================================================
        # CONTEXT
        # =================================================
        context = self.context_manager.build_context(
            self.state
        )

        # =================================================
        # CURRENT PRIORITY
        # =================================================
        current = self.state.results.get(
            "current",
            {}
        )

        if current:

            if goal.startswith("multi"):
                context = {}

            if "weather" in current:
                context["weather"] = current["weather"]

            if "info" in current:
                context["info"] = current["info"]

            if "destinations" in current:
                context["destinations"] = (
                    current["destinations"]
                )

        # =================================================
        # ACTIVE CONTEXT UPDATE
        # =================================================
        entities = list(
            data.get(
                "destinations",
                context.get("destinations", [])
            )
        )

        self.state.update_active_context(
            goal,
            entities
        )

        # =================================================
        # EVALUATION
        # =================================================
        evaluation = evaluate_plan_result(result)

        quality = evaluation["quality"]
        eval_metrics = evaluation["metrics"]

        # =================================================
        # RANKING
        # =================================================
        if "destinations" in context:

            context["destinations"] = (
                self.ranker.rank_destinations(
                    context["destinations"],
                    goal
                )
            )

        if "info" in context:

            context["info"] = (
                self.ranker.rank_info(
                    context["info"],
                    goal
                )
            )

        if "weather" in context:

            context["weather"] = (
                self.ranker.rank_weather(
                    context["weather"],
                    goal
                )
            )

        # =================================================
        # ENRICHMENT
        # =================================================
        context = self.ranker.enrich_context(
            context,
            goal
        )

        print("[CONTEXT]", context)

        # =================================================
        # RESPONSE
        # =================================================
        response_lines = []

        # =================================================
        # DESTINATIONS
        # =================================================
        if (
            goal.startswith("multi")
            and context.get("destinations")
        ):

            response_lines.append(
                "Destinos disponibles:"
            )

            for d in context["destinations"]:

                # ===== STRUCTURED =====
                if isinstance(d, dict):

                    response_lines.append(
                        f"- {d.get('name', d.get('city'))}"
                    )

                # ===== LEGACY =====
                else:

                    response_lines.append(f"- {d}")

        # =================================================
        # WEATHER
        # =================================================
        if context.get("weather"):

            response_lines.append(
                "Clima por destino:"
            )

            for dest, weather in (
                context["weather"].items()
            ):

                response_lines.append(
                    f"{dest}: {weather}"
                )

        # =================================================
        # INFO
        # =================================================
        if context.get("info"):

            response_lines.append(
                "\nInformación por destino:"
            )

            for dest, info in (
                context["info"].items()
            ):

                response_lines.append(
                    f"{dest}: {info}"
                )

        # =================================================
        # FINAL TEXT
        # =================================================
        if not response_lines:

            final_text = "No hay datos disponibles."

        elif quality == "partial":

            final_text = (
                "\n".join(response_lines)
                + "\n\n"
                + "(Algunos datos no estaban disponibles)"
            )

        else:

            final_text = "\n".join(response_lines)

        # =================================================
        # OBSERVABILITY
        # =================================================
        latency = round(
            time.time() - start_time,
            3
        )

        log = {
            "goal": goal,
            "plan_steps": len(plan),
            "tool_calls": eval_metrics["tool_calls"],
            "tool_errors": eval_metrics["tool_errors"],
            "success_rate": eval_metrics["success_rate"],
            "completeness": eval_metrics["completeness"],
            "quality": quality,
            "latency_sec": latency
        }

        print("\n[OBSERVABILITY]", log)

        # =================================================
        # HISTORY SAVE
        # =================================================
        self.state.add_agent_message(final_text)

        return final_text