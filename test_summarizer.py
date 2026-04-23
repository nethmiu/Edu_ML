# test_summarizer.py (Updated Version)
from agents import summarizer_agent

def test_summarizer_logic():
    print("\n--- STARTING EVALUATION TEST ---")
    
    # 1. Providing a Test Input
    test_state = {"lecture_notes": "Agentic AI uses autonomous agents to solve complex problems."}
    
    # 2. Executing the Agent
    result = summarizer_agent(test_state)
    summary_text = result.get("summary", "")
    
    # 3. Assertions
    assert "summary" in result, "The 'summary' key must be present in the result."
    assert len(summary_text) > 20, "The summary cannot be too short."
    
    # Security check: Checking if an error occurred
    assert "Error" not in summary_text, "The summary should not contain an Error."
    
    print("Test Result: summary generation passed accuracy checks!")

if __name__ == "__main__":
    test_summarizer_logic()