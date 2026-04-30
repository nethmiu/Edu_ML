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

# Student 2: Quiz Exporter
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

from typing import Dict, Union

# Student 3: Grader Tool
def grader_tool(grading_json: str) -> str:
    """
    Parses the evaluation JSON, determines the performance level, and saves grades to a file.
    
    Args:
        grading_json (str): A JSON-formatted string containing 'score' and 'feedback'.
        
    Returns:
        str: A summary message of the grading process result.
        
    Raises:
        ValueError: If the score is not within the valid range of 0-100.
    """
    import re
    import ast
    try:

        match = re.search(r'\{.*\}', grading_json, re.DOTALL)
        clean_json = match.group(0) if match else grading_json
            
        try:
            data: Dict[str, Union[int, str]] = json.loads(clean_json)
        except json.JSONDecodeError:
        
            data = ast.literal_eval(clean_json)
            
        score = int(data.get("score", 0))
        feedback = str(data.get("feedback", "No feedback provided."))
        
        if not (0 <= score <= 100):
            logger.warning(f"Grader Tool: Received out-of-range score {score}. Normalizing to 0-100.")
            score = max(0, min(100, score))
            
    except (json.JSONDecodeError, ValueError) as e:
        logger.error(f"Grader Tool Parsing Error: {str(e)}")
        score = 0
        feedback = f"Error parsing evaluation: {grading_json[:100]}..."
    except Exception as e:
        logger.error(f"Grader Tool Unexpected Error: {str(e)}")
        score = 0
        feedback = "An unexpected error occurred during grading."

    try:
        result = "Pass" if score >= 50 else "Needs Improvement"
        
        with open("grades.json", "w", encoding='utf-8') as f:
            json.dump({
                "score": score, 
                "status": result, 
                "feedback": feedback
            }, f, ensure_ascii=False, indent=4)
            
        logger.info(f"Grader Tool: Successfully processed score {score} ({result})")
        return f"Grader Output: Score {score}/100 ({result})\nFeedback: {feedback}"
    except Exception as e:
        logger.error(f"Grader Tool File Error: {str(e)}")
        return f"Error saving grade to file: {str(e)}"

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