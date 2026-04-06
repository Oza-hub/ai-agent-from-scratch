import json
import time

from core.client import ask_model
from config.instructions import SYSTEM_PROMPT

from agent.tool_executor import execute_tool
from agent.tool_validator import normalize_args, validate_tool_call
from agent.planner import detect_goal, create_plan, execute_plan
from agent.plan_validator import validate_plan
from agent.input_processor import normalize_input


# ===== TOOL SCHEMAS =====
TOOL_SCHEMAS = [
    {
        "type": "function",
        "function": {
            "name": "get_destinations",
            "description": "Get travel destinations filtered by region",
            "parameters": {
                "type": "object",
                "properties": {
                    "region": {"type": "string"}
                },
                "required": ["region"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Get current weather",
            "parameters": {
                "type": "object",
                "properties": {
                    "destination": {"type": "string"}
                },
                "required": ["destination"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_destination_info",
            "description": "Get destination info",
            "parameters": {
                "type": "object",
                "properties": {
                    "destination": {"type": "string"}
                },
                "required": ["destination"]
            }
        }
    }
]


# ===== RAG EVALUATION =====
def evaluate_step(messages, tool_cache):
    last_msg = messages[-1]
    role = last_msg.get("role")
    content = last_msg.get("content", "")

    if not content:
        return "continue"

    text = content.lower().strip()

    if role == "assistant":
        if len(text) > 50:
            return "enough"

        strong_signals = ["clima", "temperatura", "destino", "bogotá", "rio", "parís"]

        if any(s in text for s in strong_signals):
            return "enough"

    impossible_signals = [
        "no existe",
        "no puedo proporcionar",
        "no hay datos",
        "no se puede"
    ]

    if any(s in text for s in impossible_signals):
        return "enough"

    return "continue"


# ===== EVALUACIÓN =====
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

    # ===== SUCCESS RATE =====
    if tool_calls > 0:
        success_rate = (tool_calls - tool_errors) / tool_calls
    else:
        success_rate = 1.0

    # ===== COMPLETENESS =====
    total_items = 0
    valid_items = 0

    for section in data.values():
        if isinstance(section, dict):
            for v in section.values():
                total_items += 1

                # ignorar errores explícitos
                if isinstance(v, dict) and "error" in v:
                    continue

                if v is not None:
                    valid_items += 1

    completeness = (valid_items / total_items) if total_items else 1.0

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


class TravelAgent:

    def __init__(self, state):
        self.state = state

    def run(self, user_input):

        text = user_input.lower()
        self.state.add_user_message(user_input)

        normalized_input = normalize_input(user_input)

        start_time = time.time()

        goal = detect_goal(normalized_input)
        plan = create_plan(goal, normalized_input)

        if not plan:
            return "No se pudo interpretar correctamente la solicitud. Intenta usar regiones como: Europa, Asia o Sudamérica."

        is_valid, error = validate_plan(plan)

        if not is_valid:
            return f"Invalid plan: {error}"

        print("[PLANNER] Plan detected → executing...")

        result = execute_plan(plan)

        # FIX PRINCIPAL
        if result["status"] == "error":
            return "Error ejecutando el plan"

        data = result["data"]

        # ===== EVALUACIÓN =====
        evaluation = evaluate_plan_result(result)
        quality = evaluation["quality"]
        eval_metrics = evaluation["metrics"]

        # ===== ADAPTIVE =====
        if quality == "bad":

            print("[ADAPTIVE] Bad result detected → attempting recovery...")

            retry_improved = False

            if eval_metrics["tool_errors"] > 0:

                print("[ADAPTIVE] Retrying failed execution once...")

                retry_result = execute_plan(plan)

                if retry_result["status"] == "success":

                    retry_eval = evaluate_plan_result(retry_result)

                    if retry_eval["quality"] in ["partial", "good"]:
                        print("[ADAPTIVE] Retry improved result")

                        result = retry_result
                        data = result["data"]
                        quality = retry_eval["quality"]
                        eval_metrics = retry_eval["metrics"]

                        retry_improved = True

            if quality == "bad" and not retry_improved:

                print("[ADAPTIVE] Replanning → simplifying output")

                simplified_data = {}

                if "weather" in data and data["weather"]:
                    simplified_data["weather"] = data["weather"]

                elif "info" in data and data["info"]:
                    simplified_data["info"] = data["info"]

                if simplified_data:
                    data = simplified_data
                    quality = "partial"

        # ===== RESPONSE =====
        response_lines = []

        # ===== DESTINATIONS =====
        if "destinations" in data and data["destinations"]:
            response_lines.append("Destinos disponibles:")
            for d in data["destinations"]:

                if isinstance(d, dict):
                    response_lines.append(f"- {d['name']} ({d['city']})")
                else:
                    response_lines.append(f"- {d}")

        if "weather" in data and data["weather"]:
            response_lines.append("Clima por destino:")
            for dest, weather in data["weather"].items():

                #Ocultar errores tecnicos
                if isinstance(weather, dict) and "error" in weather:
                    response_lines.append(f"{dest}: no disponible")
                    continue
                
                response_lines.append(f"{dest}: {weather}")

        if "info" in data and data["info"]:
            valid_info = {k: v for k, v in data["info"].items() if v is not None}

            if valid_info:
                response_lines.append("\nInformación por destino:")
                for dest, info in valid_info.items():
                    if isinstance(info, dict):
                        response_lines.append(
                            f"{dest}: {info.get('country')}, {info.get('language')}, {info.get('description')}"
                        )
                    else:
                        response_lines.append(f"{dest}: {info}")

        if not response_lines:
            final_text = "No hay datos disponibles."
        elif quality == "partial":
            final_text = "\n".join(response_lines) + "\n\n(Algunos datos no estaban disponibles)"
        else:
            final_text = "\n".join(response_lines)

        # ===== OBSERVABILITY =====
        latency = round(time.time() - start_time, 3)

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

        self.state.add_agent_message(final_text)

        return final_text