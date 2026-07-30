import chromadb

client = chromadb.PersistentClient(path="./chroma_db")

collection = client.get_or_create_collection(
    name="research_papers"
)

def add_chunk(chunk_id, text, embedding, metadata=None):
    collection.add(
        ids=[chunk_id],
        documents=[text],
        embeddings=[embedding],
        metadatas=[metadata or {}]
    )

def search_chunks(query_embedding, n_results=3):
    return collection.query(
        query_embeddings=[query_embedding],
        n_results=n_results
    )

def clear_collection():
    collection.delete(
        ids=collection.get()["ids"]
    )