from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

embedding_model = HuggingFaceEmbeddings(
    model_name="BAAI/bge-small-en-v1.5"
)

vector_store = Chroma(
    persist_directory="./chroma_db",
    embedding_function=embedding_model
)

def get_vector_store():
    return vector_store

def save_documents(documents):

    vector_store = get_vector_store()

    vector_store.add_documents(documents)

    print(f"Stored {len(documents)} chunks")

def search_documents(
    query: str,
    k: int = 5,
    filter: dict | None = None
):
    vector_store = get_vector_store()

    return vector_store.similarity_search(
        query=query,
        k=k,
        filter=filter
    )