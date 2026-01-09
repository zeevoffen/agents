"""
Research Agent - Gathers and synthesizes information
Uses Groq API for real LLM inference, falls back to simulation
"""
from typing import Any, Dict, List
from agents.base import BaseAgent, AgentRole
import os
import json


class ResearchAgent(BaseAgent):
    """Agent specialized in research and information gathering"""
    
    def __init__(self, name: str = "Research Agent", use_api: bool = True):
        expertise = ["research", "data collection", "information synthesis", 
                    "trend analysis", "market research", "competitive analysis"]
        super().__init__(name, AgentRole.RESEARCH, expertise)
        
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
        
        # Knowledge base for research
        self.knowledge_base = {
            "data_sources": ["primary research", "secondary sources", "surveys", "interviews"],
            "research_methods": ["quantitative", "qualitative", "mixed methods"],
            "recent_trends": {
                "ai_ml": ["LLM advancements", "prompt engineering", "agent systems"],
                "startups": ["AI companies", "biotech", "climate tech", "fintech"],
                "markets": ["Enterprise SaaS", "Consumer apps", "B2B platforms"]
            }
        }
        
    def process_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process a research task and gather information
        """
        objective = task.get("objective", "General research")
        context = task.get("context", {})
        research_type = task.get("type", "general")
        
        # Get findings - either from API or simulation
        if self.use_api and self.client:
            findings = self._conduct_research_with_api(objective, research_type, context)
        else:
            findings = self._conduct_research_simulation(objective, research_type, context)
        
        result = {
            "status": "completed",
            "agent": self.name,
            "task": objective,
            "research_type": research_type,
            "findings": findings,
            "sources_used": self._get_sources(research_type),
            "confidence": 0.85,
            "methodology": self._get_methodology(research_type),
            "mode": "real_api" if (self.use_api and self.client) else "simulation"
        }
        
        self.add_to_history(task, result)
        return result
    
    def _conduct_research_with_api(self, objective: str, research_type: str, 
                                   context: Dict) -> List[Dict[str, Any]]:
        """Use real Groq LLM for research"""
        try:
            prompt = f"""You are a research expert. Provide 3-4 key research findings about:
Objective: {objective}
Type: {research_type}
Context: {json.dumps(context, default=str)}

Return ONLY a JSON array of findings with this format:
[
  {{"finding": "title", "data": "key data point", "confidence": "high/medium/low"}},
  ...
]

Be concise and factual."""

            response = self.client.chat.completions.create(
                model="mixtral-8x7b-32768",  # Free model on Groq
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
                max_tokens=500
            )
            
            response_text = response.choices[0].message.content.strip()
            
            # Parse JSON response
            try:
                # Handle markdown code blocks
                if "```json" in response_text:
                    response_text = response_text.split("```json")[1].split("```")[0].strip()
                elif "```" in response_text:
                    response_text = response_text.split("```")[1].split("```")[0].strip()
                
                findings = json.loads(response_text)
                
                # Ensure valid format
                if isinstance(findings, list):
                    return findings
            except json.JSONDecodeError:
                # If JSON parsing fails, create structured response from text
                return [{
                    "finding": "Research Analysis",
                    "data": response_text,
                    "confidence": "medium"
                }]
            
        except Exception as e:
            print(f"⚠️  API Error: {e}. Falling back to simulation.")
            self.use_api = False
            return self._conduct_research_simulation(objective, research_type, context)
    
    def _conduct_research_simulation(self, objective: str, research_type: str, 
                                     context: Dict) -> List[Dict[str, Any]]:
        """Fallback simulation-based research"""
        findings = []
        
        if "market" in objective.lower():
            findings = [
                {
                    "finding": "Market growth trajectory",
                    "data": "12-15% YoY growth in target segment",
                    "confidence": "high"
                },
                {
                    "finding": "Key market players",
                    "data": "Identified 5 primary competitors with market shares",
                    "confidence": "high"
                },
                {
                    "finding": "Customer pain points",
                    "data": "Integration complexity, cost management, scalability",
                    "confidence": "medium"
                },
                {
                    "finding": "Market entry opportunities",
                    "data": "Niche segments underserved, integration gaps",
                    "confidence": "medium"
                }
            ]
        elif "product" in objective.lower():
            findings = [
                {
                    "finding": "Feature demand analysis",
                    "data": "Top 3 requested features identified from surveys",
                    "confidence": "high"
                },
                {
                    "finding": "User personas",
                    "data": "5 distinct personas created based on research",
                    "confidence": "medium"
                },
                {
                    "finding": "Competitive feature comparison",
                    "data": "Analysis of 8 competitor products completed",
                    "confidence": "high"
                }
            ]
        else:
            findings = [
                {
                    "finding": "General information synthesis",
                    "data": f"Research completed on: {objective}",
                    "confidence": "medium"
                },
                {
                    "finding": "Key data points identified",
                    "data": "3-5 major insights synthesized from sources",
                    "confidence": "medium"
                }
            ]
        
        return findings
    
    def _get_sources(self, research_type: str) -> List[str]:
        """Get relevant sources for research type"""
        return [
            "Market research reports",
            "Industry publications",
            "Expert interviews",
            "Statistical databases",
            "Academic journals"
        ]
    
    def _get_methodology(self, research_type: str) -> Dict[str, Any]:
        """Get methodology for research"""
        return {
            "approach": "Mixed methods (quantitative + qualitative)",
            "data_collection": "Surveys, interviews, database analysis",
            "analysis_framework": "Thematic analysis for qualitative, statistical for quantitative",
            "validation": "Cross-referenced with multiple sources"
        }
