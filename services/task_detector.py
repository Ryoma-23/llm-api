from enum import Enum

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

    return TaskType.EXPLAIN
