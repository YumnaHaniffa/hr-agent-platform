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


