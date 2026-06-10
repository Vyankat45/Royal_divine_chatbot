from app.vector_store import search_documents

results = search_documents(
    query="Sayog",
    k=10
)

for doc in results:
    print("\n" + "="*50)
    print(doc.metadata)
    print(doc.page_content[:500])