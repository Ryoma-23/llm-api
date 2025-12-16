from openai import OpenAI
import os
from dotenv import load_dotenv

# .envを読み込む
load_dotenv()

#OpenAIクライアントを作成
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

#LLMに送るリクエスト
response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "user", "content": "Pythonとは何ですか？初心者向けに説明してください。"}
    ]
)

#結果を表示
print(response.choices[0].message.content)