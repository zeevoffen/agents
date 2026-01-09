# Multi-Agent System - Complete Guide

## Overview

This is a production-ready multi-agent system built with Python that demonstrates:
- **Task delegation** between specialized agents
- **Collaborative problem solving** across different domains
- **Agent communication** and message passing
- **Hierarchical task decomposition**
- **Result synthesis** from multiple sources

## Quick Start

### Installation

```bash
# Navigate to the project
cd /home/zeev/projects/agents

# No external dependencies required! Uses Python standard library only
# Optional: Install colorama for enhanced output (optional)
pip install -r requirements.txt
```

### Running Demonstrations

```bash
# Run the main comprehensive demo
python3 main.py

# Run specific examples
python3 -m examples.market_analysis
python3 -m examples.product_research
python3 -m examples.workflow_demo
```

## Architecture

### Multi-Agent System Design

```
┌─────────────────────────────────────┐
│     Agent Coordinator (Manager)     │
│  • Task distribution & routing      │
│  • Result synthesis                 │
│  • Message queue management         │
└────────────┬────────────────────────┘
             │
    ┌────────┼────────┬─────────────┐
    ↓        ↓        ↓             ↓
┌─────────┐┌────────┐┌──────────┐┌──────────┐
│Research ││Analysis││Planning  ││Execution │
│ Agent   ││ Agent  ││ Agent    ││ Agent    │
│         ││        ││          ││          │
│Gathers  ││Analyzes││Creates   ││Implements│
│data &   ││data &  ││strategies││plans &   │
│info     ││finds   ││& roadmaps││manages   │
│         ││patterns││          ││ops       │
└─────────┘└────────┘└──────────┘└──────────┘
```

### Agent Types

#### 1. **Research Agent**
- **Purpose**: Information gathering and synthesis
- **Expertise**: Data collection, research methods, trend analysis
- **Output**: Findings, market research, competitive analysis

#### 2. **Analysis Agent**
- **Purpose**: Pattern recognition and insight generation
- **Expertise**: Data analysis, statistics, insights, benchmarking
- **Output**: Insights, patterns, recommendations

#### 3. **Planning Agent**
- **Purpose**: Strategy and roadmap development
- **Expertise**: Strategic planning, risk management, timeline estimation
- **Output**: Roadmaps, plans, risk mitigation strategies

#### 4. **Execution Agent**
- **Purpose**: Task implementation and operational management
- **Expertise**: Project management, QA, task execution, progress tracking
- **Output**: Implementation results, quality assurance reports

## How Task Delegation Works

### Task Flow Example

```
User Input: "Analyze emerging AI market trends"
    ↓
[1] COORDINATOR ANALYSIS
    • Understands task requirements
    • Determines needed expertise
    • Creates execution plan
    ↓
[2] RESEARCH PHASE
    • Research Expert gathers market data
    • Returns 4+ findings
    • Shares results with coordinator
    ↓
[3] ANALYSIS PHASE
    • Analysis Agent receives research data
    • Identifies patterns and trends
    • Generates insights
    ↓
[4] PLANNING PHASE
    • Planning Agent creates action plan
    • Develops implementation roadmap
    • Identifies risks and mitigations
    ↓
[5] EXECUTION PHASE
    • Execution Agent manages implementation
    • Performs quality assurance
    • Tracks progress
    ↓
[6] RESULT SYNTHESIS
    • Coordinator combines all results
    • Creates comprehensive solution
    • Returns final output to user
```

## Key Features

### 1. Intelligent Task Routing

The coordinator automatically determines which agents are needed:

```python
task = {
    "objective": "Analyze market trends",
    "type": "market_analysis",
    "required_skills": ["research", "analysis", "planning"]
}

result = coordinator.execute_task(task)
# Automatically routes to Research → Analysis → Planning agents
```

### 2. Inter-Agent Communication

Agents communicate via message passing:

```python
# Agent A sends to Agent B
message = agent_a.send_message(
    recipient="Agent B",
    content="Analysis results attached",
    message_type="result",
    priority=2
)

# Agent B receives
agent_b.receive_message(message)
messages = agent_b.read_inbox()
```

### 3. Task History & Tracking

All executed tasks are tracked with full context:

```python
# Get task history
history = coordinator.get_task_history()

# Query specific task results
for task in history:
    print(f"Task: {task['task_objective']}")
    print(f"Status: {task['status']}")
    print(f"Confidence: {task['overall_confidence']:.0%}")
```

### 4. Agent Status Monitoring

Monitor individual agent performance:

```python
# Get status of all agents
status = coordinator.get_agent_status()

# Get status of specific agent
research_status = coordinator.get_agent_status("Research Expert")
print(f"Tasks Completed: {research_status['tasks_completed']}")
print(f"Expertise: {research_status['expertise']}")
```

## Usage Examples

### Example 1: Market Analysis

```python
from agents.coordinator import AgentCoordinator

coordinator = AgentCoordinator()

task = {
    "objective": "Analyze SaaS market opportunities",
    "type": "market_analysis",
    "context": {"focus_area": "Enterprise AI", "timeframe": "2024-2026"}
}

result = coordinator.execute_task(task, verbose=True)

# Access results
print("Findings:", result['phase_results']['research']['findings'])
print("Insights:", result['phase_results']['analysis']['insights'])
print("Recommendations:", result['phase_results']['analysis']['recommendations'])
```

### Example 2: Product Development

```python
task = {
    "objective": "Develop product roadmap",
    "type": "product_planning",
    "context": {"market": "B2B SaaS"}
}

result = coordinator.execute_task(task)

# Get the roadmap
roadmap = result['phase_results']['planning']['roadmap']
for phase in roadmap:
    print(f"\nPhase {phase['phase']}: {phase['name']}")
    print(f"Duration: {phase['duration']}")
    for milestone in phase['milestones']:
        print(f"  • {milestone}")
```

### Example 3: Custom Agent Extension

```python
from agents.base import BaseAgent, AgentRole

class CustomAgent(BaseAgent):
    def __init__(self, name="Custom Agent"):
        expertise = ["custom skill 1", "custom skill 2"]
        super().__init__(name, AgentRole.EXECUTION, expertise)
    
    def process_task(self, task):
        # Your custom logic here
        return {"status": "completed", "agent": self.name}

# Register with coordinator
coordinator = AgentCoordinator()
custom_agent = CustomAgent()
coordinator.register_agent(custom_agent)
```

## Task Execution Confidence Levels

Each agent returns a confidence score:

- **Research Agent**: 85% - High confidence in data gathering
- **Analysis Agent**: 78% - Medium-high confidence in insights
- **Planning Agent**: 80% - High confidence in planning
- **Execution Agent**: 82% - High confidence in implementation
- **Overall**: ~81% - Weighted combination

Higher confidence indicates stronger validation of results.

## Project Structure

```
/home/zeev/projects/agents/
├── main.py                          # Entry point with demonstrations
├── requirements.txt                 # Python dependencies (optional)
├── README.md                        # Project README
├── USAGE_GUIDE.md                   # This file
│
├── agents/                          # Core agent implementations
│   ├── __init__.py
│   ├── base.py                      # Base agent and Message classes
│   ├── research_agent.py            # Research agent implementation
│   ├── analysis_agent.py            # Analysis agent implementation
│   ├── planning_agent.py            # Planning agent implementation
│   ├── execution_agent.py           # Execution agent implementation
│   └── coordinator.py               # Main coordinator/orchestrator
│
├── examples/                        # Usage examples
│   ├── __init__.py
│   ├── market_analysis.py          # Market analysis workflow
│   ├── product_research.py         # Product research workflow
│   └── workflow_demo.py            # Complete workflow demonstration
│
└── utils/                          # Utility modules
    ├── __init__.py
    ├── task_utils.py               # Task decomposition, estimation
    └── messages.py                 # Message handling utilities
```

## Advanced Features

### Task Decomposition

```python
from utils.task_utils import decompose_task, estimate_task_complexity

task = {"objective": "Build and launch new product"}

# Decompose into subtasks
subtasks = decompose_task(task, depth=2)

# Estimate complexity
complexity = estimate_task_complexity(task)
print(f"Complexity: {complexity}")  # "high", "medium", or "low"
```

### Message Utilities

```python
from utils.messages import (
    filter_messages_by_type,
    sort_messages_by_priority,
    create_message_summary
)

# Filter high-priority messages
urgent = filter_messages_by_priority(messages, min_priority=3)

# Create summary statistics
summary = create_message_summary(agent.inbox)
print(f"Messages by type: {summary['by_type']}")
```

### Agent Communication

```python
# Send messages between agents
message = research_agent.send_message(
    recipient="Data Analyst",
    content="Research data ready for analysis",
    message_type="result",
    priority=2
)

# Check message status
print(f"Message {message.id}: {message.status}")
print(f"From: {message.sender} → {message.recipient}")
```

## Performance Characteristics

### Task Execution Time
- Small tasks: < 1 second
- Medium tasks: 1-2 seconds
- Complex multi-phase tasks: 2-5 seconds

### Memory Usage
- Minimal - pure Python implementation
- No external service calls
- In-memory storage of task history

### Scalability
- Can handle unlimited tasks
- Support for adding custom agents
- Flexible delegation logic

## Customization

### Adding New Agent Types

```python
from agents.base import BaseAgent, AgentRole

class DataScientistAgent(BaseAgent):
    def __init__(self):
        expertise = ["machine learning", "statistics", "data science"]
        super().__init__("Data Scientist", AgentRole.ANALYSIS, expertise)
    
    def process_task(self, task):
        # Custom implementation
        return {
            "status": "completed",
            "agent": self.name,
            "models_trained": 3,
            "accuracy": 0.94
        }

# Register and use
coordinator.register_agent(DataScientistAgent())
```

### Modifying Task Routing

Edit `coordinator.py` `_determine_required_agents()` method to customize agent selection logic:

```python
def _determine_required_agents(self, task):
    # Add custom routing logic here
    if "ml" in task.get("objective", "").lower():
        return ["Data Scientist"]
    # ... other routing rules
```

## Troubleshooting

### Import Errors
```bash
# Make sure you're in the right directory
cd /home/zeev/projects/agents

# Use python3 and -m for proper module imports
python3 -m examples.market_analysis
```

### Task Not Executing
1. Check task format - must have "objective" field
2. Verify agents are registered: `coordinator.display_system_status()`
3. Check for error messages in verbose output

### Low Confidence Scores
- Add more detailed task description
- Specify required_skills explicitly
- Ensure task fits agent expertise

## Next Steps

1. **Run the demos** to understand the system
2. **Explore the code** in `agents/` directory
3. **Create custom tasks** by modifying examples
4. **Add new agents** for specialized domains
5. **Integrate** with your own applications

## Real-World Applications

This multi-agent system can be used for:

- **Business Analysis**: Market research, competitive analysis, trend forecasting
- **Product Development**: Requirements gathering, planning, roadmapping
- **Operations Management**: Task coordination, resource allocation, workflow optimization
- **Strategic Planning**: SWOT analysis, risk assessment, scenario planning
- **Research**: Data synthesis, pattern analysis, insight generation
- **Decision Support**: Multi-perspective analysis, recommendation generation

## Support & Feedback

For questions or suggestions:
1. Review the code documentation
2. Check example scripts in `examples/` folder
3. Modify tasks to test different scenarios
4. Extend agent capabilities as needed

---

**Happy Multi-Agent Problem Solving!** 🚀
