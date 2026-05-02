from langgraph.graph import StateGraph, END
from state import AgentState
from agents import summarizer_agent, question_generator_agent, evaluator_agent, study_planner_agent
from tools import file_reader_tool, planner_formatter_tool, summary_saver_tool
from logger_config import logger

# Initialize the Workflow Graph
workflow = StateGraph(AgentState)

workflow.add_node("summarizer", summarizer_agent)
workflow.add_node("quiz_gen", question_generator_agent)
workflow.add_node("evaluator", evaluator_agent)
workflow.add_node("planner", study_planner_agent)

workflow.set_entry_point("summarizer")
workflow.add_edge("summarizer", "quiz_gen")
workflow.add_edge("quiz_gen", "evaluator")
workflow.add_edge("evaluator", "planner")
workflow.add_edge("planner", END)

app = workflow.compile()

if __name__ == "__main__":
    logger.info("=== EDUCATIONAL MULTI-AGENT SYSTEM INITIALIZED ===")

    content = file_reader_tool("notes.txt")

    if content and not content.startswith("Error"):
        result = app.invoke({"lecture_notes": content})

        print("\n" + "=" * 70)
        print("          COMPLETE MULTI-AGENT SYSTEM EXECUTION LOG          ")
        print("=" * 70)

        # Student 1 Output
        summary_out = result.get("summary", "No summary generated.")
        print(f"\n[STUDENT 1: SUMMARIZER OUTPUT]\n{'-' * 30}\n{summary_out}")
        summary_saver_tool(summary_out)

        # Student 2 Output
        quiz_out = result.get("quiz", "No quiz generated.")
        print(f"\n[STUDENT 2: QUESTION GENERATOR OUTPUT]\n{'-' * 30}\n{quiz_out}")
        print(f"\nQuiz file saved at: {result.get('quiz_file', 'No quiz file path available')}")

        # Student 3 Output
        print(f"\n[STUDENT 3: PERFORMANCE EVALUATOR OUTPUT]\n{'-' * 30}\n{result.get('grading_results')}")

        # Student 4 Output
        print(f"\n[STUDENT 4: STUDY PLANNER OUTPUT]\n{'-' * 30}\n{result.get('final_study_plan')}")
        planner_formatter_tool(result.get("final_study_plan"))

        logger.info("=== SYSTEM EXECUTION FINISHED SUCCESSFULLY ===")
    else:
        logger.error("System failed to start due to file reading error.")