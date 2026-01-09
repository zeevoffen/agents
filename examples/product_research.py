"""
Example: Product Research & Planning Workflow
Demonstrates task delegation for product development
"""
from agents.coordinator import AgentCoordinator


def product_research_example():
    """
    Execute a comprehensive product research and planning workflow
    demonstrating sequential agent delegation
    """
    print("\n" + "="*70)
    print("PRODUCT RESEARCH & PLANNING EXAMPLE")
    print("="*70)
    
    coordinator = AgentCoordinator()
    
    product_task = {
        "objective": "Design and plan a new productivity collaboration tool",
        "type": "product_planning",
        "context": {
            "market": "Remote work and team collaboration",
            "target_segment": "Mid-market companies (50-500 employees)",
            "timeline": "Launch in Q2 2026"
        },
        "required_skills": ["research", "product development", "planning"],
        "analysis_type": "product"
    }
    
    result = coordinator.execute_task(product_task, verbose=True)
    
    print("\n" + "─"*70)
    print("PRODUCT DEVELOPMENT ROADMAP")
    print("─"*70)
    
    research_phase = result['phase_results'].get('research', {})
    planning_phase = result['phase_results'].get('planning', {})
    
    if 'findings' in research_phase:
        print("\nResearch Findings:")
        for finding in research_phase['findings'][:3]:
            print(f"  • {finding['finding']}")
    
    if 'strategic_plan' in planning_phase:
        plan = planning_phase['strategic_plan']
        print(f"\nStrategic Vision: {plan['vision']}")
        print(f"Strategy: {plan['strategy']}")
        
        print("\nSuccess Criteria:")
        for criterion in plan['success_criteria']:
            print(f"  ✓ {criterion}")
    
    if 'roadmap' in planning_phase:
        print("\nDetailed Roadmap:")
        for phase in planning_phase['roadmap']:
            print(f"\n  {phase['phase']}. {phase['name']}")
            print(f"     Duration: {phase['duration']}")
            print(f"     Owner: {phase['owner']}")
            print(f"     Milestones:")
            for milestone in phase['milestones']:
                print(f"       • {milestone}")
    
    if 'risk_mitigation' in planning_phase:
        print("\nRisk Management:")
        for risk in planning_phase['risk_mitigation'][:2]:
            print(f"  • {risk['risk']} (Probability: {risk['probability']})")
            print(f"    Mitigation: {risk['mitigation']}")
    
    print("\n" + "─"*70)
    print(f"Plan Confidence: {result['overall_confidence']:.0%}")
    print("─"*70 + "\n")
    
    return result


if __name__ == "__main__":
    product_research_example()
