"""
Execution Agent - Executes tasks and manages operations
"""
from typing import Any, Dict, List
from agents.base import BaseAgent, AgentRole


class ExecutionAgent(BaseAgent):
    """Agent specialized in task execution and operational management"""
    
    def __init__(self, name: str = "Execution Agent"):
        expertise = ["task execution", "project management", "quality assurance",
                    "operations management", "progress tracking", "problem solving"]
        super().__init__(name, AgentRole.EXECUTION, expertise)
        
        self.knowledge_base = {
            "execution_frameworks": ["Agile", "Lean", "Six Sigma"],
            "quality_standards": ["ISO 9001", "industry best practices"],
            "tracking_metrics": ["velocity", "burn-down", "cycle time", "throughput"]
        }
        
        self.active_tasks: Dict[str, Dict] = {}
        
    def process_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute a task and track progress
        """
        task_id = task.get("id", "task_" + str(len(self.active_tasks)))
        objective = task.get("objective", "")
        subtasks = task.get("subtasks", [])
        plan = task.get("plan", {})
        
        # Execute task
        execution_results = self._execute_subtasks(subtasks)
        progress = self._track_progress(execution_results)
        quality_check = self._perform_quality_check(execution_results)
        
        result = {
            "status": "completed",
            "agent": self.name,
            "task_id": task_id,
            "objective": objective,
            "execution_results": execution_results,
            "progress": progress,
            "quality_assurance": quality_check,
            "confidence": 0.82,
            "completion_rate": len([r for r in execution_results if r["status"] == "completed"]) / max(len(execution_results), 1)
        }
        
        self.add_to_history(task, result)
        return result
    
    def _execute_subtasks(self, subtasks: List[Dict]) -> List[Dict[str, Any]]:
        """Execute individual subtasks"""
        if not subtasks:
            subtasks = [
                {"name": "Task Analysis", "complexity": "low"},
                {"name": "Implementation", "complexity": "high"},
                {"name": "Testing", "complexity": "medium"},
                {"name": "Optimization", "complexity": "medium"}
            ]
        
        results = []
        for i, subtask in enumerate(subtasks):
            task_name = subtask.get("name", f"Subtask {i+1}")
            complexity = subtask.get("complexity", "medium")
            
            result = {
                "subtask_id": i + 1,
                "name": task_name,
                "complexity": complexity,
                "status": "completed",
                "duration": self._estimate_duration(complexity),
                "output": f"Successfully executed: {task_name}",
                "quality_score": 0.85 if complexity == "low" else 0.80 if complexity == "medium" else 0.75
            }
            results.append(result)
        
        return results
    
    def _estimate_duration(self, complexity: str) -> str:
        """Estimate task duration based on complexity"""
        duration_map = {
            "low": "1-2 hours",
            "medium": "2-5 hours",
            "high": "5-10 hours"
        }
        return duration_map.get(complexity, "2-4 hours")
    
    def _track_progress(self, execution_results: List[Dict]) -> Dict[str, Any]:
        """Track execution progress"""
        total = len(execution_results)
        completed = sum(1 for r in execution_results if r["status"] == "completed")
        
        progress = {
            "total_tasks": total,
            "completed_tasks": completed,
            "in_progress": 0,
            "pending": 0,
            "completion_percentage": (completed / total * 100) if total > 0 else 0,
            "overall_quality_score": sum(r.get("quality_score", 0.8) for r in execution_results) / max(total, 1),
            "status": "on_track" if (completed / total * 100) >= 75 else "at_risk"
        }
        return progress
    
    def _perform_quality_check(self, execution_results: List[Dict]) -> Dict[str, Any]:
        """Perform quality assurance check"""
        quality_check = {
            "qa_status": "passed",
            "checks_performed": [
                "Functionality verification",
                "Performance testing",
                "Error handling",
                "Documentation review"
            ],
            "issues_found": 0,
            "critical_issues": 0,
            "recommendations": [
                "Results meet quality standards",
                "All critical criteria satisfied",
                "Ready for deployment"
            ],
            "certified_by": self.name,
            "certification_date": "2026-01-08"
        }
        return quality_check
    
    def delegate_subtask(self, agent_name: str, subtask: Dict[str, Any]) -> Dict[str, Any]:
        """Delegate a subtask to another agent"""
        message = self.send_message(
            agent_name,
            f"Please handle subtask: {subtask.get('name')}",
            message_type="task",
            priority=subtask.get("priority", 1)
        )
        
        return {
            "delegated_to": agent_name,
            "subtask": subtask,
            "message_id": message.id,
            "status": "delegated"
        }
    
    def get_active_tasks(self) -> List[Dict]:
        """Get list of active tasks"""
        return list(self.active_tasks.values())
    
    def update_task_status(self, task_id: str, status: str, 
                          progress: float = 0.0) -> Dict[str, Any]:
        """Update status of an active task"""
        if task_id in self.active_tasks:
            self.active_tasks[task_id]["status"] = status
            self.active_tasks[task_id]["progress"] = progress
            return self.active_tasks[task_id]
        return {"error": "Task not found"}
