# Multi-Agent Task Delegation System

A Python-based multi-agent system that demonstrates how intelligent agents collaborate, delegate tasks, and provide solutions. **Now with optional real LLM API support!**

## ✨ Key Features

- **Multiple Specialized Agents**: Research Agent, Analysis Agent, Planning Agent, and Execution Agent
- **Task Delegation**: Agents intelligently delegate tasks based on expertise
- **Hierarchical Task Decomposition**: Complex tasks broken into subtasks
- **Collaborative Problem Solving**: Agents work together to solve complex problems
- **Agent Communication**: Built-in message passing and coordination system
- **🆕 Real LLM API Support**: Optional Groq API integration (FREE)
- **Offline Simulation Mode**: Works perfectly without any API (zero dependencies)

## Architecture

```
┌──────────────────────────────────────────────────┐
│          Agent Coordinator (Manager)             │
└──────────────────────────────────────────────────┘
              ↓         ↓         ↓         ↓
    ┌─────────┴─┴─────────┴─────────┘
    ↓         ↓         ↓         ↓
┌────────┐┌────────┐┌────────┐┌────────┐
│Research││Analysis││Planning││Execution
│ Agent  ││ Agent  ││ Agent  ││ Agent
└────────┘└────────┘└────────┘└────────┘
```

## Requirements

- Python 3.8+
- No external APIs required (uses free local simulation)

## Installation

```bash
cd /home/zeev/projects/agents

# Option 1: No setup needed (offline simulation mode)
# Just run it!
python3 main.py

# Option 2: Enable real LLM API (OPTIONAL, requires Groq API key)
pip install groq
export GROQ_API_KEY='your-free-groq-api-key'
python3 main.py
```

### 🆕 Using Real LLM APIs

The system now supports **Groq API** (FREE tier):

1. **Get free API key**: https://console.groq.com (no credit card needed)
2. **Set environment variable**: `export GROQ_API_KEY='your-key'`
3. **Run**: `python3 main.py`

**Benefits with API**: Real AI-generated insights vs. offline simulation
**Works without API**: Perfect for offline testing and learning

See [API_SETUP.md](API_SETUP.md) for detailed instructions.

## Usage

### Basic Example
```python
from agents.coordinator import AgentCoordinator

# Initialize the multi-agent system
coordinator = AgentCoordinator()

# Define a complex task
task = {
    "objective": "Analyze market trends for tech startups",
    "context": "Q4 2025 market analysis"
}

# Let agents collaborate to solve it
result = coordinator.execute_task(task)
print(result)
```

### Run Examples

```bash
# Run the main demo
python main.py

# Run specific examples
python examples/market_analysis.py
python examples/product_research.py
python examples/workflow_demo.py
```

## How It Works

1. **Task Submission**: A task is submitted to the Agent Coordinator
2. **Task Analysis**: Coordinator analyzes the task and determines which agents are needed
3. **Delegation**: The coordinator delegates subtasks to appropriate agents
4. **Execution**: Each agent processes its assigned task using its expertise
5. **Collaboration**: Agents share results and may request help from other agents
6. **Synthesis**: Coordinator combines results into a final comprehensive solution

## Agent Types

- **Research Agent**: Gathers information and data
- **Analysis Agent**: Analyzes data and identifies patterns
- **Planning Agent**: Creates actionable plans based on analysis
- **Execution Agent**: Executes tasks and reports results

## Free Resources Used

- **Python standard library** for core functionality
- **Custom implementations** of agent logic (no paid APIs)
- **Optional: Groq API** (free tier, generous limits)
- **Offline simulation** (always available, requires no setup)

## Examples Included

- Market trend analysis
- Product research and planning
- Project workflow optimization
- Customer issue resolution

## Project Structure

```
agents/
├── main.py                 # Entry point with demonstrations
├── requirements.txt        # Project dependencies
├── agents/
│   ├── __init__.py
│   ├── base.py            # Base agent class
│   ├── research_agent.py  # Research agent implementation
│   ├── analysis_agent.py  # Analysis agent implementation
│   ├── planning_agent.py  # Planning agent implementation
│   ├── execution_agent.py # Execution agent implementation
│   └── coordinator.py     # Agent coordinator/manager
├── examples/
│   ├── market_analysis.py
│   ├── product_research.py
│   └── workflow_demo.py
└── utils/
    ├── __init__.py
    ├── messages.py        # Message passing utilities
    └── task_utils.py      # Task management utilities
```

## License

MIT
