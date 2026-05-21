#Scheduling, Leave, Compliance stubs

#CREATE THE STUBS FOR ECH SUB AGENT

def leave_agent(state: dict):
    """Stub for Leave Management specialist."""
    return {
        "final_output": "The Leave Agent is processing your request for time off.",
        "logs": ["Leave Agent activated."]
    }

def scheduling_agent(state: dict):
    """Stub for Scheduling specialist."""
    return {
        "final_output": "The Scheduling Agent is looking at your calendar.",
        "logs": ["Scheduling Agent activated."]
    }

def compliance_agent(state: dict):
    """Stub for Compliance specialist."""
    return {
        "final_output": "The Compliance Agent is checking HR regulations.",
        "logs": ["Compliance Agent activated."]
    }

def clarification_agent(state: dict):
    """Stub for when the request is unclear."""
    return {
        "final_output": "I'm not quite sure what you need. Could you please provide more details?",
        "logs": ["Clarification Agent activated."]
    }
