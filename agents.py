from langchain_ollama import OllamaLLM
from state import AgentState
from logger_config import logger
from quiz_generator.question_generator import QuestionGeneratorAgent

# Shared local LLM for Student 1, 3, and 4
llm = OllamaLLM(model="llama3")

# WIJESINGHE WACS - integrated component
question_gen_runner = QuestionGeneratorAgent(model_name="llama3")


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

    state["summary"] = llm.invoke(prompt)
    logger.info("AGENT 1: Summarizer completed the task.")
    return state


# WIJESINGHE W.A.C.S : The Quiz Generator
def question_generator_agent(state: AgentState):
    logger.info("AGENT 2: Question Generator task started.")
    print("\n--- [AGENT 2] GENERATING QUIZ ---")

    updated_state = question_gen_runner.run(state, output_path="quiz.json")

    logger.info("AGENT 2: Question Generator completed the task.")
    return updated_state


# Student 3: The Performance Evaluator
def evaluator_agent(state: AgentState):
    logger.info("AGENT 3: Evaluator task started.")
    print("\n--- [AGENT 3] EVALUATING PERFORMANCE ---")

    prompt = f"""
    SYSTEM: Academic Evaluator.
    TASK: Grade the student's understanding based on the generated quiz.
    QUIZ: {state['quiz']}
    """

    state["grading_results"] = llm.invoke(prompt)
    logger.info("AGENT 3: Evaluator completed the task.")
    return state


# Student 4: The Study Planner
def study_planner_agent(state: AgentState):
    logger.info("AGENT 4: Study Planner task started.")
    print("\n--- [AGENT 4] BUILDING STUDY PLAN ---")

    prompt = f"""
    SYSTEM: Study Consultant.
    TASK: Create a 7-day study schedule based on the evaluation results.
    EVALUATION: {state['grading_results']}
    """

    state["final_study_plan"] = llm.invoke(prompt)
    logger.info("AGENT 4: Study Planner completed the task.")
    return state