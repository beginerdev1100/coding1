from openai import OpenAI
from sentence_transformers import SentenceTransformer
from pinecone import Pinecone
from pinecone import ServerlessSpec

model = SentenceTransformer("all-MiniLM-L6-v2")
try:
    pc = Pinecone(
        api_key="pcsk_jvYbH_CDewgcFV23xm3YebAV8CBt7tvf4tTUMX2cicZPJMxqmdwYRBUoXCxD7SMP9LHMJ"
    )
except Exception as e:
    print("API key invalid")
messages = []

INDEX_NAME = "secondrag"
if not pc.has_index(INDEX_NAME):
    pc.create_index(
        name=INDEX_NAME,
        vector_type="dense",
        dimension=384,
        metric="cosine",
        spec=ServerlessSpec(cloud="aws", region="us-east-1"),
    )
index = pc.Index("secondrag")

try:
    client = OpenAI(
        base_url="https://integrate.api.nvidia.com/v1",
        api_key="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",
    )
except Exception as e:
    print(f"OpenAI client could not be created because of {e}")

texts = [
    "Go to Settings > Account > Reset Password, and follow the email link we send you.",
    "We accept Visa, Mastercard, American Express, and PayPal.",
    "You can cancel anytime from Settings > Billing > Cancel Subscription.",
    "Yes, we offer full refunds within 30 days of purchase.",
    "You can reach us via live chat, email at support@example.com, or our help center.",
    "Yes, we offer a 14-day free trial with full access to all features.",
    "Go to Settings > Account > Email, enter your new email, and verify it.",
    "Yes, your account syncs across up to 5 devices.",
    "We'll retry the charge after 3 days and notify you by email if it fails again.",
    "Go to Settings > Privacy > Export Data to download a copy of your account data.",
    "Yes, our app is available on both iOS and Android.",
    "Go to Settings > Billing > Upgrade Plan to choose a higher tier.",
    "Yes, all data is encrypted in transit and at rest using industry-standard protocols.",
    "Yes, go to Settings > Team > Invite Members to add collaborators by email.",
    "We guarantee 99.9% uptime, with status updates available at status.example.com.",
]

if index.describe_index_stats()['total_vector_count'] == 0:
    embeds = embeddings = model.encode(texts)

    ids = [f"id{i}" for i in range(len(texts))]

    vectors = [
        {"id": id_, "values": embed.tolist(), "metadata": {"text": text}}
        for id_, embed, text in zip(ids, embeds, texts)
    ]
    index.upsert(vectors=vectors, namespace="faqs")


def prompt_format(user, docs):
    prompt = f"""
    You will take the user question which is '{user}'
    and you will answer it using this info do not make up your own info: '{docs}'
    """
    return prompt


def ask(user, docs):
    try:
        messages.append({"role": "user", "content": prompt_format(user, docs)})
        completion = client.chat.completions.create(
            model="nvidia/nemotron-3-ultra-550b-a55b", messages=messages
        )
        print(completion.choices[0].message.content)
    except Exception as e:
        print(f"Could not get your response because of {e}")


def get_query(user):
    try:
        user = model.encode(user)
        docs = index.query(
            vector=user.tolist(), top_k=1, namespace="faqs", include_metadata=True
        )
        if not docs["matches"] or docs["matches"][0]["score"] < 0.5: 
            return None
        return docs["matches"][0]["metadata"]
    except Exception as e:
        print(f"Could not get query. {e}")


def main():
    while True:
        user = input("User: ")
        if user:
            answer = get_query(user)
            if answer == None:
                ask(user, "There was no document that was related to this question if this is a follow up question answer else say I dont have info on that")
            else:
                ask(user, answer)
        else:
            print("Please provide input")


main()
