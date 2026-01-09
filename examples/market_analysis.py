"""
Example: Market Analysis Workflow
Demonstrates how agents collaborate to analyze market opportunities
"""
from agents.coordinator import AgentCoordinator


def market_analysis_example():
    """
    Execute a comprehensive market analysis task demonstrating
    agent delegation and collaboration
    """
    print("\n" + "="*70)
    print("MARKET ANALYSIS EXAMPLE")
    print("="*70)
    
    # Initialize coordinator
    coordinator = AgentCoordinator()
    
    # Define the market analysis task
    market_analysis_task = {
        "objective": "Comprehensive analysis of AI-powered SaaS market opportunity",
        "type": "market_analysis",
        "context": {
            "focus_area": "Enterprise AI Solutions",
            "market_segment": "B2B SaaS",
            "timeframe": "2024-2026"
        },
        "required_skills": ["research", "data analysis", "market trends"],
        "analysis_type": "market",
        "focus_areas": ["market size", "growth rate", "competitive landscape", "customer needs"]
    }
    
    # Execute the task
    result = coordinator.execute_task(market_analysis_task, verbose=True)
    
    # Extract and display key insights
    print("\n" + "─"*70)
    print("MARKET ANALYSIS RESULTS")
    print("─"*70)
    
    research_phase = result['phase_results'].get('research', {})
    analysis_phase = result['phase_results'].get('analysis', {})
    
    if 'findings' in research_phase:
        print("\nKey Market Findings:")
        for finding in research_phase['findings']:
            print(f"  • {finding['finding']}")
            print(f"    Data: {finding['data']}")
    
    if 'insights' in analysis_phase:
        print("\nMarket Insights:")
        for insight in analysis_phase['insights']:
            print(f"  • {insight['insight']} ({insight['impact']} impact)")
            print(f"    {insight['description']}")
    
    if 'recommendations' in analysis_phase:
        print("\nStrategic Recommendations:")
        for i, rec in enumerate(analysis_phase['recommendations'], 1):
            print(f"  {i}. [{rec['priority'].upper()}] {rec['recommendation']}")
            print(f"     Expected Impact: {rec['expected_impact']}")
    
    if 'roadmap' in result['phase_results'].get('planning', {}):
        print("\nImplementation Timeline:")
        roadmap = result['phase_results']['planning']['roadmap']
        for phase in roadmap[:2]:  # Show first 2 phases
            print(f"  Phase {phase['phase']}: {phase['name']} ({phase['duration']})")
    
    print("\n" + "─"*70)
    print(f"Analysis Confidence: {result['overall_confidence']:.0%}")
    print("─"*70 + "\n")
    
    return result


if __name__ == "__main__":
    market_analysis_example()
