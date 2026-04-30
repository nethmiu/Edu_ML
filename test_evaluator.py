import json
import os
import ast
from agents import evaluator_agent

def test_evaluator_agent():
    """
    Comprehensive evaluation script for Agent 3 (Performance Evaluator).
    Validates:
    1. Agent logic (High score for correct answers, low score for incorrect).
    2. Tool usage (Persistence to grades.json).
    3. Output format (Handled tool summary strings).
    """
    print("\n" + "="*50)
    print("      AGENT 3: COMPREHENSIVE EVALUATION TEST      ")
    print("="*50)
    
    # Mock Quiz Data (Agent 2 Output)
    quiz_data = {
        "topic": "Microservices",
        "questions": [
            {
                "id": 1,
                "question": "What is microservices architecture?",
                "correct_answer": "Independent services"
            }
        ]
    }
    quiz_str = json.dumps(quiz_data)

    test_cases = [
        {
            "name": "CORRECT CASE",
            "answers": "1. Independent services.",
            "min_expected_score": 50
        },
        {
            "name": "WRONG CASE",
            "answers": "1. Monolithic application.",
            "max_expected_score": 10
        }
    ]

    for case in test_cases:
        print(f"\n[RUNNING TEST]: {case['name']}")
        
        state = {
            "quiz_questions": quiz_str,
            "student_answers": case['answers'],
            "grading_results": ""
        }
        
        # Invoke Agent
        result_state = evaluator_agent(state)
        output = result_state.get('grading_results', "")
        
        print(f"Agent Output: {output}")
        
        # Verify Tool Persistence (Check grades.json)
        if os.path.exists("grades.json"):
            with open("grades.json", "r") as f:
                saved_data = json.load(f)
                score = saved_data.get("score", 0)
                print(f"Verified grades.json - Score: {score}")
                
                # Accuracy Checks
                if "min_expected_score" in case:
                    assert score >= case['min_expected_score'], f"Score {score} too low for {case['name']}"
                if "max_expected_score" in case:
                    assert score <= case['max_expected_score'], f"Score {score} too high for {case['name']}"
        else:
            print("ERROR: grades.json was not created!")
            assert False, "Tool failed to create output file."

    print("\n" + "="*50)
    print("      ALL AGENT 3 EVALUATION TESTS PASSED!      ")
    print("="*50)

if __name__ == "__main__":
    try:
        test_evaluator_agent()
    except AssertionError as e:
        print(f"\n[TEST FAILED]: {str(e)}")
    except Exception as e:
        print(f"\n[UNEXPECTED ERROR]: {str(e)}")
