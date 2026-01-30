from datetime import date
import json
from typing import Literal

import nest_asyncio
from pydantic import BaseModel
from pydantic_ai import Agent, RunContext

nest_asyncio.apply()

# --------------------------------------------------------------
# Without dependencies - limited context
# --------------------------------------------------------------

agent = Agent(
    "openai:gpt-4o-mini",
    instructions="You are a helpful customer service agent.",
)

result = agent.run_sync(user_prompt="What's my account status?")
print(result.output)

# --------------------------------------------------------------
# With dependencies - inject runtime data
# --------------------------------------------------------------


class Customer(BaseModel):
    name: str
    account_id: str
    status: Literal["Active", "Inactive"]


agent = Agent(
    "openai:gpt-4o-mini",
    deps_type=Customer,
    instructions="You are a helpful customer service agent.",
)


@agent.instructions
def add_customer_context(ctx: RunContext[Customer]) -> str:
    customer = ctx.deps
    return f"Customer: {customer.name} (ID: {customer.account_id}, Status: {customer.status})"


@agent.instructions
def add_current_date() -> str:
    return f"Today's date: {date.today()}"


customer = Customer(
    name="Alice",
    account_id="C001",
    status="Active",
)
result = agent.run_sync(user_prompt="What's my account status?", deps=customer)
print(result.output)

# --------------------------------------------------------------
# Different customer, same agent
# --------------------------------------------------------------

another_customer = Customer(
    name="Bob",
    account_id="C002",
    status="Inactive",
)
result = agent.run_sync(user_prompt="What's my account status?", deps=another_customer)
print(result.output)


# --------------------------------------------------------------
# Let's explore the result
# --------------------------------------------------------------

messages = json.loads(result.all_messages_json())
print(json.dumps(messages, indent=2))


# --------------------------------------------------------------
# Why you want type-safe dependencies
# --------------------------------------------------------------

wacky_agent = Agent(
    "openai:gpt-4o-mini",
    instructions="You are a helpful customer service agent.",
)


@wacky_agent.instructions
def add_customer_context(customer: str) -> str:
    return f"Customer: {customer}"


yet_another_customer = "Bob"
result = wacky_agent.run_sync(user_prompt="What's my account status?")
print(result.output)  # Results in generic chatbot error that will go unnoticed
