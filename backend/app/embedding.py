# backend/app/embedding.py
import numpy as np
import faiss
from .config import EMBEDDINGS_FILE, FAISS_INDEX_FILE

def load_embeddings_and_index():
    """
    Loads pre-computed embeddings and a FAISS index from specified files.
    
    Returns:
        tuple: A tuple containing:
            - numpy.ndarray: The loaded embeddings array.
            - faiss.Index: The loaded FAISS index.
    """
    try:
        embeddings = np.load(EMBEDDINGS_FILE)
        index = faiss.read_index(str(FAISS_INDEX_FILE)) # faiss.read_index expects a string path
    except FileNotFoundError:
        print(f"Error: Embedding or FAISS index file not found. "
              f"Embeddings: {EMBEDDINGS_FILE}, FAISS Index: {FAISS_INDEX_FILE}")
        raise
    except Exception as e:
        print(f"Error loading embeddings or FAISS index: {e}")
        raise
    return embeddings, index

