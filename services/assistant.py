from typing import List, Dict

conversation_history: List[Dict[str, str]] = []

def add_assistant_message(content: str):
    conversation_history.append({
        "role": "assistant",
        "content": content
    })

def add_user_message(content: str):
    conversation_history.append({
        "role": "user",
        "content": content
    })

def get_history(limit: int = 6) -> List[Dict[str, str]]:
    """
    直近の履歴だけ返す（暴走防止）
    """
    return conversation_history[-limit:]

def reset_histry():
    conversation_history.clear()

def build_messages(system_prompt: str, user_prompt: str):
    messages = [{"role": "system", "content": system_prompt}]
    messages.extend(get_history())
    messages.append({"role": "user", "content": user_prompt})
    return messages
