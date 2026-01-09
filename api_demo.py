"""
API Demo - Shows system working with and without real LLM API
Run this to see the difference between simulation and real API modes
"""
from agents.coordinator import AgentCoordinator
import os


def demo_current_mode():
    """Show what mode the system is running in"""
    api_key = os.getenv("GROQ_API_KEY")
    
    print("\n" + "="*70)
    print("API MODE DETECTION")
    print("="*70)
    
    if api_key:
        print("✓ GROQ_API_KEY is SET")
        print(f"  Key (first 20 chars): {api_key[:20]}...")
        print("\n  System will use REAL Groq LLM API")
        print("  Expected: Slower (~2-5 sec) but AI-generated responses")
    else:
        print("✗ GROQ_API_KEY is NOT SET")
        print("\n  System will use SIMULATION mode (offline)")
        print("  Expected: Instant responses with predefined data")
    
    print("\n" + "="*70)
    print("To enable real API:")
    print("  1. Get free key: https://console.groq.com")
    print("  2. Set: export GROQ_API_KEY='gsk_your_key'")
    print("  3. Run: python3 main.py")
    print("="*70 + "\n")


def demo_with_timing():
    """Run demo and show timing"""
    import time
    
    print("\n" + "="*70)
    print("RUNNING MULTI-AGENT TASK WITH TIMING")
    print("="*70 + "\n")
    
    coordinator = AgentCoordinator()
    
    task = {
        "objective": "Analyze competitive landscape for AI-powered CRM tools",
        "type": "market_analysis",
        "required_skills": ["research", "market analysis", "competitive intelligence"]
    }
    
    print(f"Task: {task['objective']}\n")
    
    start_time = time.time()
    result = coordinator.execute_task(task, verbose=False)
    elapsed = time.time() - start_time
    
    print("\n" + "-"*70)
    print("RESULTS SUMMARY")
    print("-"*70)
    
    # Get mode from result
    research_phase = result['phase_results'].get('research', {})
    mode = research_phase.get('mode', 'unknown')
    
    print(f"\nMode: {mode.upper()}")
    print(f"Total Time: {elapsed:.2f} seconds")
    print(f"Overall Confidence: {result['overall_confidence']:.0%}")
    
    if "research" in result['phase_results'] and result['phase_results']['research'].get('findings'):
        print(f"\nResearch Findings: {len(research_phase['findings'])} items")
        for i, finding in enumerate(research_phase['findings'][:2], 1):
            print(f"  {i}. {finding['finding']}")
    
    print("\n" + "-"*70)
    if mode == "real_api":
        print("✓ Using REAL LLM API - responses are AI-generated")
    else:
        print("ℹ️  Using SIMULATION - responses are predefined")
    print("-"*70 + "\n")
    
    return result


def instructions():
    """Show setup instructions"""
    print("\n" + "="*70)
    print("🔧 SETUP INSTRUCTIONS")
    print("="*70)
    
    print("""
To use REAL Groq LLM API (FREE):

1. GET API KEY (5 minutes):
   → Visit: https://console.groq.com
   → Sign up (free, no credit card needed)
   → Go to "API Keys" section
   → Create new key
   → Copy the key (starts with 'gsk_')

2. SET ENVIRONMENT VARIABLE:
   → Linux/Mac:
     export GROQ_API_KEY='gsk_your_actual_key_here'
   
   → Windows (PowerShell):
     $env:GROQ_API_KEY='gsk_your_actual_key_here'

3. RUN THE SYSTEM:
   → python3 main.py
   
   You should see:
   ✓ Research Expert using real Groq LLM API
   ✓ Data Analyst using real Groq LLM API

4. OPTIONAL - INSTALL groq package for better integration:
   → pip install groq
   
   Without it, system still works but shows warnings

BENEFITS OF USING API:
✓ Real AI-generated responses
✓ More accurate insights
✓ Realistic market analysis
✓ Still free (Groq has generous free tier)

RUNNING WITHOUT API:
✓ Works offline with zero setup
✓ Uses predefined simulation data
✓ Instant response (no API calls)
✓ Perfect for testing and learning
""")
    
    print("="*70 + "\n")


if __name__ == "__main__":
    print("\n")
    print("╔" + "="*68 + "╗")
    print("║" + "  API DEMO - Multi-Agent System with Real LLM Support".center(68) + "║")
    print("╚" + "="*68 + "╝")
    
    # Show current mode
    demo_current_mode()
    
    # Run with timing
    demo_with_timing()
    
    # Show instructions
    instructions()
    
    print("📚 For more info, see: API_SETUP.md\n")
