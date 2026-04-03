from agent.tool_registry import tool_registry


def execute_tool(tool_name, args):

    try:
        print(f"[DEBUG] Tool call → {tool_name} | args → {args}")

        # ===== VALIDAR EXISTENCIA =====
        if tool_name not in tool_registry:
            return {
                "success": False,
                "error": "unknown_tool",
                "data": None,
                "tool": tool_name
            }

        tool = tool_registry[tool_name]

        # ===== EJECUCIÓN =====
        result = tool["function"](**args)

        print(f"[DEBUG] Tool result → {result}")

        return result

    except Exception as e:
        print(f"[ERROR] Tool failed → {str(e)}")

        return {
            "success": False,
            "error": "execution_error",
            "data": None,
            "details": str(e),
            "tool": tool_name
        }