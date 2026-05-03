import json
from pathlib import Path
from quiz_generator.quiz_schema import Quiz


def export_quiz_to_json(quiz: Quiz, output_path: str) -> str:
    """
    Export a validated quiz object to a JSON file.

    Args:
        quiz: A validated Quiz object.
        output_path: Path where the JSON file should be saved.

    Returns:
        The absolute path to the saved JSON file.
    """
    if not output_path.strip():
        raise ValueError("Output path cannot be empty.")

    path = Path(output_path)

    if path.parent != Path(""):
        path.parent.mkdir(parents=True, exist_ok=True)

    with path.open("w", encoding="utf-8") as file:
        json.dump(quiz.model_dump(), file, indent=2, ensure_ascii=False)

    return str(path.resolve())