"""
Example: Workflow Demonstration
Shows how agents delegate and solve complex problems step-by-step
"""
from agents.coordinator import AgentCoordinator


def workflow_demonstration():
    """
    Demonstrate the complete workflow of task delegation and
    agent collaboration for problem solving
    """
    print("\n" + "="*70)
    print("WORKFLOW DEMONSTRATION - STEP-BY-STEP AGENT COLLABORATION")
    print("="*70)
    
    coordinator = AgentCoordinator()
    
    # Show system initialization
    print("\n[1] SYSTEM INITIALIZATION")
    print("    Initializing multi-agent system...")
    coordinator.display_system_status()
    
    # Define a complex task
    print("\n[2] TASK SUBMISSION")
    complex_task = {
        "objective": "Develop strategy for entering Asian market with AI-powered analytics platform",
        "type": "market_expansion",
        "context": {
            "current_position": "Leader in North American market",
            "target": "Establish presence in Asia-Pacific",
            "timeline": "12-14 weeks"
        },
        "required_skills": ["research", "market analysis", "planning", "execution"]
    }
    
    print(f"    Task: {complex_task['objective']}")
    print(f"    Timeline: {complex_task['context']['timeline']}")
    
    # Execute with verbose output to show coordination
    print("\n[3] TASK COORDINATION & DELEGATION")
    result = coordinator.execute_task(complex_task, verbose=True)
    
    # Display detailed workflow
    print("\n[4] WORKFLOW COMPLETION SUMMARY")
    print("─"*70)
    
    print("\nAgent Collaboration Sequence:")
    for i, step in enumerate(result['collaboration_log'], 1):
        print(f"  {i}. {step}")
    
    # Show phase-by-phase results
    print("\nPhase Results Overview:")
    print("─"*70)
    
    phases = result['phase_results']
    
    # Research phase
    if phases['research']['status'] != 'skipped':
        research = phases['research']
        print(f"\n📊 RESEARCH PHASE")
        print(f"   Status: {research['status']}")
        print(f"   Findings: {len(research.get('findings', []))} items")
        print(f"   Confidence: {research.get('confidence', 'N/A'):.0%}")
    
    # Analysis phase
    if phases['analysis']['status'] != 'skipped':
        analysis = phases['analysis']
        print(f"\n📈 ANALYSIS PHASE")
        print(f"   Status: {analysis['status']}")
        print(f"   Insights: {len(analysis.get('insights', []))} items")
        print(f"   Quality Score: {analysis.get('key_metrics', {}).get('average', 'N/A')}")
    
    # Planning phase
    if phases['planning']['status'] != 'skipped':
        planning = phases['planning']
        print(f"\n📋 PLANNING PHASE")
        print(f"   Status: {planning['status']}")
        print(f"   Roadmap Phases: {len(planning.get('roadmap', []))}")
        print(f"   Risk Items Identified: {len(planning.get('risk_mitigation', []))}")
    
    # Execution phase
    if phases['execution']['status'] != 'skipped':
        execution = phases['execution']
        print(f"\n⚡ EXECUTION PHASE")
        print(f"   Status: {execution['status']}")
        print(f"   Subtasks: {execution.get('progress', {}).get('total_tasks', 'N/A')}")
        print(f"   Completion: {execution.get('progress', {}).get('completion_percentage', 0):.1f}%")
    
    # Display key deliverables
    print("\n" + "─"*70)
    print("KEY DELIVERABLES")
    print("─"*70)
    
    summary = result['summary']
    
    if summary['key_findings']:
        print("\nKey Findings:")
        for finding in summary['key_findings'][:3]:
            print(f"  • {finding}")
    
    if summary['critical_insights']:
        print("\nCritical Insights:")
        for insight in summary['critical_insights'][:3]:
            print(f"  • {insight}")
    
    if summary['recommended_actions']:
        print("\nRecommended Actions:")
        for action in summary['recommended_actions'][:3]:
            print(f"  • {action}")
    
    # Final metrics
    print("\n" + "─"*70)
    print("EXECUTION METRICS")
    print("─"*70)
    print(f"Overall Confidence Level: {result['overall_confidence']:.0%}")
    print(f"Agents Coordinated: {len(result['agents_involved'])}")
    print(f"Execution Timeline: {summary['timeline']}")
    print(f"Success Probability: {summary['success_probability']}")
    
    print("\n" + "─"*70)
    print("✓ WORKFLOW DEMONSTRATION COMPLETE")
    print("─"*70 + "\n")
    
    return result


def demonstrate_agent_communication():
    """Demonstrate inter-agent communication and delegation"""
    print("\n" + "="*70)
    print("AGENT COMMUNICATION DEMONSTRATION")
    print("="*70)
    
    coordinator = AgentCoordinator()
    
    # Get agents
    research_agent = coordinator.agents.get("Research Expert")
    analysis_agent = coordinator.agents.get("Data Analyst")
    planning_agent = coordinator.agents.get("Strategic Planner")
    
    if research_agent and analysis_agent:
        print("\n[COMMUNICATION FLOW]")
        print("\n1. Research Agent → Analysis Agent")
        
        # Research agent sends message to analyst
        message = research_agent.send_message(
            analysis_agent.name,
            "Completed market research. Data ready for analysis.",
            message_type="result",
            priority=2
        )
        
        analysis_agent.receive_message(message)
        print(f"   Message ID: {message.id}")
        print(f"   Type: {message.message_type}")
        print(f"   Priority: {message.priority}")
        
        print("\n2. Data Analyst → Strategic Planner")
        
        # Analysis agent sends results to planner
        message2 = analysis_agent.send_message(
            planning_agent.name,
            "Analysis complete. Generated insights for strategy development.",
            message_type="result",
            priority=2
        )
        
        planning_agent.receive_message(message2)
        print(f"   Message ID: {message2.id}")
        print(f"   Type: {message2.message_type}")
        print(f"   Status: {message2.status}")
        
        print("\n3. Message Queue Status")
        print(f"   Research Agent outbox: {len(research_agent.outbox)} message(s)")
        print(f"   Analysis Agent inbox: {len(analysis_agent.inbox)} message(s)")
        print(f"   Planning Agent inbox: {len(planning_agent.inbox)} message(s)")


if __name__ == "__main__":
    workflow_demonstration()
    demonstrate_agent_communication()
