from fastapi import FastAPI
from models.request import ChatRequest
from services.task_detector import detect_task
from prompt.user_templates import build_user_prompt
from prompt.system import SYSTEM_PTOMPT
from llm.client import client

app = FastAPI()

@app.post("/chat")
def chat(request: ChatRequest):
    task = detect_task(request.message)
    user_prompt = build_user_prompt(task, request.message)

    response = client.responses.create(
        model="gpt-4o-mini",
        input=[
            {"role": "system", "content": SYSTEM_PTOMPT},
            {"role": "user", "content": user_prompt}
        ]
    )
    return {"reply": response.output_text}