def validate_plan(plan):

    if  not isinstance(plan, list):
        return False, "Plan must be a list"
    
    allowed_types = {"tool", "map"}

    for step in plan:

        if not isinstance(step, dict):
            return False, "Each step must be a dict"
        
        if "type" not in step:
            return False, "Missing step type"
        
        if step["type"] not in allowed_types:
            return False, f"Invalid step type: {step ['type']}"
        
        if step["type"] == "tool":
            required = {"tool" , "args", "save_as"}

        elif step["type"] == "map":
            required = {"input", "tool", "arg_map", "save_as"}

        for field in required:
            if field not in step:
                return False, f"Missing field '{field}' in step"
            
    return True, None

