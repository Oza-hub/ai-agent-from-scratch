import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    base_url=os.getenv("GH_ENDPOINT"),
    api_key=os.getenv("GH_TOKEN")
)


def ask_model(messages, tools=None):

    params = {
        "model": os.getenv("GH_MODEL"),
        "messages": messages,
    }

    # Activar tool calling
    if tools:
        params["tools"] = tools
        



    response = client.chat.completions.create(**params)

    # IMPORTANTE: devolver TODO, no solo content
    return response.model_dump()