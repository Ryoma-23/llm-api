from services.task_detector import TaskType

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