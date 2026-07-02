import json
from pathlib import Path

from app.services.draft_service import generate_draft_reply


DATA_PATH = Path("data/sample_emails.jsonl")


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

    for example in examples:
        prediction = generate_draft_reply(example["email_body"])
        predicted_intent = prediction["intent"]
        expected_intent = example["intent"]

        if predicted_intent == expected_intent:
            correct += 1
        else:
            print("Wrong prediction:")
            print(f"Email: {example['email_body']}")
            print(f"Expected: {expected_intent}")
            print(f"Predicted: {predicted_intent}")
            print()

    accuracy = correct / total if total > 0 else 0

    print(f"Intent accuracy: {accuracy:.2%}")
    print(f"Correct: {correct}/{total}")


if __name__ == "__main__":
    evaluate_intents()