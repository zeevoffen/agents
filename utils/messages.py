"""
Message Handling Utilities
"""
from typing import Dict, List, Any
from agents.base import Message


def format_message(message: Message) -> str:
    """Format message for display"""
    return f"[{message.sender} → {message.recipient}] {message.content}"


def filter_messages_by_type(messages: List[Message], 
                          message_type: str) -> List[Message]:
    """Filter messages by type"""
    return [m for m in messages if m.message_type == message_type]


def filter_messages_by_priority(messages: List[Message], 
                               min_priority: int = 1) -> List[Message]:
    """Filter messages by minimum priority"""
    return [m for m in messages if m.priority >= min_priority]


def sort_messages_by_priority(messages: List[Message]) -> List[Message]:
    """Sort messages by priority (highest first)"""
    return sorted(messages, key=lambda m: m.priority, reverse=True)


def create_message_summary(messages: List[Message]) -> Dict[str, Any]:
    """Create a summary of messages"""
    return {
        "total_messages": len(messages),
        "by_type": {
            "task": len([m for m in messages if m.message_type == "task"]),
            "result": len([m for m in messages if m.message_type == "result"]),
            "query": len([m for m in messages if m.message_type == "query"]),
            "update": len([m for m in messages if m.message_type == "update"])
        },
        "by_priority": {
            "high": len([m for m in messages if m.priority >= 3]),
            "medium": len([m for m in messages if m.priority == 2]),
            "low": len([m for m in messages if m.priority == 1])
        },
        "pending": len([m for m in messages if m.status == "pending"])
    }
