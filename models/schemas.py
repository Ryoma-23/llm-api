from pydantic import BaseModel
from enum import Enum

# -----------------------------
# リクエストボディ
# -----------------------------
class ChatRequest(BaseModel):
    message: str


# -----------------------------
# Task種別
# -----------------------------
class TaskType(str, Enum):
    EXPLAIN = "Explain"
    REWRITE = "Rewrite"
    SUMMARIZE = "Summarize"
    JUDGE = "Judge"
