from typing import TypedDict, Annotated, List

# පද්ධතිය පුරා හුවමාරු වන දත්ත ව්‍යුහය 
class AgentState(TypedDict):
    lecture_notes: str        # Student 1 ලබාගන්නා දත්ත
    summary: str              # Student 1 නිපදවන සාරාංශය
    quiz_questions: List[str] # Student 2 සඳහා
    student_answers: str      # Student 3 සඳහා (mock answers)
    grading_results: str      # Student 3 සඳහා
    final_study_plan: str     # Student 4 සඳහා