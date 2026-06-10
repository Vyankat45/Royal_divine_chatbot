from app.vector_store import search_documents

results = search_documents(
    query="almond",
    k=3,
    filter={
        "product_name": "almond"
    }
)

for doc in results:
    print("\n" + "=" * 50)
    print(doc.metadata)
    print(doc.page_content[:300])