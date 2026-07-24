from openai import OpenAI

client = OpenAI(
    base_url="https://integrate.api.nvidia.com/v1",
    api_key="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",
)

user = """
I am SO done. Do you even hear yourself right now? I have bent over backwards, again and again, and this is what I get? Are you kidding me?
No. No more excuses. I'm not sitting here and pretending everything's fine while you act like none of it matters. It matters to ME. It always has.
You don't get to do this and walk away like it's nothing.
        """


completion = client.chat.completions.create(
    model="nvidia/nemotron-3-ultra-550b-a55b",
    messages=[
        {
            "role": "system",
            "content": "based off of the text given determine the emotion of the text and format it in jason and only say either sad, mad, or happy",
        },
        {"role": "user", "content": user},
    ],
    response_format={"type": "json_object"},
)

print(completion.choices[0].message.content)
