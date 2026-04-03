def evaluate_plan_result(result: dict):

    # ===== VALIDACIÓN =====
    if not result.get("success"):
        return {
            "quality": "bad",
            "metrics": {
                "success_rate": 0.0,
                "completeness": 0.0
            },
            "reason": result.get("error", "execution_failed")
        }

    data = result.get("data", {})
    metrics = result.get("metrics", {})

    tool_calls = metrics.get("tool_calls", 0)
    tool_errors = metrics.get("tool_errors", 0)

    # ===== SUCCESS RATE =====
    success_rate = 1.0
    if tool_calls > 0:
        success_rate = (tool_calls - tool_errors) / tool_calls

    # ===== COMPLETENESS =====
    total_items = 0
    valid_items = 0

    for section in data.values():
        if isinstance(section, dict):
            for v in section.values():
                total_items += 1
                if v is not None:
                    valid_items += 1

    completeness = 1.0
    if total_items > 0:
        completeness = valid_items / total_items

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