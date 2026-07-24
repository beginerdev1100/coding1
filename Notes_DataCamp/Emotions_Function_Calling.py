from openai import OpenAI
import chromadb

client = OpenAI(
    base_url="https://integrate.api.nvidia.com/v1",
    api_key="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",
)
db_client = chromadb.Client()
collection = db_client.get_or_create_collection(name="faqs")

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
    "We guarantee 99.9% uptime, with status updates available at status.example.com."
]

metadata = [
    {"category": "Account",     "topic": "password_reset"},
    {"category": "Billing",     "topic": "payment_methods"},
    {"category": "Billing",     "topic": "cancel_subscription"},
    {"category": "Billing",     "topic": "refunds"},
    {"category": "Support",     "topic": "contact"},
    {"category": "Billing",     "topic": "free_trial"},
    {"category": "Account",     "topic": "change_email"},
    {"category": "Account",     "topic": "device_sync"},
    {"category": "Billing",     "topic": "payment_retry"},
    {"category": "Privacy",     "topic": "data_export"},
    {"category": "General",     "topic": "platform_availability"},
    {"category": "Billing",     "topic": "upgrade_plan"},
    {"category": "Security",    "topic": "encryption"},
    {"category": "Account",     "topic": "team_invite"},
    {"category": "Reliability", "topic": "uptime"},
]


def prompt_format(user, docs):
    prompt = f"""
    You will take the user question which is '{user}'
    and you will answer it using this info do not make up your own info: '{docs}' """
    return prompt


def ask(user, docs):
    completion = client.chat.completions.create(
        model="nvidia/nemotron-3-ultra-550b-a55b",
        messages=[
            {"role": "user", "content": prompt_format(user, docs)},
        ],
    )
    print(completion.choices[0].message.content)


def get_query(user):
    query = collection.query(
        query_texts=user,
        n_results=1
    )
    return query["documents"][0][0]

def get_embeddings():
    pass

def main():
    user = input("User: ")
    collection.add(
        documents=texts,
        metadatas=metadata,
        ids=[f"id{i}" for i in range(len(texts))]
    )
    answer = get_query(user)
    ask(user, answer)

main()
