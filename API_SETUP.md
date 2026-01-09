# 🔌 Using Real LLM APIs with Multi-Agent System

## Overview

The system now supports **real LLM APIs** while maintaining offline simulation mode as fallback.

### Current Setup
- **Primary**: Groq API (free tier, very fast)
- **Fallback**: Offline simulation (no setup needed)

---

## 🚀 Quick Setup with Groq API (FREE)

### Step 1: Get Free API Key

1. Go to [console.groq.com](https://console.groq.com)
2. Sign up (free account, no credit card needed)
3. Navigate to "API Keys"
4. Create a new API key
5. Copy it

### Step 2: Set Environment Variable

```bash
# On Linux/Mac, add to ~/.bashrc or ~/.zshrc:
export GROQ_API_KEY='gsk_your_actual_key_here'

# Or set it temporarily for one session:
export GROQ_API_KEY='gsk_your_actual_key_here'
cd /home/zeev/projects/agents
python3 main.py
```

### Step 3: Install Groq Package (Optional)

```bash
pip install groq
```

If not installed, the system will automatically fall back to simulation mode.

---

## 🎯 Using the System

### With Real API (Groq)
```bash
export GROQ_API_KEY='your-key-here'
python3 main.py
```

Output will show:
```
✓ Research Expert using real Groq LLM API
✓ Data Analyst using real Groq LLM API
```

### Without API (Simulation - Default)
```bash
python3 main.py
```

Output will show:
```
ℹ️  Research Expert using simulation mode (offline)
ℹ️  Data Analyst using simulation mode (offline)
```

---

## 📊 What Each Agent Uses

### Research Expert
- **API Mode**: Groq LLM generates realistic research findings
- **Simulation Mode**: Returns predefined market research data
- **Confidence**: 85% in both modes

### Data Analyst
- **API Mode**: Groq LLM analyzes data and generates insights
- **Simulation Mode**: Returns predefined analysis patterns
- **Confidence**: 78% in both modes

### Strategic Planner
- **Status**: Currently simulation-based
- **Future**: Can be enhanced with API

### Operations Manager
- **Status**: Currently simulation-based
- **Future**: Can be enhanced with API

---

## 🔄 Automatic Fallback

If API fails or key is missing:
1. System automatically prints warning
2. Switches to simulation mode
3. **Continues working seamlessly**

```bash
# This just works - no errors!
python3 main.py
```

---

## 💡 Example: Compare Modes

### Run with API
```bash
export GROQ_API_KEY='gsk_your_key'
python3 -m examples.market_analysis
```

Output:
```
Agent: Research Expert
Status: completed
Confidence: 85%
Mode: real_api  ← Real LLM API
Findings: 4 items (AI-generated)
```

### Run without API
```bash
unset GROQ_API_KEY
python3 -m examples.market_analysis
```

Output:
```
Agent: Research Expert
Status: completed
Confidence: 85%
Mode: simulation  ← Offline simulation
Findings: 4 items (predefined)
```

Both work perfectly!

---

## 🔐 Security Notes

- **API Key**: Store safely, never commit to git
- **Best Practice**: Use environment variables
- **Safety**: Key is only used when explicitly set

```bash
# ❌ DON'T do this
python3 main.py "gsk_your_key_here"

# ✅ DO this instead
export GROQ_API_KEY='gsk_your_key_here'
python3 main.py
```

---

## 📋 Available Groq Models (Free Tier)

- `mixtral-8x7b-32768` - Fast, good quality (currently used)
- `llama2-70b-4096` - Larger model
- `gemma-7b-it` - Lightweight

Currently using: **mixtral-8x7b-32768** (best balance of speed and quality)

---

## ✅ Groq Free Tier Limits

- **Rate Limit**: 30 requests/minute
- **Cost**: FREE
- **No Credit Card**: Required
- **Perfect for**: Demos, testing, development

---

## 🔧 Customizing API Behavior

### In Your Code

```python
from agents.coordinator import AgentCoordinator
from agents.research_agent import ResearchAgent

# Create agents with API disabled
coordinator = AgentCoordinator()

# Force simulation mode
research = ResearchAgent(use_api=False)
coordinator.register_agent(research)

# Or use environment variable
import os
os.environ['GROQ_API_KEY'] = 'your-key'
research = ResearchAgent(use_api=True)
coordinator.register_agent(research)
```

---

## 🐛 Troubleshooting

### "groq not installed"
```bash
pip install groq
```

### "No GROQ_API_KEY found"
```bash
export GROQ_API_KEY='your-key-here'
python3 main.py
```

### "API Error: Rate limit exceeded"
Wait a minute and try again (30 requests/minute limit)

### System still in simulation mode?
```bash
# Verify key is set
echo $GROQ_API_KEY

# Should print your key
# If empty, you didn't export it correctly
```

---

## 📈 Performance

### With Groq API
- Research: ~2-3 seconds (API call)
- Analysis: ~2-3 seconds (API call)
- Planning: <1 second (simulation)
- Execution: <1 second (simulation)
- **Total**: ~5-8 seconds

### With Simulation
- Research: <0.1 seconds
- Analysis: <0.1 seconds
- Planning: <0.1 seconds
- Execution: <0.1 seconds
- **Total**: <1 second

---

## 🚀 Full Example

```bash
# 1. Get API key from console.groq.com
# 2. Set environment variable
export GROQ_API_KEY='gsk_your_actual_key_from_groq'

# 3. Run any example with real API
cd /home/zeev/projects/agents
python3 main.py

# 4. Check output for API confirmation
# ✓ Research Expert using real Groq LLM API
# ✓ Data Analyst using real Groq LLM API
```

---

## 🎯 Next Steps to Add More Agents

To add API support to Planning Agent:

```python
# In agents/planning_agent.py
def _create_strategic_plan_with_api(self, objective, insights):
    """Use Groq LLM for strategy"""
    prompt = f"Create a strategic plan for: {objective}..."
    response = self.client.chat.completions.create(...)
    return json.loads(response.choices[0].message.content)
```

Same pattern applies to all agents!

---

## 📚 Additional Resources

- [Groq Console](https://console.groq.com)
- [Groq Documentation](https://console.groq.com/docs)
- [Groq Python SDK](https://github.com/groq/groq-python)

---

## ✨ Summary

| Aspect | Without API | With Groq API |
|--------|-------------|---------------|
| Setup Time | 0 minutes | 5 minutes |
| Cost | Free | Free |
| Real AI Output | No | Yes |
| Internet Required | No | Yes |
| Speed | <1 sec | 5-8 sec |
| Accuracy | Medium | High |
| Best For | Testing | Production |

**Both modes work perfectly - choose based on your needs!**

---

**Happy multi-agent problem solving with real AI!** 🚀
