"""
Task Management Utilities
"""
from typing import Dict, List, Any
from enum import Enum


class TaskStatus(Enum):
    """Task execution status"""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    DELEGATED = "delegated"


class TaskPriority(Enum):
    """Task priority levels"""
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    CRITICAL = 4


def decompose_task(task: Dict[str, Any], depth: int = 2) -> List[Dict[str, Any]]:
    """
    Decompose a complex task into subtasks
    
    Args:
        task: Main task to decompose
        depth: How many levels deep to decompose
        
    Returns:
        List of subtasks
    """
    if depth <= 0:
        return [task]
    
    subtasks = []
    
    # Analyze task objective to identify components
    objective = task.get("objective", "").lower()
    
    # Create subtasks based on common patterns
    if "research" in objective or "analyze" in objective:
        subtasks.append({
            "name": "Information Gathering",
            "type": "research",
            "priority": TaskPriority.HIGH.value,
            "parent_task": task.get("id")
        })
        subtasks.append({
            "name": "Data Synthesis",
            "type": "analysis",
            "priority": TaskPriority.HIGH.value,
            "parent_task": task.get("id")
        })
    
    if "plan" in objective or "develop" in objective:
        subtasks.append({
            "name": "Strategy Definition",
            "type": "planning",
            "priority": TaskPriority.HIGH.value,
            "parent_task": task.get("id")
        })
        subtasks.append({
            "name": "Resource Allocation",
            "type": "planning",
            "priority": TaskPriority.MEDIUM.value,
            "parent_task": task.get("id")
        })
    
    if "implement" in objective or "execute" in objective:
        subtasks.append({
            "name": "Implementation",
            "type": "execution",
            "priority": TaskPriority.HIGH.value,
            "parent_task": task.get("id")
        })
        subtasks.append({
            "name": "Quality Assurance",
            "type": "execution",
            "priority": TaskPriority.HIGH.value,
            "parent_task": task.get("id")
        })
    
    return subtasks if subtasks else [task]


def estimate_task_complexity(task: Dict[str, Any]) -> str:
    """
    Estimate complexity of a task
    
    Returns:
        "low", "medium", or "high"
    """
    objective = task.get("objective", "").lower()
    keywords = task.get("required_skills", [])
    
    complexity_score = 0
    
    # Analyze objective length and complexity
    if len(objective) > 100:
        complexity_score += 1
    if len(keywords) > 3:
        complexity_score += 1
    
    # Check for complex keywords
    complex_keywords = ["strategy", "architecture", "design", "comprehensive", "integrate"]
    if any(kw in objective for kw in complex_keywords):
        complexity_score += 1
    
    if complexity_score >= 2:
        return "high"
    elif complexity_score == 1:
        return "medium"
    else:
        return "low"


def filter_tasks_by_status(tasks: List[Dict], status: TaskStatus) -> List[Dict]:
    """Filter tasks by status"""
    return [t for t in tasks if t.get("status") == status.value]


def merge_task_results(*results: Dict[str, Any]) -> Dict[str, Any]:
    """Merge results from multiple agents"""
    merged = {
        "combined_findings": [],
        "combined_insights": [],
        "combined_recommendations": [],
        "timestamp": None
    }
    
    for result in results:
        if "findings" in result:
            merged["combined_findings"].extend(result["findings"])
        if "insights" in result:
            merged["combined_insights"].extend(result["insights"])
        if "recommendations" in result:
            merged["combined_recommendations"].extend(result["recommendations"])
    
    return merged
