# backend/app/retrieval.py
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np # Import numpy for array handling

# This module no longer loads embeddings and index directly.
# Instead, it receives them as arguments, making it reusable with
# pre-loaded components.

def retrieve_context(query: str, texts: list[str], embedder: SentenceTransformer, index: faiss.Index, top_k: int = 10) -> list[str]:
    """
    Retrieves the most relevant text contexts from a corpus based on a user query.
    
    Args:
        query (str): The user's natural language query.
        texts (list[str]): The list of all available text documents.
        embedder (SentenceTransformer): The pre-loaded SentenceTransformer model.
        index (faiss.Index): The pre-loaded FAISS index.
        top_k (int): The number of top relevant contexts to retrieve.
        
    Returns:
        list[str]: A list of top_k most relevant text contexts.
    """
    try:
        # Encode the query using the pre-loaded embedder model.
        query_embedding = embedder.encode([query], convert_to_numpy=True)
        
        # Perform a similarity search on the FAISS index.
        # distances: distances to the nearest neighbors
        # indices: indices of the nearest neighbors in the original embeddings array
        distances, indices = index.search(query_embedding, top_k)
        
        # Retrieve the actual text documents using the found indices.
        # indices[0] because index.search returns a 2D array (batch size x top_k),
        # and we only have one query (batch size 1).
        return [texts[i] for i in indices[0]]
    except Exception as e:
        print(f"Error during context retrieval: {e}")
        return [] # Return empty list on error

