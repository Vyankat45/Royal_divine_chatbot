from app.rag_service import ask_question

question = "ما هو الحد الأدنى لكمية الطلب؟"

answer = ask_question(question)

print("\nANSWER:\n")
print(answer)