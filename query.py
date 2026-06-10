from app.vector_store import search_documents

question = "What is the company address?"

results = search_documents(
    query=question,
    k=10
)

for doc, score in results:
    print(score)
    print(doc.page_content[:300])