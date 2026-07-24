from openai import OpenAI
from sentence_transformers import SentenceTransformer
from pinecone import Pinecone
from pinecone import ServerlessSpec
from langchain_text_splitters import CharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader

model = SentenceTransformer("all-MiniLM-L6-v2")
try:
    pc = Pinecone(
        api_key="pcsk_jvYbH_CDewgcFV23xm3YebAV8CBt7tvf4tTUMX2cicZPJMxqmdwYRBUoXCxD7SMP9LHMJ"
    )
except Exception as e:
    print("API key invalid")
messages = []
text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
index_name = "secondrag"
if not pc.has_index(index_name):
    pc.create_index(
        name=index_name,
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

def get_file_text():
    loader = PyPDFLoader("document.pdf")
    document = loader.load()

    return document

def chunks():
    chunks = text_splitter.split_documents(get_file_text())
    return [chunk.page_content for chunk in chunks]
texts = chunks()

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
    if the info just provided if it does not match the question say 'I dont have info on that' unless it is a follow up question then you can take the past data and use that"""
    return prompt


def ask(user, docs):
    try:
        messages.append({"role": "user", "content": prompt_format(user, docs)})
        completion = client.chat.completions.create(
            model="nvidia/nemotron-3-ultra-550b-a55b", messages=messages
        )
        print(completion.choices[0].message.content)
    except Exception as e:
        print("Could not get your response because of {e}")


def get_query(user):
    try:
        user = model.encode(user)
        docs = index.query(
            vector=user.tolist(), top_k=1, namespace="faqs", include_metadata=True
        )
        return docs["matches"][0]["metadata"]
    except Exception as e:
        print(f"Could not get query. {e}")


def main():
    while True:
        user = input("User: ")
        if user:
            answer = get_query(user)
            ask(user, answer)
        else:
            print("Please provide input")

main()
