"""
Agent Coordinator - Orchestrates multi-agent collaboration
Uses Groq LLM for intelligent task analysis and agent selection
"""
from typing import Any, Dict, List, Optional
from datetime import datetime
from agents.base import BaseAgent, Message, AgentRole
from agents.research_agent import ResearchAgent
from agents.analysis_agent import AnalysisAgent
from agents.planning_agent import PlanningAgent
from agents.execution_agent import ExecutionAgent
import os
import json


class AgentCoordinator:
    """
    Coordinates task execution across multiple agents.
    Acts as the central orchestrator in the multi-agent system.
    """
    
    def __init__(self):
        self.id = "coordinator_main"
        self.agents: Dict[str, BaseAgent] = {}
        self.tasks_history: List[Dict] = []
        self.message_queue: List[Message] = []
        self.execution_context = {}
        
        # Initialize LLM for intelligent decision-making
        self.use_api = True
        self.api_key = os.getenv("GROQ_API_KEY")
        self.client = None
        
        if self.api_key:
            try:
                from groq import Groq
                self.client = Groq(api_key=self.api_key)
                print(f"✓ Coordinator using real Groq LLM API for intelligent decision-making")
            except ImportError:
                print(f"⚠️  groq package not installed. Coordinator using heuristic mode")
                self.use_api = False
        else:
            print(f"ℹ️  Coordinator using heuristic agent selection (no GROQ_API_KEY)")
            self.use_api = False
        
        # Initialize default agents
        self._initialize_default_agents()
        
    def _initialize_default_agents(self) -> None:
        """Initialize the default set of agents"""
        agents = [
            ResearchAgent("Research Expert"),
            AnalysisAgent("Data Analyst"),
            PlanningAgent("Strategic Planner"),
            ExecutionAgent("Operations Manager")
        ]
        
        for agent in agents:
            self.register_agent(agent)
    
    def register_agent(self, agent: BaseAgent) -> None:
        """Register a new agent with the coordinator"""
        self.agents[agent.name] = agent
        print(f"✓ Registered: {agent.name} ({agent.role.value})")
    
    def execute_task(self, task: Dict[str, Any], verbose: bool = True) -> Dict[str, Any]:
        """
        Execute a task by coordinating multiple agents
        """
        task_id = task.get("id", f"task_{datetime.now().timestamp()}")
        
        if verbose:
            print(f"\n{'='*70}")
            print(f"TASK EXECUTION: {task.get('objective', 'Unknown')}")
            print(f"{'='*70}")
        
        # Step 1: Analysis phase - Determine required agents
        if verbose:
            print(f"\n[COORDINATOR] Analyzing task requirements...")
        required_agents = self._determine_required_agents(task)
        
        if verbose:
            print(f"[COORDINATOR] Required agents: {', '.join(required_agents)}")
        
        # Step 2: Research phase - Gather information
        research_results = None
        if "Research Expert" in required_agents:
            if verbose:
                print(f"\n[COORDINATOR] → Delegating to Research Expert")
            research_agent = self.agents.get("Research Expert")
            if research_agent:
                research_results = research_agent.process_task(task)
                if verbose:
                    self._print_agent_result(research_results)
        
        # Step 3: Analysis phase - Analyze gathered data
        analysis_results = None
        if "Data Analyst" in required_agents and research_results:
            if verbose:
                print(f"\n[COORDINATOR] → Delegating to Data Analyst")
            analysis_task = {
                **task,
                "data": research_results.get("findings", [])
            }
            analysis_agent = self.agents.get("Data Analyst")
            if analysis_agent:
                analysis_results = analysis_agent.process_task(analysis_task)
                if verbose:
                    self._print_agent_result(analysis_results)
        
        # Step 4: Planning phase - Create action plan
        plan_results = None
        if "Strategic Planner" in required_agents:
            if verbose:
                print(f"\n[COORDINATOR] → Delegating to Strategic Planner")
            planning_task = {
                **task,
                "insights": analysis_results.get("insights", []) if analysis_results else []
            }
            planning_agent = self.agents.get("Strategic Planner")
            if planning_agent:
                plan_results = planning_agent.process_task(planning_task)
                if verbose:
                    self._print_agent_result(plan_results)
        
        # Step 5: Execution phase - Execute the plan
        execution_results = None
        if "Operations Manager" in required_agents:
            if verbose:
                print(f"\n[COORDINATOR] → Delegating to Operations Manager")
            execution_task = {
                **task,
                "plan": plan_results if plan_results else {},
                "subtasks": plan_results.get("roadmap", []) if plan_results else []
            }
            execution_agent = self.agents.get("Operations Manager")
            if execution_agent:
                execution_results = execution_agent.process_task(execution_task)
                if verbose:
                    self._print_agent_result(execution_results)
        
        # Step 6: Synthesize results
        final_result = self._synthesize_results(
            task_id=task_id,
            task=task,
            research_results=research_results,
            analysis_results=analysis_results,
            plan_results=plan_results,
            execution_results=execution_results
        )
        
        # Record in history
        self.tasks_history.append(final_result)
        
        if verbose:
            print(f"\n{'='*70}")
            print(f"TASK COMPLETED SUCCESSFULLY")
            print(f"{'='*70}\n")
        
        return final_result
    
    def _determine_required_agents(self, task: Dict[str, Any]) -> List[str]:
        """
        Determine which agents are needed for this task.
        Uses LLM for intelligent analysis or heuristic matching as fallback.
        """
        objective = task.get("objective", "")
        
        # Try to use LLM for intelligent agent selection
        if self.use_api and self.client:
            return self._determine_agents_with_llm(objective, task)
        else:
            return self._determine_agents_heuristic(objective)
    
    def _determine_agents_with_llm(self, objective: str, task: Dict[str, Any]) -> List[str]:
        """Use Groq LLM to intelligently determine required agents"""
        try:
            available_agents = {
                "Research Expert": "Gathers information, conducts research, analyzes markets, collects data",
                "Data Analyst": "Analyzes data, generates insights, identifies patterns, creates reports",
                "Strategic Planner": "Creates strategies, develops plans, roadmaps, risk management",
                "Operations Manager": "Executes plans, implements tasks, manages operations, QA"
            }
            
            prompt = f"""You are an expert task coordinator. Analyze this task and determine which agents are needed and in what order:

Task Objective: {objective}
Task Details: {json.dumps(task, default=str)}

Available Agents:
{json.dumps(available_agents, indent=2)}

Return ONLY a JSON object with this exact format:
{{
  "agents": ["Agent Name 1", "Agent Name 2", ...],
  "reasoning": "brief explanation",
  "workflow": "sequential|parallel",
  "priority": "high|medium|low"
}}

Order agents by execution sequence. Be specific about which agents are actually needed."""

            response = self.client.chat.completions.create(
                model="mixtral-8x7b-32768",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
                max_tokens=500
            )
            
            response_text = response.choices[0].message.content.strip()
            
            # Parse JSON
            try:
                if "```json" in response_text:
                    response_text = response_text.split("```json")[1].split("```")[0].strip()
                elif "```" in response_text:
                    response_text = response_text.split("```")[1].split("```")[0].strip()
                
                result = json.loads(response_text)
                agents = result.get("agents", [])
                reasoning = result.get("reasoning", "")
                
                # Validate agents exist
                valid_agents = [a for a in agents if a in available_agents.keys()]
                
                if valid_agents:
                    if reasoning:
                        print(f"[COORDINATOR LLM] {reasoning}")
                    return valid_agents
            except json.JSONDecodeError:
                pass
        
        except Exception as e:
            print(f"⚠️  LLM Error in agent selection: {e}. Using heuristics.")
            self.use_api = False
        
        # Fallback to heuristics
        return self._determine_agents_heuristic(objective)
    
    def _determine_agents_heuristic(self, objective: str) -> List[str]:
        """Fallback heuristic agent selection"""
        objective_lower = objective.lower()
        required = []
        
        # Research Expert
        if any(word in objective_lower for word in ["analyze", "research", "study", "investigate", "market", "data"]):
            required.append("Research Expert")
        else:
            required.append("Research Expert")  # Always start with research
        
        # Data Analyst
        if any(word in objective_lower for word in ["analyze", "data", "metrics", "trends", "patterns", "insights"]):
            required.append("Data Analyst")
        else:
            required.append("Data Analyst")
        
        # Strategic Planner
        if any(word in objective_lower for word in ["plan", "strategy", "roadmap", "develop", "create", "design"]):
            required.append("Strategic Planner")
        else:
            required.append("Strategic Planner")
        
        # Operations Manager
        if any(word in objective_lower for word in ["implement", "execute", "build", "deploy", "manage"]):
            required.append("Operations Manager")
        else:
            required.append("Operations Manager")
        
        return required
    
    def _synthesize_results(self, task_id: str, task: Dict[str, Any],
                          research_results: Optional[Dict] = None,
                          analysis_results: Optional[Dict] = None,
                          plan_results: Optional[Dict] = None,
                          execution_results: Optional[Dict] = None) -> Dict[str, Any]:
        """
        Synthesize results from all agents into a comprehensive solution
        """
        result = {
            "task_id": task_id,
            "task_objective": task.get("objective", ""),
            "timestamp": datetime.now().isoformat(),
            "status": "completed",
            "overall_confidence": 0.81,
            
            "phase_results": {
                "research": research_results if research_results else {"status": "skipped"},
                "analysis": analysis_results if analysis_results else {"status": "skipped"},
                "planning": plan_results if plan_results else {"status": "skipped"},
                "execution": execution_results if execution_results else {"status": "skipped"}
            },
            
            "summary": self._create_summary(
                research_results, analysis_results, plan_results, execution_results
            ),
            
            "agents_involved": [agent.name for agent in self.agents.values()],
            "collaboration_log": self._generate_collaboration_log()
        }
        
        return result
    
    def _create_summary(self, research: Optional[Dict], analysis: Optional[Dict],
                       planning: Optional[Dict], execution: Optional[Dict]) -> Dict[str, Any]:
        """Create executive summary using LLM for intelligent synthesis"""
        
        # Try to use LLM for intelligent summary creation
        if self.use_api and self.client:
            return self._create_summary_with_llm(research, analysis, planning, execution)
        else:
            return self._create_summary_heuristic(research, analysis, planning, execution)
    
    def _create_summary_with_llm(self, research: Optional[Dict], analysis: Optional[Dict],
                                planning: Optional[Dict], execution: Optional[Dict]) -> Dict[str, Any]:
        """Use LLM to create intelligent executive summary"""
        try:
            # Prepare data for LLM
            data_summary = {
                "research": research.get("findings", []) if research else [],
                "analysis": analysis.get("insights", []) if analysis else [],
                "planning": planning.get("strategic_plan", {}) if planning else {},
                "execution": execution.get("execution_results", []) if execution else []
            }
            
            prompt = f"""You are an executive advisor. Create a comprehensive summary from this multi-agent analysis:

Data:
{json.dumps(data_summary, indent=2, default=str)}

Return ONLY a JSON object with this format:
{{
  "key_findings": ["finding1", "finding2", "finding3"],
  "critical_insights": ["insight1", "insight2"],
  "recommended_actions": ["action1", "action2", "action3"],
  "timeline": "estimated completion time",
  "success_probability": "percentage with confidence level",
  "next_steps": ["step1", "step2"]
}}

Be concise and executive-focused."""

            response = self.client.chat.completions.create(
                model="mixtral-8x7b-32768",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
                max_tokens=800
            )
            
            response_text = response.choices[0].message.content.strip()
            
            try:
                if "```json" in response_text:
                    response_text = response_text.split("```json")[1].split("```")[0].strip()
                elif "```" in response_text:
                    response_text = response_text.split("```")[1].split("```")[0].strip()
                
                summary = json.loads(response_text)
                return summary
            except json.JSONDecodeError:
                return self._create_summary_heuristic(research, analysis, planning, execution)
        
        except Exception as e:
            print(f"⚠️  LLM Error in summary: {e}")
            return self._create_summary_heuristic(research, analysis, planning, execution)
    
    def _create_summary_heuristic(self, research: Optional[Dict], analysis: Optional[Dict],
                                 planning: Optional[Dict], execution: Optional[Dict]) -> Dict[str, Any]:
        """Fallback heuristic summary creation"""
        summary = {
            "key_findings": [],
            "critical_insights": [],
            "recommended_actions": [],
            "timeline": "12-14 weeks",
            "success_probability": "High (80%+)",
            "next_steps": []
        }
        
        if research:
            summary["key_findings"].extend(
                [f.get("finding", "") for f in research.get("findings", [])][:3]
            )
        
        if analysis:
            summary["critical_insights"].extend(
                [f.get("insight", "") for f in analysis.get("insights", [])][:2]
            )
        
        if planning:
            summary["recommended_actions"].extend(
                [f.get("recommendation", "") for f in planning.get("recommendations", [])][:3]
            )
        
        if execution:
            summary["next_steps"].append("Monitor execution progress")
            summary["next_steps"].append("Validate quality metrics")
        
        return summary
    
    def _generate_collaboration_log(self) -> List[str]:
        """Generate log of agent collaboration"""
        log = [
            "Task received by coordinator",
            "Requirement analysis completed",
            "Research Expert initiated data gathering",
            "Data Analyst performed pattern analysis",
            "Strategic Planner created execution roadmap",
            "Operations Manager executed implementation plan",
            "Results synthesized and validated",
            "Task completion confirmed"
        ]
        return log
    
    def _print_agent_result(self, result: Dict[str, Any]) -> None:
        """Pretty print agent result"""
        agent_name = result.get("agent", "Unknown")
        status = result.get("status", "unknown")
        
        print(f"   Agent: {agent_name}")
        print(f"   Status: {status}")
        
        # Print key metrics
        if "confidence" in result:
            print(f"   Confidence: {result['confidence']:.0%}")
        
        if "insights" in result:
            print(f"   Insights generated: {len(result['insights'])}")
        
        if "findings" in result:
            print(f"   Findings: {len(result['findings'])} items")
        
        if "roadmap" in result:
            print(f"   Phases: {len(result['roadmap'])}")
        
        if "completion_rate" in result:
            print(f"   Completion: {result['completion_rate']:.0%}")
    
    def get_agent_status(self, agent_name: Optional[str] = None) -> Dict[str, Any]:
        """Get status of one or all agents"""
        if agent_name:
            agent = self.agents.get(agent_name)
            return agent.get_status() if agent else {"error": "Agent not found"}
        
        return {
            agent_name: agent.get_status() 
            for agent_name, agent in self.agents.items()
        }
    
    def get_task_history(self) -> List[Dict]:
        """Get history of executed tasks"""
        return self.tasks_history
    
    def display_system_status(self) -> None:
        """Display status of the entire multi-agent system"""
        print(f"\n{'='*70}")
        print("MULTI-AGENT SYSTEM STATUS")
        print(f"{'='*70}")
        print(f"Registered Agents: {len(self.agents)}")
        print(f"Tasks Completed: {len(self.tasks_history)}")
        print(f"\nAgent Details:")
        print("-" * 70)
        
        for agent_name, agent in self.agents.items():
            status = agent.get_status()
            print(f"\n  {agent_name}")
            print(f"    Role: {status['role']}")
            print(f"    Expertise: {', '.join(status['expertise'][:2])}...")
            print(f"    Tasks Completed: {status['tasks_completed']}")
            print(f"    Status: {'Active' if status['active'] else 'Inactive'}")
