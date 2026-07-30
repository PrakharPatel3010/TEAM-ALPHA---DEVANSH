from database.chroma_db import search_chunks
from services.embedding_service import create_embedding


def retrieve_chunks(question, n_results=3):
    """
    Convert the user's question into an embedding
    and retrieve the most relevant document chunks.
    """

    embedding = create_embedding(question)

    results = search_chunks(
        query_embedding=embedding,
        n_results=n_results
    )

    return results