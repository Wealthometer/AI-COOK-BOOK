import nest_asyncio
from pydantic import BaseModel
from pydantic_ai import Agent, RunContext, ModelResponse

nest_asyncio.apply()


# --------------------------------------------------------------
# Basic output
# --------------------------------------------------------------


class CityLocation(BaseModel):
    city: str
    country: str


agent = Agent("openai:gpt-4o-mini", output_type=CityLocation)
result = agent.run_sync("Where were the olympics held in 2012?")

print(result.output)
print(result.usage())

# --------------------------------------------------------------
# Returning either text or structured data
# --------------------------------------------------------------


class Box(BaseModel):
    width: int
    height: int
    depth: int
    units: str


agent = Agent(
    "openai:gpt-4o-mini",
    output_type=[Box, str],
    instructions=(
        "Extract me the dimensions of a box, "
        "if you can't extract all data, ask the user to try again."
    ),
)

result = agent.run_sync("The box is 10x20x30")
print(result.output)

result = agent.run_sync("The box is 10x20x30 cm")
print(result.output)

# --------------------------------------------------------------
# Union of output types
# --------------------------------------------------------------

agent = Agent(
    "openai:gpt-4o-mini",
    output_type=list[str] | list[int],
    instructions="Extract either colors or sizes from the shapes provided.",
)

result = agent.run_sync("red square, blue circle, green triangle")
print(result.output)

result = agent.run_sync("square size 10, circle size 20, triangle size 30")
print(result.output)

# --------------------------------------------------------------
# Output functions - function as output_type
# --------------------------------------------------------------


def uppercase(ctx: RunContext[None], message: ModelResponse) -> str:
    """Uppercase the model's text response."""
    return message.text.upper()


agent = Agent(
    "openai:gpt-4o-mini",
    output_type=uppercase,
)

result = agent.run_sync("Tell me a quick joke")
print(result.output)
