from openai import OpenAi

client = OpenAi()

response = client.chat.completions.create(
    model="gpt-5",
    messages=[
        {
            "role": "user",
            "content": "Hello How Are You?"
        }
        ]
)