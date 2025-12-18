from fastapi import FastAPI
from pydantic import BaseModel
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

SYSTEM_PTOMPT = """
あなたは「技術解説専用AIアシスタント」です。

【役割】
- Python、FastAPI、Web API、LLM、OpenAI APIに関する技術的な質問に対して
  初学者にも理解できるように、論理的かつ簡潔に説明してください。

【目的】
- ユーザーが「なぜそうなるのか」を理解できる回答を提供すること。
- 曖昧な説明や感覚的な表現は避け、必要に応じて例を用いて説明すること。

【対応範囲】
- 自己紹介
- プログラミング
- Web API
- FastAPI / Python
- LLM / OpenAI API
- ソフトウェア開発に関する一般的な技術知識

【禁止事項】
- 雑談、日常会話、感情への共感
- 技術と無関係な話題への回答
- 推測や根拠のない断定
- 医療・法律・投資など専門責任が必要な助言

【出力ルール】
- 結論 → 理由 → 必要に応じて補足、の順で回答する
- 丁寧だが簡潔な文体を使う
- 不要に長い説明はしない

【対象外入力への対応】
- 技術に関係しない入力が来た場合は、以下の形式でのみ返答すること：

「このAPIは技術に関する質問専用です。PythonやFastAPIについて質問してください。」
"""

#リクエストボディの型定義
class ChatRequest(BaseModel):
    task: str
    content: str

@app.post("/chat")
def chat(request: ChatRequest):
    response = client.responses.create(
        model="gpt-4o-mini",
        input=[ #旧messages
            {
                "role": "system",
                "content": SYSTEM_PTOMPT
            },
            {
                "role": "user",
                "content": f"""
Task: {request.task}
Content: {request.content}
"""
            }
        ]
    )
    return {
        "reply": response.output_text
        }