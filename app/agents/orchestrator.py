from typing import Literal # to restric the value to a specific options
from pydantic import BaseModel, Field # (BaseModel-to create the structured data schema, defines the shape of the data that the returns), (Field - to add extra descriptions)
from langchain_openai import ChatOpenAI # the AI engine(interprets requests,classifies intents,generates outputs,routes workflows.)
from langchain_core.prompts import ChatPromptTemplate #to create structured prompts dynamically

#THE SCHEMA
# The structured output
# define what the brain outputs
class IntentResponse(BaseModel):
    # the literal shows what the sub  agents do
    intent: Literal["Scheduling", "Leave", "Compliance", "Clarification"] = Field(
        description="The target HR department for the request."
    )
    confidence_score: float = Field(
        description="How sure the model is (0.0 to 1.0)."
    )
    significance_score: float = Field(description="How important is this info for future reference? (0.0-1.0)")
    
    reasoning: str = Field(
        description="Explanation for the classification."
    )


#THE BRAIN
#converting flexible human language into a limited set of system-understandable actions
def classify_intent(state: dict):
    """
    Takes the current state, uses an LLM to decide the intent, 
    and updates the state with the decision.
    """
    #Initialize the Expert
    # temperature=0 ensures the model is logical and consistent, not 'creative'.
    llm = ChatOpenAI(model="gpt-4-turbo-preview", temperature=0)

    structured_llm = llm.with_structured_output(IntentResponse)


    #Tell how the LLM should behave before it sees anny user input, CONTROL THE MODELS behavior
    #constraints the model into a specific decision making role
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are an HR Router. Analyze user requests and map them "
                   "to the correct department. If the request is vague, "
                   "select 'Clarification'."),
        ("user", "{user_input}")
    ])
    #Role: “You are an HR Router”
    #Task: “map requests to departments”
    #Rule: “if unclear → Clarification”

    #Get input from the State Management system
    # We look at the very last message the user sent.
    user_text = state["messages"][-1].content # the foundation of the letest message

    # Execute the Brain
    # This transforms natural language into our Pydantic JSON object
    prediction = structured_llm.invoke(prompt.format(user_input=user_text))
    # send the formated prompt to a structured LLLM
    # return a validated structured prediction(the intent)


    #STATE UPDATE
    # We return a dictionary. LangGraph automatically merges this 
    # into the global 'state' so other agents can see it
    return {
        "intent": prediction.intent,
        "confidence": prediction.confidence_score,
        "logs": [f"System identified {prediction.intent} intent."]
    }


#Intent classification & routing
