from langchain_ollama import OllamaLLM
from state import AgentState
from logger_config import logger
from tools import grader_tool

# Initialize the Local LLM (Phi)
llm = OllamaLLM(model="phi")

# Student 1: The Content Summarizer
def summarizer_agent(state: AgentState):
    logger.info("AGENT 1: Summarizer task execution started.")
    print("\n--- [AGENT 1] SUMMARIZING CONTENT ---")
    prompt = f"""
    SYSTEM: You are a distinguished University Professor. 
    TASK: Summarize the following lecture notes into a professional academic abstract. 
    CONSTRAINT: Focus on core concepts and eliminate redundant information. Use only English.
    
    NOTES: {state['lecture_notes']}
    """
    state['summary'] = llm.invoke(prompt)
    logger.info("AGENT 1: Summarizer completed the task.")
    return state

# Student 2: The Question Generator
def question_generator_agent(state: AgentState):
    logger.info("AGENT 2: Question Generator task started.")
    prompt = f"SYSTEM: Senior Examiner. TASK: Generate 3 MCQs. SUMMARY: {state['summary']}"
    state['quiz_questions'] = llm.invoke(prompt)
    logger.info("AGENT 2: Question Generator completed the task.")
    return state

# Student 3: The Performance Evaluator
def evaluator_agent(state: AgentState):
    logger.info("AGENT 3: Performance Evaluator task execution started.")
    print("\n--- [AGENT 3] EVALUATING PERFORMANCE ---")
    
    # Safeguard for empty quiz data from Agent 2
    quiz_data = state.get('quiz_questions', "")
    if not quiz_data or len(str(quiz_data).strip()) < 5:
        logger.warning("AGENT 3: Quiz questions are missing. Cannot evaluate properly.")
        state['grading_results'] = "Evaluation Error: No quiz questions were provided for comparison."
        return state

    # Prompt engineering designed for Small Language Models (SLMs)
    prompt = f"""
    SYSTEM: You are a strict University Academic Evaluator. 
    TASK: Grade the student's answers based on the correct answers in the Quiz Data.
    
    QUIZ DATA: {quiz_data}
    STUDENT ANSWERS: {state.get('student_answers')}
    
    SCORING EXAMPLES:
    - If answer matches 'Supervised', Score: 100
    - If answer matches 'A straight line', Score: 100
    - If answer is wrong, Score: 0
    
    FORMAT: Return ONLY a JSON object: {{"score": <int>, "feedback": "<string>"}}
    JSON:"""
    
    # 1. LLM Reasoning
    raw_grading = llm.invoke(prompt)
    
    # 2. Tool Usage (Saves to grades.json and updates state)
    tool_summary = grader_tool(raw_grading)
    state['grading_results'] = tool_summary
    
    logger.info("AGENT 3: Performance Evaluator task execution finished.")
    return state
# Student 4: The Study Planner
def study_planner_agent(state: AgentState):
    logger.info("AGENT 4: Study Planner task started.")
    prompt = f"SYSTEM: Study Consultant. TASK: 7-day schedule. EVALUATION: {state['grading_results']}"
    state['final_study_plan'] = llm.invoke(prompt)
    logger.info("AGENT 4: Study Planner completed the task.")
    return state