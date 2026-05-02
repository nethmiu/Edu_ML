import json
import logging
from pathlib import Path
from typing import Any, Dict

from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import ChatOllama

from quiz_generator.quiz_schema import Quiz
from quiz_generator.quiz_exporter import export_quiz_to_json
from quiz_generator.validator import validate_quiz_content


def setup_logger() -> logging.Logger:
    """
    Configure and return a logger for the Question Generator Agent.
    Logs are written to both console and question_generator.log.
    """
    logger = logging.getLogger("question_generator")
    logger.setLevel(logging.INFO)

    if logger.handlers:
        return logger

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
    )

    file_handler = logging.FileHandler("question_generator.log", encoding="utf-8")
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(formatter)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger


class QuestionGeneratorAgent:
    """
    Agent responsible for generating structured MCQ quizzes
    from summarized lesson content using a local Ollama model.
    """

    def __init__(self, model_name: str = "llama3") -> None:
        self.model_name = model_name
        self.logger = setup_logger()

        self.llm = ChatOllama(
            model=model_name,
            temperature=0.3
        )

        prompt_path = Path("quiz_generator/question_generator_prompt.txt")
        self.system_prompt = prompt_path.read_text(encoding="utf-8")

        # Escape literal JSON braces in the system prompt
        self.system_prompt = self.system_prompt.replace("{", "{{").replace("}", "}}")

        self.prompt = ChatPromptTemplate.from_messages(
            [
                ("system", self.system_prompt),
                (
                    "user",
                    (
                        "Generate a quiz for the following topic and summary.\n\n"
                        "Topic: {topic}\n"
                        "Summary: {summary}\n"
                    ),
                ),
            ]
        )

        self.logger.info("QuestionGeneratorAgent initialized with model: %s", self.model_name)

    def generate_quiz(self, topic: str, summary: str) -> Quiz:
        """
        Generate a validated Quiz object from topic and summary input.
        """
        topic = topic.strip()
        summary = summary.strip()

        if not topic:
            self.logger.error("Topic is empty.")
            raise ValueError("Topic cannot be empty.")

        if not summary:
            self.logger.error("Summary is empty.")
            raise ValueError("Summary cannot be empty.")

        self.logger.info("Generating quiz for topic: %s", topic)
        self.logger.info("Summary length: %d characters", len(summary))

        chain = self.prompt | self.llm
        response = chain.invoke({"topic": topic, "summary": summary})

        raw_text = response.content.strip()
        self.logger.info("Received raw response from model.")

        # Save raw response for debugging
        Path("last_quiz_raw_response.txt").write_text(raw_text, encoding="utf-8")

        if raw_text.startswith("```json"):
            raw_text = raw_text.removeprefix("```json").removesuffix("```").strip()
        elif raw_text.startswith("```"):
            raw_text = raw_text.removeprefix("```").removesuffix("```").strip()

        # Try direct JSON parse first
        try:
            quiz_dict = json.loads(raw_text)
        except json.JSONDecodeError:
            # Try extracting the first JSON object from the text
            start = raw_text.find("{")
            end = raw_text.rfind("}")
            if start != -1 and end != -1 and end > start:
                possible_json = raw_text[start:end + 1]
                try:
                    quiz_dict = json.loads(possible_json)
                except json.JSONDecodeError as e:
                    self.logger.error("Failed to parse extracted JSON.")
                    self.logger.error("Raw model output saved to last_quiz_raw_response.txt")
                    raise ValueError("Model returned invalid JSON format.") from e
            else:
                self.logger.error("No JSON object found in model response.")
                self.logger.error("Raw model output saved to last_quiz_raw_response.txt")
                raise ValueError("Model did not return JSON output.")

        quiz = Quiz(**quiz_dict)
        validate_quiz_content(quiz)

        self.logger.info("Quiz validation successful. Generated %d questions.", len(quiz.questions))
        return quiz

    def run(self, state: Dict[str, Any], output_path: str = "quiz.json") -> Dict[str, Any]:
        """
        Execute the full question generation flow.

        Input rules:
        - summary is required
        - topic is optional

        Output:
        - updated_state["quiz"]
        - updated_state["quiz_file"]
        """
        topic = state.get("topic", "Generated Quiz")
        summary = state.get("summary", "")

        self.logger.info("Run started.")
        self.logger.info("Received topic: %s", topic)
        self.logger.info("Using model: %s", self.model_name)

        if not summary or not str(summary).strip():
            self.logger.error("Summary is missing from state.")
            raise ValueError("Summary cannot be empty.")

        quiz = self.generate_quiz(topic=topic, summary=summary)
        saved_path = export_quiz_to_json(quiz, output_path)

        self.logger.info("Quiz exported successfully to: %s", saved_path)
        self.logger.info("Run completed successfully.")

        updated_state = dict(state)
        updated_state["quiz"] = quiz.model_dump()
        updated_state["quiz_file"] = saved_path

        return updated_state