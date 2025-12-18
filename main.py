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


def build_user_prompt(task: TaskType, user_input: str) -> str:
    if task == TaskType.EXPLAIN:
        return f"""
Task: Explain
Audience: ソフトウェア開発初心者
Constraints:
- 日本語で回答する
- 結論 → 理由 → 具体例 の順で説明する
- 専門用語は必ず噛み砕いて説明する

Question:
{user_input}
"""

    if task == TaskType.REWRITE:
        return f"""
Task: Rewrite
Constraints:
- 日本語で書き直す
- 意味は変えない
- より分かりやすくする

Original Text:
{user_input}
"""

    if task == TaskType.SUMMARIZE:
        return f"""
Task: Summarize
Constraints:
- 日本語で要約する
- 3行以内
- 要点のみ

Text:
{user_input}
"""

    if task == TaskType.JUDGE:
        return f"""
Task: Judge
Constraints:
- 日本語で回答
- 結論を最初に述べる
- 理由を簡潔に述べる

Question:
{user_input}
"""

    return user_input


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