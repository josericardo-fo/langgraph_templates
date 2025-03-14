from templates.chatbot_summary import get_response


def main():
    while True:
        message = input("You: ")
        response = get_response(message)
        print(f"\nBot: {response}\n")


if __name__ == "__main__":
    main()
