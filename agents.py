from langchain_community.llms import Ollama
from state import AgentState

# Local LLM Engine [cite: 12]
llm = Ollama(model="llama3")

def summarizer_agent(state: AgentState):
    """
    පළපුරුදු ආචාර්යවරයෙකු ලෙස ක්‍රියා කරමින් සාරාංශයක් සාදයි. [cite: 25]
    """
    print("--- SUMMARIZING CONTENT ---") # Observability සඳහා [cite: 21]
    
    notes = state.get("lecture_notes", "")
    
    prompt = f"""
    ඔබ දක්ෂ විශ්වවිද්‍යාල ආචාර්යවරයෙකි. 
    පහත දැක්වෙන පාඩම් සටහන් කියවා එහි ඇති වැදගත් කරුණු පමණක් ඇතුළත් සාරාංශයක් සාදන්න.
    සටහන්: {notes}
    """
    
    response = llm.invoke(prompt)
    
    # State එක update කිරීම 
    return {"summary": response}