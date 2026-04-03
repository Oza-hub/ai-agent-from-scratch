from agent.agent import TravelAgent
from core.state import ConversationState


state = ConversationState()
agent = TravelAgent(state)


while True:

    user_input = input("User: ")

    if user_input.lower() == "exit":
        break

    response = agent.run(user_input)

    # ===== RESPUESTA =====
    print("Agent:", response)

    # ===== DEBUG OPCIONAL =====
    if isinstance(response, dict):
        if "metrics" in response:
            print("[DEBUG] Metrics:", response["metrics"])