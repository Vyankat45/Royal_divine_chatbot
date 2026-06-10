from langchain_chroma import Chroma


# vector_store = Chroma(
#     persist_directory="./chroma_db",
#     embedding_function=embedding_model
# )

# temporary changes to test if the issue is with chroma or the embedding model
vector_store = Chroma(
    persist_directory="./chroma_db"
)

def get_vector_store():
    return vector_store


def save_documents(documents):
    raise Exception(
        "Document ingestion is disabled on Render."
    )


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