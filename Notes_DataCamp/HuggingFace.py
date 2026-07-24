import OpenAi

client = OpenAi(
    api_key="text-gen-model",
    base_url=""
)
messages = [
    {"role": "user", "content": "Write me a paper on ml"}
]
print(client(messages))
