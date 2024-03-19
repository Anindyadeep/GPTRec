from premai import Prem
import os

api_key = os.getenv("PREM_KEY")
client = Prem(api_key=api_key)


messages = [
    {"role": "user", "content": "Who won the world series in 2020?"},
]
project_id = 446

# Create completion
response = client.chat.completions.create(
    project_id=project_id,
    messages=messages,
)

print(response.choices)
