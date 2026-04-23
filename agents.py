from langchain_ollama import OllamaLLM
from state import AgentState

# Local LLM Engine එක සම්බන්ධ කිරීම (llama3 භාවිතා කරයි) [cite: 12, 14]
llm = OllamaLLM(model="llama3")

def summarizer_agent(state: AgentState):
    """
    පළපුරුදු විශ්වවිද්‍යාල ආචාර්යවරයෙකු ලෙස ක්‍රියා කරමින් සාරාංශයක් සාදයි[cite: 25, 43].
    මෙම ඒජන්තවරයා සටහන් කියවා වැදගත් කරුණු පමණක් ලබා දෙයි[cite: 6, 9].
    """
    # පද්ධතියේ ක්‍රියාකාරිත්වය නිරීක්ෂණය සඳහා (Observability) [cite: 21, 54]
    print("\n--- [AGENT] SUMMARIZING CONTENT ---") 
    
    # Global State එකෙන් දත්ත ලබා ගැනීම [cite: 20, 46]
    notes = state.get("lecture_notes", "")
    
    # Prompt Engineering: Persona සහ Constraints ඇතුළත් වේ [cite: 25, 43, 56]
    prompt = f"""
    ඔබ දක්ෂ විශ්වවිද්‍යාල ආචාර්යවරයෙකි. 
    පහත දැක්වෙන පාඩම් සටහන් කියවා එහි ඇති වැදගත් කරුණු පමණක් ඇතුළත් සාරාංශයක් සාදන්න.
    සාරාංශය කෙටි සහ පැහැදිලි විය යුතුය.
    
    සටහන්: {notes}
    """
    
    # LLM එකෙන් පිළිතුර ලබා ගැනීම [cite: 9]
    response = llm.invoke(prompt)
    
    # Global State එක යාවත්කාලීන කර ආපසු යැවීම [cite: 20, 46]
    return {"summary": response}