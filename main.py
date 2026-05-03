from langgraph.graph import StateGraph, END
from state import AgentState
from agents import summarizer_agent, question_generator_agent, evaluator_agent, study_planner_agent
from tools import file_reader_tool, planner_formatter_tool, quiz_exporter_tool, summary_saver_tool, grader_tool
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
        # Mock student answers matching the Linear Regression Quiz Data
        mock_student_answers = "1. Continuous Numerical. 2. The relationship between dependent and independent variables. 3. Forecasting and trend analysis. 4. Supervised. 5. A straight line."
        
        result = app.invoke({
            "lecture_notes": content,
            "student_answers": mock_student_answers
        })
        
        print("\n" + "="*70)
        print("          COMPLETE MULTI-AGENT SYSTEM EXECUTION LOG          ")
        print("="*70)
        
        # Student 1 Output processing
        summary_out = result.get('summary', 'No summary generated.')
        print(f"\n[STUDENT 1: SUMMARIZER OUTPUT]\n{'-'*30}\n{summary_out}")
        summary_saver_tool(summary_out) # Summary එක වෙනම සේව් කිරීම
        
        # Other Outputs
        print(f"\n[STUDENT 2: QUESTION GENERATOR OUTPUT]\n{'-'*30}\n{result.get('quiz_questions')}")
        quiz_exporter_tool(result.get('quiz_questions'))
        
        print(f"\n[STUDENT 3: PERFORMANCE EVALUATOR OUTPUT]\n{'-'*30}")
        print(result.get('grading_results', 'No evaluation generated.'))
        
        print(f"\n[STUDENT 4: STUDY PLANNER OUTPUT]\n{'-'*30}\n{result.get('final_study_plan')}")
        planner_formatter_tool(result.get('final_study_plan'))
        
        logger.info("=== SYSTEM EXECUTION FINISHED SUCCESSFULLY ===")
    else:
        logger.error("System failed to start due to file reading error.")