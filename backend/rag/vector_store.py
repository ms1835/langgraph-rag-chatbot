from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS

def create_vector_store(documents, embeddings):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=100, 
        chunk_overlap=30
    )

    chunks = splitter.split_documents(documents)
    return FAISS.from_documents(
        chunks,
        embeddings
    )