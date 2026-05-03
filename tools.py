import json
from logger_config import logger

# Student 1: File Reader
def file_reader_tool(file_path: str) -> str:
    """Used to read lecture notes from a local text file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            logger.info(f"File Reader Tool: Successfully read {file_path}")
            return content
    except Exception as e:
        logger.error(f"File Reader Tool Error: {str(e)}")
        return f"Error reading file: {str(e)}"

# Student 1: Summary Saver (අලුතින් එකතු කරන ලදී)
def summary_saver_tool(summary_text: str):
    """Saves the academic summary into a local file named summary.txt."""
    try:
        with open("summary.txt", "w", encoding='utf-8') as f:
            f.write(summary_text)
        logger.info("Summary Saver Tool: Successfully saved summary.txt")
        return "Summary saved to summary.txt"
    except Exception as e:
        logger.error(f"Summary Saver Tool Error: {str(e)}")
        return f"Error saving summary: {str(e)}"

# WIJESINGHE WACS -: Quiz Exporter
def quiz_exporter_tool(quiz_content: str):
    """Saves the generated quiz questions into a JSON file."""
    try:
        with open("quiz.json", "w", encoding='utf-8') as f:
            json.dump({"quiz": quiz_content}, f, ensure_ascii=False, indent=4)
        logger.info("Quiz Exporter Tool: Successfully exported quiz.json")
        return "Quiz saved to quiz.json"
    except Exception as e:
        logger.error(f"Quiz Exporter Tool Error: {str(e)}")
        return f"Error saving quiz: {str(e)}"

# Student 3: Grader Tool (Internal Logic Only)
def grader_tool(score: int) -> str:
    """Determines the academic performance level based on the score provided."""
    result = "Pass" if score >= 50 else "Needs Improvement"
    logger.info(f"Grader Tool: Classified score {score} as {result}")
    return result

# Student 4: Planner Formatter
def planner_formatter_tool(plan: str):
    """Saves the finalized study plan into a text file."""
    try:
        with open("study_plan.txt", "w", encoding='utf-8') as f:
            f.write(plan)
        logger.info("Planner Formatter Tool: Successfully saved study_plan.txt")
        return "Study plan saved to study_plan.txt"
    except Exception as e:
        logger.error(f"Planner Formatter Tool Error: {str(e)}")
        return f"Error saving study plan: {str(e)}"