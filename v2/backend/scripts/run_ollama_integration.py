from app.services.llm_client import LLMClient


def main():
    client = LLMClient()

    email_body = (
        "Hi, can we reschedule our meeting to Friday afternoon? "
        "Also, do you like food?"
    )

    draft = client.generate_llm_reply(email_body)

    print("\nInput email:")
    print(email_body)

    print("\nGenerated draft:")
    print(draft)


if __name__ == "__main__":
    main()