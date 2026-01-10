"""
Planning Agent - Creates actionable plans and strategies
Uses Groq API for real LLM inference, falls back to simulation
"""
from typing import Any, Dict, List
from agents.base import BaseAgent, AgentRole
import os
import json


class PlanningAgent(BaseAgent):
    """Agent specialized in planning and strategy development"""
    
    def __init__(self, name: str = "Planning Agent", use_api: bool = True):
        expertise = ["strategic planning", "roadmap development", "risk management",
                    "resource allocation", "timeline estimation", "milestone definition"]
        super().__init__(name, AgentRole.PLANNING, expertise)
        
        self.use_api = use_api
        self.api_key = os.getenv("GROQ_API_KEY")
        
        # Try to use API, fallback to simulation if not available
        if use_api and not self.api_key:
            print(f"⚠️  No GROQ_API_KEY found. Set it to use real LLM: export GROQ_API_KEY='your-key'")
            self.use_api = False
        
        if self.use_api:
            try:
                from groq import Groq
                self.client = Groq(api_key=self.api_key)
                print(f"✓ {self.name} using real Groq LLM API")
            except ImportError:
                print(f"⚠️  groq package not installed. Install: pip install groq")
                self.use_api = False
                self.client = None
        else:
            print(f"ℹ️  {self.name} using simulation mode (offline)")
            self.client = None
        
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
        
        # Create strategic plan - either from API or simulation
        if self.use_api and self.client:
            strategic_plan = self._create_plan_with_api(objective, constraints, insights)
        else:
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
            "timeline": self._estimate_timeline(roadmap),
            "mode": "real_api" if (self.use_api and self.client) else "simulation"
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
    
    def _create_plan_with_api(self, objective: str, constraints: Dict, 
                             insights: List[Dict]) -> Dict[str, Any]:
        """Use real Groq LLM for plan creation"""
        try:
            prompt = f"""You are a strategic planning expert. Create a detailed strategic plan for:
Objective: {objective}
Constraints: {json.dumps(constraints, default=str)}
Key Insights: {json.dumps(insights, default=str)}

Return ONLY a JSON object with this format:
{{
  "vision": "clear vision statement",
  "strategy": "high-level strategy",
  "success_criteria": ["criterion1", "criterion2", ...],
  "key_success_factors": ["factor1", "factor2", ...],
  "critical_risks": ["risk1", "risk2", ...],
  "implementation_approach": "how to implement"
}}

Be concise and strategic."""

            response = self.client.chat.completions.create(
                model="mixtral-8x7b-32768",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
                max_tokens=800
            )
            
            response_text = response.choices[0].message.content.strip()
            
            # Parse JSON response
            try:
                if "```json" in response_text:
                    response_text = response_text.split("```json")[1].split("```")[0].strip()
                elif "```" in response_text:
                    response_text = response_text.split("```")[1].split("```")[0].strip()
                
                plan = json.loads(response_text)
                return plan
            except json.JSONDecodeError:
                return {"vision": response_text, "strategy": "LLM-generated strategy"}
            
        except Exception as e:
            print(f"⚠️  API Error: {e}. Falling back to simulation.")
            self.use_api = False
            return self._create_strategic_plan(objective, insights)
    
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
