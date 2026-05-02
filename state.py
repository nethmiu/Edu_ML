from typing import TypedDict, Any


class AgentState(TypedDict, total=False):
    lecture_notes: str
    topic: str
    summary: str
    quiz: Any
    quiz_file: str
    grading_results: str
    final_study_plan: str