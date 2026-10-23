from assistant_core.service import AssistantService


def main():
    service = AssistantService()
    question = " ".join(__import__("sys").argv[1:])

    if not question:
        print("Please provide a question.")
        return

    response = service.handle(question)
    print(response)


if __name__ == "__main__":
    main()