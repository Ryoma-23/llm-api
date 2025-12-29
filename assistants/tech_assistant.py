from typing import List, Dict
from models.schemas import TaskType

class TechAssistant:
    def __init__(self):
        self.system_prompt = """
あなたは技術解説専用のAIアシスタントです。

【基本方針】
- 回答は必ず日本語で行う
- 技術・IT・プログラミング以外の話題には答えない
- 雑談・感情的な慰め・個人情報は扱わない
- 結論 → 理由 → 補足 の順で簡潔に説明する
"""

        # 会話履歴（Assistant only）
        self.history: List[Dict[str, str]] = []

    # -----------------------------
    # Userプロンプト生成
    # -----------------------------
    def build_user_prompt(self, task: TaskType, user_input: str) -> str:
        if task == TaskType.EXPLAIN:
            return f"""
Task: Explain
Audience: ソフトウェア開発初心者
Constraints:
- 日本語で回答
- 結論 → 理由 → 具体例
- 専門用語は必ず噛み砕く

Question:
{user_input}
"""

        if task == TaskType.REWRITE:
            return f"""
Task: Rewrite
Constraints:
- 日本語で書き直す
- 意味は変えない
- より分かりやすく

Text:
{user_input}
"""

        if task == TaskType.SUMMARIZE:
            return f"""
Task: Summarize
Constraints:
- 日本語
- 3行以内
- 要点のみ

Text:
{user_input}
"""

        if task == TaskType.JUDGE:
            return f"""
Task: Judge
Constraints:
- 日本語
- 結論を最初に述べる
- 理由は簡潔に

Question:
{user_input}
"""

        return user_input

    def add_user_message(self, content: str):
        self.history.append({
            "role": "user",
            "content": content
        })

    # -----------------------------
    # 会話履歴管理
    # -----------------------------
    def add_assistant_message(self, content: str):
        self.history.append({
            "role": "assistant",
            "content": content
        })

        # 直近3ターンのみ保持
        self.history = self.history[-3:]

    def reset_history(self):
        self.history = []

    # -----------------------------
    # messages生成
    # -----------------------------
    def build_messages(self) -> List[Dict[str, str]]:
        messages = [
            {"role": "system", "content": self.system_prompt},
        ]

        messages.extend(self.history)

        return messages
