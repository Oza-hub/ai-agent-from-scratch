from agent.tool_registry import tool_registry


def normalize_result(result):
    """
    Adapter para soportar:
    - formato viejo (success/error)
    - formato nuevo (status/error dict)
    """

    # Ya está en formato nuevo
    if isinstance(result, dict) and "status" in result:
        return result

    # Adaptar formato legacy → nuevo
    if result.get("success"):
        return {
            "status": "success",
            "data": result.get("data"),
            "meta": {
                "source": "legacy_tool"
            }
        }

    return {
        "status": "error",
        "error": {
            "type": result.get("error", "unknown_error"),
            "message": result.get("error", "unknown_error"),
            "retryable": False  # por defecto (luego lo mejoramos)
        },
        "meta": {
            "source": "legacy_tool"
        }
    }


def execute_tool(tool_name, args):

    try:
        print(f"[DEBUG] Tool call → {tool_name} | args → {args}")

        # ===== VALIDAR EXISTENCIA =====
        if tool_name not in tool_registry:
            return {
                "status": "error",
                "error": {
                    "type": "unknown_tool",
                    "message": tool_name,
                    "retryable": False
                }
            }

        tool = tool_registry[tool_name]

        # ===== EJECUCIÓN =====
        raw_result = tool["function"](**args)

        # NORMALIZACIÓN (CLAVE)
        result = normalize_result(raw_result)

        print(f"[DEBUG] Tool result → {result}")

        return result

    except Exception as e:
        print(f"[ERROR] Tool failed → {str(e)}")

        return {
            "status": "error",
            "error": {
                "type": "execution_error",
                "message": str(e),
                "retryable": False
            },
            "meta": {
                "tool": tool_name
            }
        }