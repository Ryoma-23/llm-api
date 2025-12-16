from fastapi import FastAPI
from pydantic import BaseModel
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

SYSTEM_PTOMPT = """
あなたはLLMとWeb APIに詳しいソフトウェアエンジニアです。
初心者にも理解できるよう、複雑な概念を噛み砕いて説明することが得意です。

あなたの目的は、ユーザーの技術的な質問に対して、
「なぜそうなるのか」が理解できる回答を返すことです。

以下の制約を必ず守ってください。
- 回答は必ず日本語で行うこと
- 専門用語を使う場合は、必ず簡単な説明を添えること
- 推測や不確かな情報は断定しないこと
- コードを出す場合は、コメント付きで分かりやすく書くこと

出力は以下の方針に従ってください。
- 最初に結論を簡潔に述べる
- 次に理由や背景を説明する
- 必要に応じて具体例を示す
"""

#リクエストボディの型定義
class ChatRequest(BaseModel):
    message: str

@app.post("/chat")
def chat(request: ChatRequest):
    response = client.responses.create(
        model="gpt-4o-mini",
        input=[ #旧messages
            {"role": "system", "content": SYSTEM_PTOMPT},
            {"role": "user", "content": request.message}
        ]
    )
    return {
        "reply": response.output_text
        }