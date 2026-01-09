"""
Planning Agent - Creates actionable plans and strategies
"""
from typing import Any, Dict, List
from agents.base import BaseAgent, AgentRole


class PlanningAgent(BaseAgent):
    """Agent specialized in planning and strategy development"""
    
    def __init__(self, name: str = "Planning Agent"):
        expertise = ["strategic planning", "roadmap development", "risk management",
                    "resource allocation", "timeline estimation", "milestone definition"]
        super().__init__(name, AgentRole.PLANNING, expertise)
        
        self.knowledge_base = {
            "planning_methodologies": ["Agile", "Waterfall", "Lean", "Kanban"],
            "risk_categories": ["technical", "market", "operational", "financial"],
            "timeline_estimation": ["story points", "t-shirt sizing", "critical path method"]
        }
        
    def process_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process a planning task and create actionable plans
        """
        objective = task.get("objective", "")
        constraints = task.get("constraints", {})
        resources = task.get("available_resources", [])
        insights = task.get("insights", [])
        
        # Create strategic plan
        strategic_plan = self._create_strategic_plan(objective, insights)
        roadmap = self._create_roadmap(objective, constraints)
        risk_mitigation = self._identify_risks_and_mitigation(objective)
        resource_plan = self._allocate_resources(resources, roadmap)
        
        result = {
            "status": "completed",
            "agent": self.name,
            "objective": objective,
            "strategic_plan": strategic_plan,
            "roadmap": roadmap,
            "risk_mitigation": risk_mitigation,
            "resource_allocation": resource_plan,
            "confidence": 0.80,
            "timeline": self._estimate_timeline(roadmap)
        }
        
        self.add_to_history(task, result)
        return result
    
    def _create_strategic_plan(self, objective: str, 
                              insights: List[Dict]) -> Dict[str, Any]:
        """Create strategic plan based on objective and insights"""
        plan = {
            "vision": f"Successfully achieve: {objective}",
            "strategy": "Multi-phase approach focusing on quick wins followed by long-term optimization",
            "success_criteria": [
                "Achieve primary objective within timeline",
                "Maintain quality standards",
                "Stay within resource constraints",
                "Minimize identified risks"
            ],
            "key_success_factors": [
                "Executive alignment and support",
                "Cross-functional team coordination",
                "Regular progress monitoring and adaptation",
                "Stakeholder communication"
            ]
        }
        return plan
    
    def _create_roadmap(self, objective: str, constraints: Dict) -> List[Dict[str, Any]]:
        """Create detailed roadmap with phases"""
        roadmap = [
            {
                "phase": 1,
                "name": "Planning & Preparation",
                "duration": "2 weeks",
                "milestones": [
                    "Define detailed requirements",
                    "Set up team and resources",
                    "Create detailed task breakdown"
                ],
                "owner": "Planning Agent",
                "status": "planned"
            },
            {
                "phase": 2,
                "name": "Implementation",
                "duration": "6-8 weeks",
                "milestones": [
                    "Core functionality development",
                    "Integration and testing",
                    "Optimization"
                ],
                "owner": "Execution Agent",
                "status": "planned"
            },
            {
                "phase": 3,
                "name": "Validation & Launch",
                "duration": "2-3 weeks",
                "milestones": [
                    "Final testing and QA",
                    "Stakeholder review",
                    "Launch and monitoring"
                ],
                "owner": "Execution Agent",
                "status": "planned"
            },
            {
                "phase": 4,
                "name": "Optimization",
                "duration": "Ongoing",
                "milestones": [
                    "Monitor performance",
                    "Gather feedback",
                    "Continuous improvement"
                ],
                "owner": "Analysis Agent",
                "status": "planned"
            }
        ]
        return roadmap
    
    def _identify_risks_and_mitigation(self, objective: str) -> List[Dict[str, Any]]:
        """Identify risks and create mitigation strategies"""
        risks = [
            {
                "risk": "Resource constraints",
                "probability": "medium",
                "impact": "high",
                "mitigation": "Prioritize critical path items, consider resource augmentation",
                "owner": "Planning Agent"
            },
            {
                "risk": "Scope creep",
                "probability": "high",
                "impact": "medium",
                "mitigation": "Strict change control, regular scope reviews",
                "owner": "Planning Agent"
            },
            {
                "risk": "Technical challenges",
                "probability": "medium",
                "impact": "medium",
                "mitigation": "Proof of concepts for critical technologies, expert consultation",
                "owner": "Execution Agent"
            },
            {
                "risk": "Timeline delays",
                "probability": "medium",
                "impact": "high",
                "mitigation": "Buffer time, weekly status reviews, adaptive scheduling",
                "owner": "Planning Agent"
            }
        ]
        return risks
    
    def _allocate_resources(self, resources: List[str], 
                           roadmap: List[Dict]) -> Dict[str, Any]:
        """Allocate resources across roadmap phases"""
        allocation = {
            "total_resources_needed": len(roadmap) * 3,  # Simplified calculation
            "allocation_by_phase": [],
            "critical_resources": ["Project Manager", "Lead Developer", "QA Engineer"],
            "recommendations": [
                "Allocate planning resources early for requirements clarity",
                "Concentrate development resources during implementation phase",
                "Ensure QA coverage throughout all phases",
                "Maintain contingency (20% buffer) for unexpected issues"
            ]
        }
        
        for phase in roadmap:
            allocation["allocation_by_phase"].append({
                "phase": phase["phase"],
                "resources": 3,
                "criticality": "high" if phase["phase"] <= 2 else "medium"
            })
        
        return allocation
    
    def _estimate_timeline(self, roadmap: List[Dict]) -> Dict[str, Any]:
        """Estimate overall timeline"""
        total_weeks = 12  # Simplified estimate
        return {
            "total_duration": "12-14 weeks",
            "phases": len(roadmap),
            "critical_path": "Implementation phase",
            "buffer": "2 weeks contingency",
            "expected_completion": "Q2 2026"
        }
