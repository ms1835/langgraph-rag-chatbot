from rag.loader import load_pdf
from rag.embeddings import get_embeddings
from rag.vector_store import create_vector_store

def build_retriever():
    docs = load_pdf("data/Mayank_Singh_GenAI.pdf")

    embeddings = get_embeddings()

    vector_store = create_vector_store(docs, embeddings)

    return vector_store.as_retriever(
        search_type="similarity",
        search_kwargs={"k": 3}
    )

