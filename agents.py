from langchain_ollama import OllamaLLM
from state import AgentState
from logger_config import logger
from tools import grader_tool

# Initialize the Local LLM (Phi)
llm = OllamaLLM(model="phi3")

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
    print("\n--- [AGENT 3] EVALUATING PERFORMANCE ---") # මෙන්න මේ පේළිය එකතු කරන්න
    logger.info("AGENT 3: Performance Evaluator task execution started.")
    quiz_data = state.get('quiz_questions', "")
    student_answers = state.get('student_answers', "")

    # 1. Input Validation: JSON එකක්ද කියලා බලන්න
    if not quiz_data:
        state['grading_results'] = "Evaluation Error: No quiz data found."
        return state

    # 2. Prompt Engineering (Critical for Assignment Rubric)
    # අපි LLM එකට හරියටම කියනවා JSON එක parse කරන්න කියලා.
    prompt = f"""
    SYSTEM: You are a strict University Academic Evaluator.
    TASK: Grade student answers based on the provided Quiz JSON.
    
    QUIZ DATA (JSON format):
    {quiz_data}
    
    STUDENT ANSWERS:
    {student_answers}
    
    INSTRUCTIONS:
    1. Iterate through the "questions" list in the JSON.
    2. For each question ID, find the corresponding student answer.
    3. Compare the student answer with the 'correct_answer' field.
    4. Calculate a percentage score (0-100).
    5. Generate a short feedback string explaining which questions were wrong.
    
    OUTPUT CONSTRAINT: Return ONLY a valid JSON object:
    {{"score": <int>, "feedback": "<string>"}}
    """
    
    # 3. LLM Reasoning
    # llm.invoke එකෙන් එන result එක JSON string එකක් විය යුතුයි.
    raw_grading = llm.invoke(prompt)
    
    # 4. Tool Usage: grading_results එක සේව් කරගැනීම
    # grader_tool එකට අපි මේ raw_grading එක යවනවා.
    tool_result = grader_tool(raw_grading)
    state['grading_results'] = tool_result
    
    logger.info("AGENT 3: Performance Evaluator task execution finished.")
    return state
# Student 4: The Study Planner
def study_planner_agent(state: AgentState):
    logger.info("AGENT 4: Study Planner task started.")
    prompt = f"SYSTEM: Study Consultant. TASK: 7-day schedule. EVALUATION: {state['grading_results']}"
    state['final_study_plan'] = llm.invoke(prompt)
    logger.info("AGENT 4: Study Planner completed the task.")
    return state