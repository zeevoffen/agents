"""
Example: Creating and Using Custom Agents
Demonstrates how to extend the multi-agent system with new specialized agents
"""
from agents.base import BaseAgent, AgentRole
from agents.coordinator import AgentCoordinator


class DataScientistAgent(BaseAgent):
    """Custom agent specialized in data science and ML tasks"""
    
    def __init__(self, name: str = "Data Scientist"):
        expertise = [
            "machine learning", "statistical modeling", "data science",
            "model development", "AI/ML", "deep learning"
        ]
        super().__init__(name, AgentRole.ANALYSIS, expertise)
        
        self.knowledge_base = {
            "ml_frameworks": ["scikit-learn", "TensorFlow", "PyTorch"],
            "model_types": ["classification", "regression", "clustering", "neural_networks"],
            "evaluation_metrics": ["accuracy", "precision", "recall", "F1-score", "AUC"]
        }
    
    def process_task(self, task):
        """Process ML/data science tasks"""
        objective = task.get("objective", "")
        
        result = {
            "status": "completed",
            "agent": self.name,
            "task": objective,
            "models_trained": 3,
            "best_model": "Random Forest Classifier",
            "accuracy": 0.94,
            "precision": 0.92,
            "recall": 0.91,
            "f1_score": 0.915,
            "recommendations": [
                "Model shows strong predictive power",
                "Feature engineering improved accuracy by 12%",
                "Consider ensemble methods for further improvement",
                "Hyperparameter tuning recommended for production"
            ],
            "confidence": 0.88
        }
        
        self.add_to_history(task, result)
        return result


class CustomerServiceAgent(BaseAgent):
    """Custom agent for customer service and support tasks"""
    
    def __init__(self, name: str = "Customer Service Manager"):
        expertise = [
            "customer support", "issue resolution", "communication",
            "complaint handling", "customer satisfaction", "service quality"
        ]
        super().__init__(name, AgentRole.EXECUTION, expertise)
    
    def process_task(self, task):
        """Process customer service tasks"""
        objective = task.get("objective", "")
        
        result = {
            "status": "completed",
            "agent": self.name,
            "task": objective,
            "tickets_processed": 47,
            "resolution_rate": 0.94,
            "average_resolution_time": "2.3 hours",
            "customer_satisfaction": 4.6,
            "actions_taken": [
                "Triaged 47 customer issues",
                "Resolved 44 issues directly",
                "Escalated 3 complex issues to specialists",
                "Implemented process improvement for common issues"
            ],
            "confidence": 0.85
        }
        
        self.add_to_history(task, result)
        return result


class ComplianceAgent(BaseAgent):
    """Custom agent for compliance and regulatory tasks"""
    
    def __init__(self, name: str = "Compliance Officer"):
        expertise = [
            "compliance", "regulations", "legal review", "audit",
            "risk assessment", "policy development"
        ]
        super().__init__(name, AgentRole.PLANNING, expertise)
    
    def process_task(self, task):
        """Process compliance tasks"""
        objective = task.get("objective", "")
        
        result = {
            "status": "completed",
            "agent": self.name,
            "task": objective,
            "compliance_status": "fully_compliant",
            "requirements_checked": 23,
            "issues_found": 0,
            "recommendations": [
                "Continue quarterly compliance audits",
                "Monitor emerging regulations in target markets",
                "Update privacy policy for new data requirements",
                "Implement additional security controls for payment data"
            ],
            "confidence": 0.96
        }
        
        self.add_to_history(task, result)
        return result


def custom_agent_example():
    """Demonstrate using custom agents"""
    print("\n" + "="*70)
    print("CUSTOM AGENT EXAMPLE")
    print("="*70)
    
    # Create coordinator
    coordinator = AgentCoordinator()
    
    # Register custom agents
    print("\n[STEP 1] Registering Custom Agents")
    coordinator.register_agent(DataScientistAgent())
    coordinator.register_agent(CustomerServiceAgent())
    coordinator.register_agent(ComplianceAgent())
    
    # Display updated system status
    print("\n[STEP 2] System Status with Custom Agents")
    print(f"Total agents registered: {len(coordinator.agents)}")
    print("\nRegistered Agents:")
    for name, agent in coordinator.agents.items():
        print(f"  • {name} ({agent.role.value})")
    
    # Use custom agents
    print("\n[STEP 3] Executing Tasks with Custom Agents")
    
    # Task 1: ML Analysis
    print("\n--- Task 1: Data Science Analysis ---")
    ml_task = {
        "objective": "Build predictive model for customer churn",
        "type": "data_science",
        "required_skills": ["machine learning", "statistical modeling"]
    }
    
    data_scientist = coordinator.agents.get("Data Scientist")
    if data_scientist:
        ml_result = data_scientist.process_task(ml_task)
        print(f"Agent: {ml_result['agent']}")
        print(f"Best Model: {ml_result['best_model']}")
        print(f"Accuracy: {ml_result['accuracy']:.1%}")
        print(f"Confidence: {ml_result['confidence']:.0%}")
    
    # Task 2: Customer Service
    print("\n--- Task 2: Customer Support Management ---")
    support_task = {
        "objective": "Handle customer service queue and resolve issues",
        "type": "customer_service",
        "required_skills": ["customer support", "issue resolution"]
    }
    
    customer_agent = coordinator.agents.get("Customer Service Manager")
    if customer_agent:
        support_result = customer_agent.process_task(support_task)
        print(f"Agent: {support_result['agent']}")
        print(f"Tickets Processed: {support_result['tickets_processed']}")
        print(f"Resolution Rate: {support_result['resolution_rate']:.0%}")
        print(f"Customer Satisfaction: {support_result['customer_satisfaction']}/5")
    
    # Task 3: Compliance
    print("\n--- Task 3: Compliance Audit ---")
    compliance_task = {
        "objective": "Perform quarterly compliance and regulatory audit",
        "type": "compliance",
        "required_skills": ["compliance", "audit", "regulatory"]
    }
    
    compliance_agent = coordinator.agents.get("Compliance Officer")
    if compliance_agent:
        compliance_result = compliance_agent.process_task(compliance_task)
        print(f"Agent: {compliance_result['agent']}")
        print(f"Status: {compliance_result['compliance_status'].replace('_', ' ').title()}")
        print(f"Requirements Checked: {compliance_result['requirements_checked']}")
        print(f"Issues Found: {compliance_result['issues_found']}")
        print(f"Confidence: {compliance_result['confidence']:.0%}")
    
    # Show agent expertise matching
    print("\n[STEP 4] Expertise Matching")
    test_task = {
        "required_skills": ["machine learning", "compliance", "customer support"]
    }
    
    print("\nAgent suitability for ML + Compliance + Customer Support task:")
    for name, agent in coordinator.agents.items():
        match_score = agent.get_expertise_match(test_task['required_skills'])
        can_handle = agent.can_handle(test_task)
        print(f"  {name}: {match_score:.1%} match - {'Can handle' if can_handle else 'Cannot handle'}")
    
    print("\n" + "="*70)
    print("CUSTOM AGENT EXAMPLE COMPLETE")
    print("="*70 + "\n")


def multi_domain_task_example():
    """Demonstrate a task that requires multiple custom agents"""
    print("\n" + "="*70)
    print("MULTI-DOMAIN TASK EXAMPLE")
    print("="*70)
    print("\nTask: Launch new AI-powered customer analytics platform")
    print("Required expertise: Research, ML, Compliance, Customer Service, Planning")
    
    coordinator = AgentCoordinator()
    coordinator.register_agent(DataScientistAgent())
    coordinator.register_agent(ComplianceAgent())
    coordinator.register_agent(CustomerServiceAgent())
    
    # Complex task requiring multiple domains
    launch_task = {
        "objective": "Launch new AI-powered customer analytics platform",
        "type": "product_launch",
        "required_skills": [
            "machine learning", "compliance", "customer support",
            "research", "planning", "data science"
        ],
        "context": {
            "target_market": "Enterprise SaaS",
            "timeline": "12 weeks",
            "budget": "$500k"
        }
    }
    
    print("\n[COORDINATOR] Analyzing task requirements...")
    print(f"Task: {launch_task['objective']}")
    print(f"Required Skills: {len(launch_task['required_skills'])} expertise areas")
    
    # Show which agents are needed
    print("\n[COORDINATOR] Matching agents to task:")
    required_agents = []
    for name, agent in coordinator.agents.items():
        match = agent.get_expertise_match(launch_task['required_skills'])
        if match > 0.3:
            required_agents.append((name, agent, match))
            print(f"  ✓ {name}: {match:.0%} match - MATCHED")
        else:
            print(f"  ✗ {name}: {match:.0%} match - not needed")
    
    # Execute with matched agents
    print(f"\n[COORDINATOR] Executing with {len(required_agents)} agents...")
    print("\nExecution Results:")
    
    for agent_name, agent, match in required_agents:
        print(f"\n  → {agent_name} ({match:.0%} expertise match)")
        
        task_for_agent = {
            **launch_task,
            "focus": f"Focus on {agent.role.value} aspects"
        }
        
        result = agent.process_task(task_for_agent)
        
        if result.get('models_trained'):
            print(f"     Models trained: {result['models_trained']}")
            print(f"     Best accuracy: {result['accuracy']:.1%}")
        elif result.get('compliance_status'):
            print(f"     Compliance: {result['compliance_status'].replace('_', ' ').title()}")
            print(f"     Issues found: {result['issues_found']}")
        elif result.get('tickets_processed'):
            print(f"     Tickets processed: {result['tickets_processed']}")
            print(f"     Satisfaction: {result['customer_satisfaction']}/5")
        
        print(f"     Confidence: {result.get('confidence', 0):.0%}")
    
    print("\n" + "="*70)
    print("✓ MULTI-DOMAIN TASK COMPLETE")
    print("="*70 + "\n")


if __name__ == "__main__":
    print("\n╔" + "="*68 + "╗")
    print("║" + "CUSTOM AGENTS DEMONSTRATION".center(68) + "║")
    print("║" + "Extending the multi-agent system with specialized agents".center(68) + "║")
    print("╚" + "="*68 + "╝")
    
    custom_agent_example()
    multi_domain_task_example()
    
    print("\n" + "="*70)
    print("KEY TAKEAWAYS")
    print("="*70)
    print("""
1. Creating Custom Agents:
   • Inherit from BaseAgent
   • Implement process_task() method
   • Define specialized expertise
   • Register with coordinator

2. Agent Specialization:
   • Each agent has unique skills
   • Expertise matching is automatic
   • Can handle cross-domain tasks

3. Flexibility:
   • Mix default and custom agents
   • Scale to any number of agents
   • Easy to add new specializations

4. Task Complexity:
   • Simple tasks need few agents
   • Complex tasks use multiple agents
   • Coordinator intelligently routes

Try creating your own custom agents for your domain!
    """)
