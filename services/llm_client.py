import os
from openai import OpenAI
from dotenv import load_dotenv
from typing import List, Dict

load_dotenv()

# -----------------------------
# 設定値はここに集約
# -----------------------------
MODEL_NAME = "gpt-4o-mini"

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

# -----------------------------
# LLM呼び出し関数
# -----------------------------
def call_llm(messages: List[Dict[str, str]]) -> str:
    response = client.responses.create(
        model=MODEL_NAME,
        input=messages
    )

    return response.output_text
