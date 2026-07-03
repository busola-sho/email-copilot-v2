import json
from pathlib import Path

from app.services.draft_service import generate_draft_reply


DATA_PATH = Path("data/sample_emails.jsonl")
REPORT_PATH = Path("reports/intent_eval.json")


def load_examples(path: Path):
    examples = []

    with path.open("r", encoding="utf-8") as file:
        for line in file:
            examples.append(json.loads(line))

    return examples


def evaluate_intents():
    examples = load_examples(DATA_PATH)

    total = len(examples)
    correct = 0
    mistakes = []

    for example in examples:
        prediction = generate_draft_reply(example["email_body"])
        predicted_intent = prediction["intent"]
        expected_intent = example["intent"]

        if predicted_intent == expected_intent:
            correct += 1
        else:
            mistakes.append(
                {
                    "email_body": example["email_body"],
                    "expected_intent": expected_intent,
                    "predicted_intent": predicted_intent,
                }
            )

    accuracy = correct / total if total > 0 else 0

    report = {
        "total_examples": total,
        "correct": correct,
        "accuracy": accuracy,
        "mistakes": mistakes,
    }

    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)

    with REPORT_PATH.open("w", encoding="utf-8") as file:
        json.dump(report, file, indent=2)

    print(f"Intent accuracy: {accuracy:.2%}")
    print(f"Correct: {correct}/{total}")
    print(f"Saved report to {REPORT_PATH}")


if __name__ == "__main__":
    evaluate_intents()