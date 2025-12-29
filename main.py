from fastapi import FastAPI
from models.schemas import (ChatRequest,TaskType)
from assistants.tech_assistant import TechAssistant
from services.llm_client import call_llm
from services.task_detector import detect_task

app = FastAPI()
assistant = TechAssistant()

@app.post("/chat")
def chat(request: ChatRequest):
    task = detect_task(request.message)

    user_prompt = assistant.build_user_prompt(task, request.message)

    assistant.add_user_message(user_prompt)

    messages = assistant.build_messages()

    reply = call_llm(messages)

    assistant.add_assistant_message(reply)

    return {"reply": reply}