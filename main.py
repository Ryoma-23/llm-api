from fastapi import FastAPI
from pydantic import BaseModel
from openai import OpenAI
from dotenv import load_dotenv
from enum import Enum
import os

load_dotenv()

app = FastAPI()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

SYSTEM_PTOMPT = """
あなたは技術解説専用のAIアシスタントです。

【基本方針】
- 回答は必ず日本語で行ってください
- 技術・IT・プログラミングに関する内容のみを扱います
- 雑談、感情的な慰め、日常会話には応答しません
- 結論 → 理由 → 補足 の順で簡潔に説明してください

【入力仕様】
- User入力には task と content が与えられます
- task に従って content を処理してください
"""

#リクエストボディの型定義
class ChatRequest(BaseModel):
    message: str
    # task: str
    # content: str

class TaskType(str, Enum):
    EXPLAIN = "Explain"
    REWRITE = "Rewrite"
    SUMMARIZE = "Summrize"
    JDGE = "Judge"

def detect_task(user_input: str) -> TaskType:
    text = user_input.lower()

    if any(word in text for word in ["とは", "意味", "何", "教えて"]):
        return TaskType.EXPLAIN

    if any(word in text for word in ["直して", "修正", "書き直"]):
        return TaskType.REWRITE

    if any(word in text for word in ["要約", "まとめて"]):
        return TaskType.SUMMARIZE

    if any(word in text for word in ["どっち", "正しい", "比較"]):
        return TaskType.JUDGE

    return TaskType.EXPLAIN  # デフォルト


@app.post("/chat")
def chat(request: ChatRequest):
    task = detect_task(request.message)

    user_prompt = F"""
Task: {task}
Question: {request.message}
"""
    
    response = client.responses.create(
        model="gpt-4o-mini",
        input=[
            {"role": "system", "content": SYSTEM_PTOMPT},
            {"role": "user", "content": user_prompt}
        ]
    )
    return {"reply": response.output_text}