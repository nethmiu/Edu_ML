from langchain_ollama import OllamaLLM
from state import AgentState

# Connecting the Local LLM Engine (uses llama3)
llm = OllamaLLM(model="llama3")

def summarizer_agent(state: AgentState):
    """
    Acts as an experienced university lecturer and creates a summary.
    This agent reads the notes and provides only the important points.
    """
    # For monitoring the system operation (Observability)
    print("\n--- [AGENT] SUMMARIZING CONTENT ---") 
    
    # Retrieving data from the Global State
    notes = state.get("lecture_notes", "")
    
    # Prompt Engineering: Includes Persona and Constraints
    prompt = f"""
    You are a skilled university lecturer. 
    Read the following lesson notes and create a summary including only the important points.
    The summary should be short and clear.
    
    Notes: {notes}
    """
    
    # Getting the response from the LLM
    response = llm.invoke(prompt)
    
    # Updating and returning the Global State
    return {"summary": response}