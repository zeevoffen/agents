# Quick Reference - Multi-Agent System

## System Initialization

```python
from agents.coordinator import AgentCoordinator

# Create coordinator (automatically registers 4 agents)
coordinator = AgentCoordinator()
```

## Running Tasks

### Basic Execution
```python
task = {
    "objective": "Your task here",
    "type": "market_analysis|product_planning|operations|general"
}

result = coordinator.execute_task(task, verbose=True)
```

### Access Results
```python
# Overall result
print(result['status'])
print(result['overall_confidence'])

# Phase results
research = result['phase_results']['research']
analysis = result['phase_results']['analysis']
planning = result['phase_results']['planning']
execution = result['phase_results']['execution']
```

## Agent Management

```python
# View all agents
coordinator.display_system_status()

# Get specific agent status
status = coordinator.get_agent_status("Research Expert")

# Register custom agent
from agents.base import BaseAgent
coordinator.register_agent(my_agent)
```

## Task History

```python
# Get all completed tasks
history = coordinator.get_task_history()

# Access task details
for task in history:
    print(f"Task: {task['task_objective']}")
    print(f"Confidence: {task['overall_confidence']:.0%}")
    print(f"Duration: {task['phase_results'].keys()}")
```

## Agent Communication

```python
# Send message between agents
message = research_agent.send_message(
    recipient="Data Analyst",
    content="Analysis data ready",
    message_type="result",
    priority=2
)

# Receive message
analysis_agent.receive_message(message)

# Read inbox
messages = analysis_agent.read_inbox()
```

## Common Task Examples

### Market Analysis
```python
task = {
    "objective": "Analyze market trends for AI startups",
    "type": "market_analysis",
    "analysis_type": "market",
    "focus_areas": ["market size", "growth rate", "competition"]
}
```

### Product Planning
```python
task = {
    "objective": "Create product roadmap for SaaS platform",
    "type": "product_planning",
    "context": {"market": "B2B Enterprise"},
    "analysis_type": "product"
}
```

### Operations Management
```python
task = {
    "objective": "Execute digital transformation initiative",
    "type": "operations",
    "required_skills": ["execution", "project management"]
}
```

## Accessing Phase Results

### Research Phase
```python
research = result['phase_results']['research']
# Available: findings, sources_used, confidence, methodology
for finding in research['findings']:
    print(f"{finding['finding']}: {finding['data']}")
```

### Analysis Phase
```python
analysis = result['phase_results']['analysis']
# Available: insights, patterns, recommendations, key_metrics
for insight in analysis['insights']:
    print(f"{insight['insight']} ({insight['impact']} impact)")
```

### Planning Phase
```python
planning = result['phase_results']['planning']
# Available: strategic_plan, roadmap, risk_mitigation, timeline
for phase in planning['roadmap']:
    print(f"Phase {phase['phase']}: {phase['name']} ({phase['duration']})")
```

### Execution Phase
```python
execution = result['phase_results']['execution']
# Available: execution_results, progress, quality_assurance, completion_rate
print(f"Completion: {execution['progress']['completion_percentage']:.1f}%")
print(f"Quality: {execution['progress']['overall_quality_score']:.2f}")
```

## Utilities

### Task Decomposition
```python
from utils.task_utils import decompose_task, estimate_task_complexity

subtasks = decompose_task(task, depth=2)
complexity = estimate_task_complexity(task)  # "low", "medium", "high"
```

### Message Filtering
```python
from utils.messages import filter_messages_by_type, sort_messages_by_priority

# Get specific message types
task_messages = filter_messages_by_type(messages, "task")
result_messages = filter_messages_by_type(messages, "result")

# Sort by priority
sorted_msgs = sort_messages_by_priority(messages)

# Get summary
summary = create_message_summary(messages)
```

## Running Examples

```bash
# Complete demonstration with 3 demos
python3 main.py

# Specific examples
python3 -m examples.market_analysis
python3 -m examples.product_research
python3 -m examples.workflow_demo
```

## Agent Roles & Expertise

| Agent | Role | Key Expertise |
|-------|------|---------------|
| Research Expert | research | Data collection, synthesis, surveys, interviews |
| Data Analyst | analysis | Statistics, pattern recognition, insights, benchmarking |
| Strategic Planner | planning | Roadmaps, strategy, risk management, resource allocation |
| Operations Manager | execution | Project management, QA, implementation, progress tracking |

## Confidence Levels

- **Research Agent**: 85% - Highly reliable data gathering
- **Analysis Agent**: 78% - Solid pattern recognition
- **Planning Agent**: 80% - Well-structured plans
- **Execution Agent**: 82% - Reliable task execution
- **Overall**: ~81% - Strong combined confidence

## Creating Custom Agents

```python
from agents.base import BaseAgent, AgentRole

class MyAgent(BaseAgent):
    def __init__(self):
        expertise = ["skill1", "skill2", "skill3"]
        super().__init__("My Agent", AgentRole.EXECUTION, expertise)
    
    def process_task(self, task):
        # Process task...
        return {
            "status": "completed",
            "agent": self.name,
            "result": "..."
        }

# Use it
coordinator.register_agent(MyAgent())
```

## Tips & Best Practices

1. **Be specific**: Detailed task objectives yield better results
2. **Specify skills**: List required_skills for better agent matching
3. **Check confidence**: Higher confidence = more reliable results
4. **Track history**: Use task history for pattern analysis
5. **Monitor agents**: Check agent status regularly
6. **Extend smartly**: Add agents that fill specific expertise gaps

---

**Keep this handy for quick reference!**
