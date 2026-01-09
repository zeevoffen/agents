"""
Base Agent Class - Provides common functionality for all agents
"""
import json
import uuid
from abc import ABC, abstractmethod
from datetime import datetime
from typing import Any, Dict, List, Optional
from enum import Enum


class AgentRole(Enum):
    """Enumeration of agent roles"""
    RESEARCH = "research"
    ANALYSIS = "analysis"
    PLANNING = "planning"
    EXECUTION = "execution"
    COORDINATOR = "coordinator"


class Message:
    """Message structure for inter-agent communication"""
    
    def __init__(self, sender: str, recipient: str, content: str, 
                 message_type: str = "task", priority: int = 1):
        self.id = str(uuid.uuid4())
        self.sender = sender
        self.recipient = recipient
        self.content = content
        self.message_type = message_type  # "task", "result", "query", "update"
        self.priority = priority
        self.timestamp = datetime.now().isoformat()
        self.status = "pending"
        
    def to_dict(self) -> Dict:
        return {
            "id": self.id,
            "sender": self.sender,
            "recipient": self.recipient,
            "content": self.content,
            "type": self.message_type,
            "priority": self.priority,
            "timestamp": self.timestamp,
            "status": self.status
        }
    
    def __repr__(self):
        return f"Message({self.sender}→{self.recipient}: {self.content[:50]}...)"


class BaseAgent(ABC):
    """Abstract base class for all agents"""
    
    def __init__(self, name: str, role: AgentRole, expertise: List[str]):
        self.id = str(uuid.uuid4())
        self.name = name
        self.role = role
        self.expertise = expertise
        self.is_active = True
        self.task_history: List[Dict] = []
        self.inbox: List[Message] = []
        self.outbox: List[Message] = []
        self.knowledge_base: Dict[str, Any] = {}
        self.created_at = datetime.now().isoformat()
        
    @abstractmethod
    def process_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process a task and return results.
        Must be implemented by subclasses.
        """
        pass
    
    def receive_message(self, message: Message) -> None:
        """Receive a message from another agent"""
        self.inbox.append(message)
        
    def send_message(self, recipient: str, content: str, 
                    message_type: str = "result", priority: int = 1) -> Message:
        """Send a message to another agent"""
        message = Message(self.name, recipient, content, message_type, priority)
        self.outbox.append(message)
        return message
    
    def read_inbox(self) -> List[Message]:
        """Read all messages in inbox"""
        messages = self.inbox[:]
        self.inbox.clear()
        return messages
    
    def get_expertise_match(self, task_keywords: List[str]) -> float:
        """Calculate how well this agent matches task requirements (0.0 to 1.0)"""
        if not task_keywords:
            return 0.5
        
        matches = sum(1 for keyword in task_keywords if keyword.lower() in 
                     [e.lower() for e in self.expertise])
        return min(1.0, matches / len(task_keywords)) if task_keywords else 0.5
    
    def can_handle(self, task: Dict[str, Any]) -> bool:
        """Determine if this agent can handle a task"""
        required_skills = task.get("required_skills", [])
        match_score = self.get_expertise_match(required_skills)
        return match_score > 0.3
    
    def add_to_history(self, task: Dict[str, Any], result: Dict[str, Any]) -> None:
        """Add task execution to history"""
        self.task_history.append({
            "timestamp": datetime.now().isoformat(),
            "task": task,
            "result": result
        })
    
    def get_status(self) -> Dict[str, Any]:
        """Get agent status information"""
        return {
            "id": self.id,
            "name": self.name,
            "role": self.role.value,
            "expertise": self.expertise,
            "active": self.is_active,
            "tasks_completed": len(self.task_history),
            "messages_pending": len(self.inbox),
            "created_at": self.created_at
        }
    
    def __repr__(self):
        return f"{self.name}({self.role.value}, expertise: {', '.join(self.expertise)})"
