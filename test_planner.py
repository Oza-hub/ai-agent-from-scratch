from agent.planner import detect_goal, create_plan


def run_test():

    user_input = "dame destinos en europa y el clima"

   
    print("INPUT:", user_input)

    goal = detect_goal(user_input)
    print("\nGOAL DETECTED:")
    print(goal)

    plan = create_plan(goal, user_input)
    print("\nPLAN GENERATED:")
    print(plan)

    print("\nDEBUG GOAL TYPE:")
    print(goal)
    print(type(goal))   


if __name__ == "__main__":
    run_test()