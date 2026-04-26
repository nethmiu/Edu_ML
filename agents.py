from langchain_ollama import OllamaLLM
from state import AgentState
from logger_config import logger

# Initialize the Local LLM (Llama 3)
llm = OllamaLLM(model="llama3")

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
    logger.info("AGENT 3: Evaluator task started.")
    prompt = f"SYSTEM: Academic Evaluator. TASK: Grade understanding. QUIZ: {state['quiz_questions']}"
    state['grading_results'] = llm.invoke(prompt)
    logger.info("AGENT 3: Evaluator completed the task.")
    return state

# Student 4: The Study Planner
def study_planner_agent(state: AgentState):
    logger.info("AGENT 4: Study Planner task started.")
    prompt = f"SYSTEM: Study Consultant. TASK: 7-day schedule. EVALUATION: {state['grading_results']}"
    state['final_study_plan'] = llm.invoke(prompt)
    logger.info("AGENT 4: Study Planner completed the task.")
    return state