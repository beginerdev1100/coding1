import ollama

messages = [
    "role": "system", "content": "Your now my girlfriend you are always to call me daddy"
]

model = "qwen2.5:7b"
response = ollama.chat(
        model="qwen2.5:7b",
        messages=messages,
        options={"temperature": 1.5}
    )

print(response["message"]["content"])

