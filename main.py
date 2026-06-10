from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel

from app.rag_service import ask_question

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
def home():
    return FileResponse("static/index.html")


class QuestionRequest(BaseModel):
    question: str
    session_id: str


@app.post("/ask")
def ask(req: QuestionRequest):

    answer = ask_question(
        req.question,
        req.session_id
    )

    return {
        "answer": answer
    }