# =========================================================
# STUDY TUTOR RAG
# =========================================================

import os
import pickle

import faiss
import numpy as np
from sentence_transformers import SentenceTransformer


# =========================================================
# EMBEDDING MODEL
# =========================================================

EMBEDDING_MODEL = "all-MiniLM-L6-v2"


def get_embedding_model():
    """
    Load the sentence-transformer embedding model.
    """

    return SentenceTransformer(EMBEDDING_MODEL)


# =========================================================
# TEXT CHUNKING
# =========================================================

def create_chunks(
    text,
    chunk_size=500,
    chunk_overlap=100,
):
    """
    Split document text into overlapping chunks.
    """

    text = text.strip()

    if not text:
        return []

    chunks = []

    start = 0

    while start < len(text):

        end = start + chunk_size

        chunk = text[start:end].strip()

        if chunk:
            chunks.append(chunk)

        start += chunk_size - chunk_overlap

    return chunks


# =========================================================
# CREATE EMBEDDINGS
# =========================================================

def create_embeddings(texts):
    """
    Convert text chunks into vector embeddings.
    """

    if not texts:
        return np.array([])

    model = get_embedding_model()

    embeddings = model.encode(
        texts,
        convert_to_numpy=True,
        normalize_embeddings=True,
    )

    return embeddings.astype("float32")


# =========================================================
# CREATE FAISS INDEX
# =========================================================

def create_faiss_index(embeddings):
    """
    Create a FAISS vector index from embeddings.
    """

    if embeddings is None or len(embeddings) == 0:
        return None

    dimension = embeddings.shape[1]

    index = faiss.IndexFlatIP(dimension)

    index.add(embeddings)

    return index


# =========================================================
# SEARCH DOCUMENTS
# =========================================================

def search_documents(
    question,
    chunks,
    index,
    top_k=5,
):
    """
    Search for the most relevant chunks using FAISS.
    """

    if not chunks or index is None:
        return []

    model = get_embedding_model()

    question_embedding = model.encode(
        [question],
        convert_to_numpy=True,
        normalize_embeddings=True,
    ).astype("float32")

    scores, indices = index.search(
        question_embedding,
        min(top_k, len(chunks)),
    )

    results = []

    for score, index_number in zip(
        scores[0],
        indices[0],
    ):

        if index_number < 0:
            continue

        results.append(
            {
                "text": chunks[index_number],
                "score": float(score),
            }
        )

    return results


# =========================================================
# SAVE RAG DATA
# =========================================================

def save_rag_data(
    index,
    chunks,
    file_path="data/rag_data.pkl",
):
    """
    Save FAISS index and chunks for reuse.
    """

    os.makedirs(
        os.path.dirname(file_path),
        exist_ok=True,
    )

    faiss.write_index(
        index,
        file_path.replace(".pkl", ".faiss"),
    )

    with open(
        file_path,
        "wb",
    ) as file:

        pickle.dump(
            chunks,
            file,
        )


# =========================================================
# LOAD RAG DATA
# =========================================================

def load_rag_data(
    file_path="data/rag_data.pkl",
):
    """
    Load previously saved FAISS index and chunks.
    """

    faiss_path = file_path.replace(
        ".pkl",
        ".faiss",
    )

    if not os.path.exists(file_path):
        return None, []

    if not os.path.exists(faiss_path):
        return None, []

    index = faiss.read_index(
        faiss_path
    )

    with open(
        file_path,
        "rb",
    ) as file:

        chunks = pickle.load(file)

    return index, chunks


# =========================================================
# BUILD RAG INDEX
# =========================================================

def build_rag_index(text):
    """
    Complete RAG pipeline:

    Text
      ↓
    Chunks
      ↓
    Embeddings
      ↓
    FAISS Index
    """

    chunks = create_chunks(text)

    if not chunks:
        return None, []

    embeddings = create_embeddings(
        chunks
    )

    index = create_faiss_index(
        embeddings
    )

    return index, chunks
