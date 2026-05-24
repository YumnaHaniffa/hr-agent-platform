#THE LOGIC THAT CONNECTS THE ORCHESTRATOR

#1.Prevents the AI from guessing wrongly on important HR tasks
# then map the intent to the sub agent

def router_logic(state: dict):
    """
    The Decision Maker.
    It reads the intent from the state and returns the name of the next node.
    """
    #1.Check If confidence is low, force clarification
    if state.get("confidence", 0) < 0.6:
        return "clarification_agent"
    
    #2.Map the intent string to the actual node(sub agent) name
    intent_map = {
        "Leave": "leave_agent",
        "Scheduling": "scheduling_agent",
        "Compliance": "compliance_agent",
        "Clarification": "clarification_agent"
    }
    
    return intent_map.get(state["intent"], "clarification_agent")


#THE STATE GRAPH
from typing import TypedDict, Annotated, List, Union #define the shape of your State dictionary,add etra metadata, represent lists, allows multiple possible data types.
from langgraph.graph import StateGraph, END, add_messages #Creates the graph, Marks workflow completion, automatically appends conversation history into state

# Import your actual functions from your other files
from app.agents.orchestrator import classify_intent, router_logic
from app.agents.sub_agents import (
    leave_agent, 
    scheduling_agent, 
    compliance_agent, 
    clarification_agent
)

#1. Define the State Schema - the data that should be kept track of during the execution
class AgentState(TypedDict):
    # 'add_messages' keeps a history of the chat 
    messages: Annotated[list, add_messages]
    intent: str
    confidence: float
    # significance_score will be used later for LTM logic
    significance_score: float 
    final_output: str
    logs: List[str]

# 2. Initialize the Graph
workflow = StateGraph(AgentState)

# 3. Add Nodes (The "Workstations")
workflow.add_node("orchestrator", classify_intent)
workflow.add_node("leave_agent", leave_agent)
workflow.add_node("scheduling_agent", scheduling_agent)
workflow.add_node("compliance_agent", compliance_agent)
workflow.add_node("clarification_agent", clarification_agent)

# 4. Set the Starting Point
# Every request MUST go through the Brain (Orchestrator) first.
workflow.set_entry_point("orchestrator")

# 5. Add Conditional Edges (The "Router")
# This implements your requirement for 'Routing classified intents'.
workflow.add_conditional_edges(
    "orchestrator",
    router_logic,
    {
        "leave_agent": "leave_agent",
        "scheduling_agent": "scheduling_agent",
        "compliance_agent": "compliance_agent",
        "clarification_agent": "clarification_agent"
    }
)

# 6. Add Normal Edges (The "Exit Paths")
# Once a sub-agent provides an answer, we go to the END node.
workflow.add_edge("leave_agent", END)
workflow.add_edge("scheduling_agent", END)
workflow.add_edge("compliance_agent", END)
workflow.add_edge("clarification_agent", END)

# 7. Compile the Graph (The "Execution Engine")
app_graph = workflow.compile()





