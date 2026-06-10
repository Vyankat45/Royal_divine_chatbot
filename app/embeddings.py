from langchain_huggingface import HuggingFaceEmbeddings

embedding_model = HuggingFaceEmbeddings(
    model_name="BAAI/bge-small-en-v1.5"
)

vector = embedding_model.embed_query(
    "Royal Divine exports almonds."
)

print(type(vector))
print(len(vector))
print(vector[:10])