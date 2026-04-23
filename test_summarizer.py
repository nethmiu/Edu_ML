# test_summarizer.py
from agents import summarizer_agent

def test_summary_not_empty():
    """
    සාරාංශය හිස් නොවන බව සහ යම් අවම දිගකින් යුක්ත බව පරීක්ෂා කිරීම.
    """
    test_state = {"lecture_notes": "Python is a programming language. It is easy to learn."}
    result = summarizer_agent(test_state)
    
    assert "summary" in result
    assert len(result["summary"]) > 10
    print("Test Passed: Summary generated successfully!")

if __name__ == "__main__":
    test_summary_not_empty()