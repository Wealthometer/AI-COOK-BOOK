import json

import nest_asyncio
from pydantic_ai import Agent, ModelMessage

nest_asyncio.apply()

# --------------------------------------------------------------
# Accessing messages from results
# --------------------------------------------------------------

agent = Agent("openai:gpt-4o-mini", instructions="Be a helpful assistant.")

result = agent.run_sync("Tell me a joke")
print(result.output)

print("\n--- All Messages ---")
print(result.all_messages())

print("\n--- New Messages ---")
print(result.new_messages())

# --------------------------------------------------------------
# Continue conversation with message history
# --------------------------------------------------------------

result1 = agent.run_sync("What is the capital of France?")
print(result1.output)

result2 = agent.run_sync(
    "What's the population?", message_history=result1.new_messages()
)
print(result2.output)

print("\n--- Full Conversation History ---")
for msg in result2.all_messages():
    print(f"{msg.kind}: {msg}")

# --------------------------------------------------------------
# Store and load messages as JSON
# --------------------------------------------------------------

result = agent.run_sync("What is 2 + 2?")

messages_json = result.all_messages_json()
print("\n--- Messages as JSON ---")
print(json.loads(messages_json)[:1])

loaded_messages = json.loads(messages_json)
print(f"\nLoaded {len(loaded_messages)} messages from JSON")

# --------------------------------------------------------------
# Processing message history - keep only recent messages
# --------------------------------------------------------------


def keep_recent_messages(messages: list[ModelMessage]) -> list[ModelMessage]:
    """Keep only the last 3 messages to manage token usage."""
    return messages[-3:] if len(messages) > 3 else messages


history_agent = Agent(
    "openai:gpt-4o-mini",
    instructions="Be concise.",
    history_processors=[keep_recent_messages],
)

msg_history = []
for i in range(5):
    result = history_agent.run_sync(f"Message {i + 1}", message_history=msg_history)
    msg_history = result.all_messages()
    print(f"Turn {i + 1}: {len(msg_history)} messages in history")
