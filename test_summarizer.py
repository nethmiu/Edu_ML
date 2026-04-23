# test_summarizer.py (යාවත්කාලීන කළ හැකි ආකාරය)
from agents import summarizer_agent

def test_summarizer_logic():
    print("\n--- STARTING EVALUATION TEST ---")
    
    # 1. Test Input එකක් ලබා දීම
    test_state = {"lecture_notes": "Agentic AI uses autonomous agents to solve complex problems."}
    
    # 2. Agent ක්‍රියාත්මක කිරීම
    result = summarizer_agent(test_state)
    summary_text = result.get("summary", "")
    
    # 3. පරීක්ෂණ (Assertions) [cite: 27, 52]
    assert "summary" in result, "Result එකේ summary key එක තිබිය යුතුයි."
    assert len(summary_text) > 20, "සාරාංශය ඉතා කෙටි වැඩි විය නොහැක."
    
    # Security check: Error එකක් ආවාදැයි බැලීම
    assert "Error" not in summary_text, "සාරාංශයේ Error එකක් අඩංගු නොවිය යුතුය."
    
    print("Test Result: summary generation passed accuracy checks!")

if __name__ == "__main__":
    test_summarizer_logic()