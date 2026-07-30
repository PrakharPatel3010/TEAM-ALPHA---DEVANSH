import chromadb

# Create a persistent database
client = chromadb.PersistentClient(path="./chroma_db")

# Create (or get) a collection
collection = client.get_or_create_collection(
    name="research_papers"
)