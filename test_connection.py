import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    base_url=os.getenv("GH_ENDPOINT"),
    api_key=os.getenv("GH_TOKEN")
)

response = client.chat.completions.create(
    model=os.getenv("GH_MODEL"),
    messages=[
        {"role": "user", "content": "Hello"}
    ]
)

print(response.choices[0].message.content)