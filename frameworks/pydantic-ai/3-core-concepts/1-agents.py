from datetime import date
import json

import nest_asyncio
from pydantic_ai import Agent

nest_asyncio.apply()

# --------------------------------------------------------------
# Static instructions - defined at agent creation
# --------------------------------------------------------------

agent = Agent(
    "openai:gpt-4o-mini",
    instructions="You are a helpful assistant. Be concise.",
)

result = agent.run_sync(user_prompt="What is Python?")
print(result.output)

# --------------------------------------------------------------
# Dynamic instructions - computed at runtime
# --------------------------------------------------------------

agent = Agent("openai:gpt-4o-mini")


@agent.instructions
def add_date() -> str:
    return f"Today's date is {date.today()}."


@agent.instructions
def add_context() -> str:
    return "Use a friendly, conversational tone."


result = agent.run_sync(user_prompt="What day is it?")
print(result.output)

# --------------------------------------------------------------
# Combining static and dynamic instructions
# --------------------------------------------------------------

agent = Agent(
    "openai:gpt-4o-mini",
    instructions="You are a helpful assistant.",
)


@agent.instructions
def add_timestamp() -> str:
    return f"Current date: {date.today()}"


result = agent.run_sync(user_prompt="What year are we in?")
print(result.output)

# --------------------------------------------------------------
# Let's explore the result
# --------------------------------------------------------------

print(result.all_messages())

messages = json.loads(result.all_messages_json())
print(json.dumps(messages, indent=2))
