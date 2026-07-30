from database.chroma_db import add_chunk
from services.embedding_service import create_embedding

def store_chunks(chunks, filename):
    for index, chunk in enumerate(chunks):

        embedding = create_embedding(chunk)

        add_chunk(
            chunk_id=f"{filename}_{index}",
            text=chunk,
            embedding=embedding,
            metadata={
                "paper": filename,
                "chunk": index
            }
        )