from fastapi import FastAPI
from models.request import ChatRequest
from services.task_detector import detect_task
from prompt.user_templates import build_user_prompt
from prompt.system import SYSTEM_PTOMPT
from llm.client import client
from services.assistant import (
    add_user_message,
    add_assistant_message,
    build_messages
)

app = FastAPI()

@app.post("/chat")
def chat(request: ChatRequest):
    task = detect_task(request.message)
    user_prompt = build_user_prompt(task, request.message)

    messages = build_messages(SYSTEM_PTOMPT, user_prompt)

    response = client.responses.create(
        model="gpt-4o-mini",
        input=messages
    )

    reply = response.output_text

    add_user_message(user_prompt)
    add_assistant_message(reply)

    return {"reply": reply}