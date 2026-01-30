from tools import SearchAgent


def main():
    """Run interactive terminal agent."""
    agent = SearchAgent()

    print("=" * 70)
    print("Research Assistant for Dutch Government Organizations")
    print("=" * 70)
    print("\nType 'quit' or 'exit' to end the conversation.")
    print("Type 'reset' to clear conversation history.\n")

    while True:
        try:
            query = input("You: ").strip()

            if not query:
                continue

            if query.lower() in ["quit", "exit", "q"]:
                print("\nGoodbye!")
                break

            if query.lower() == "reset":
                agent.reset()
                print("Conversation history cleared.\n")
                continue

            print()
            result = agent.ask(query)

            print(f"\nAssistant: {result.answer}\n")

            if result.citations:
                print("Citations:")
                for citation in result.citations:
                    source = citation.url or f"Section {citation.section}"
                    print(f"  {source}: {citation.text[:100]}...")
                print()

        except KeyboardInterrupt:
            print("\n\nGoodbye!")
            break
        except Exception as e:
            print(f"\nError: {e}\n")


if __name__ == "__main__":
    main()
