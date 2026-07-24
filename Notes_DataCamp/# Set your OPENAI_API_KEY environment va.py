# Set your OPENAI_API_KEY environment variable
import chromadb

collection = client.create_collection(
    name="my_collection",
)

# Chroma will use OpenAIEmbeddingFunction to embed your documents
collection.add(ids=["id1", "id2"], documents=["doc1", "doc2"])
print(collection.peek())