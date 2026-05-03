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
    print("\n--- [AGENT 4] GENERATING PERSONALIZED STUDY PLAN ---")

    grading = state.get('grading_results', '')

    prompt = f"""
SYSTEM: You are an expert academic study coach. You create weekly study schedules for students.

TASK: Read the student performance evaluation below and create a 7-day study schedule.

STRICT RULES:
1. You are the COACH, NOT the student. Do NOT say "thank you" or respond as a student.
2. Do NOT say "What do you think?" or ask any questions at the end.
3. Produce a schedule for exactly 7 days: Monday to Sunday.
4. Give more study time to topics where the student scored lower.
5. Format each day exactly like this:

MONDAY:
- 08:00-10:00 | [Topic Name] | Priority: HIGH | Goal: [what to study]

TUESDAY:
- 09:00-10:30 | [Topic Name] | Priority: MEDIUM | Goal: [what to study]

6. End with a STUDY TIPS section with 3 practical tips.
7. Only use topics mentioned in the evaluation. Do not invent new topics.
8. Write in English only. Be direct and structured. Do not add any closing remarks.

STUDENT PERFORMANCE EVALUATION:
{grading}

Now write the 7-day study schedule:
"""

    try:
        raw_plan = llm.invoke(prompt)
        logger.info("AGENT 4: LLM successfully generated study plan.")
    except Exception as e:
        logger.error(f"AGENT 4: LLM failed — {e}")
        state['final_study_plan'] = f"Error: {str(e)}"
        return state

    from tools import planner_formatter_tool
    save_result = planner_formatter_tool(raw_plan)
    logger.info(f"AGENT 4: Tool result — {save_result}")

    state['final_study_plan'] = raw_plan
    logger.info("AGENT 4: Study Planner completed successfully.")
    return state