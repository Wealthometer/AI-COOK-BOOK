from typing import Literal
from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIChatModel
from pydantic import BaseModel
import nest_asyncio

nest_asyncio.apply()  # Needed to run interactive python


# --------------------------------------------------------------
# Use a chat model by name
# --------------------------------------------------------------

agent = Agent(
    model="openai:gpt-4o-mini",  # Specify the model to use
    instructions="Be concise, reply with one sentence.",  # Specify the instructions (system prompt)
)

result = agent.run_sync(user_prompt='Where does "hello world" come from?')
print(result.output)
print(type(result))

# --------------------------------------------------------------
# Use a chat model by model object
# --------------------------------------------------------------

model = OpenAIChatModel("gpt-4o-mini")  # Initialize the model
agent = Agent(
    model,
    instructions="Be concise, reply with one sentence.",
    model_settings={
        "temperature": 0.0,  # Add model settings here
    },
)

result = agent.run_sync(user_prompt='Where does "hello world" come from?')
print(result.output)


# --------------------------------------------------------------
# Using structured outputs
# --------------------------------------------------------------


class TicketCategory(BaseModel):
    category: Literal["general", "order", "billing"]


agent = Agent(
    model="openai:gpt-4o-mini",
    output_type=TicketCategory,
    instructions="Classify the following message into a category",
)

ticket = "I would like to place an order."

result: TicketCategory = agent.run_sync(user_prompt=ticket)
print(result.output)
assert result.output.category == "order"
