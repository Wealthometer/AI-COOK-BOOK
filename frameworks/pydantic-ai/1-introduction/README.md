# Introduction

If you have shipped real LLM features before, you have probably wrestled with brittle JSON, unclear tool boundaries, and poor visibility into what the model actually did. Pydantic AI approaches these problems with the same philosophy that made Pydantic and FastAPI so useful in production: strong types, minimal magic, clear interfaces, and first class observability.

## What is Pydantic AI

Pydantic AI is a **type-safe agent framework for Python** built around three core ideas:

1. **Structured outputs** — use Pydantic models to define exactly what your model should return and automatically validate it.
2. **Composable tools** — integrate external capabilities through the emerging **Model Context Protocol (MCP)** so that agents can safely connect to tools, APIs, or other agents.
3. **Full observability** — every prompt, token, and tool call can be traced using OpenTelemetry.

At its core, Pydantic AI brings the same reliability and developer experience of Pydantic and FastAPI into AI development. You get the confidence of type checking, the simplicity of declarative models, and the power of dynamic tool calling — all while staying compatible with any model provider such as OpenAI, Anthropic, or Google Gemini.

## Why Use It

If you have ever built an LLM application, you know that most frameworks promise flexibility but introduce hidden complexity. Pydantic AI takes a different path. It does not try to be the “everything” framework. It gives you the **right primitives** to build structured, maintainable, and observable AI systems.

- **Type safety from end to end.** Your models, tools, and dependencies are validated at runtime and at development time.
- **Reduced fragility.** Automatic retries on validation errors mean your agent can self-correct without you writing endless if-else logic.
- **Protocol-level interoperability.** MCP allows your agents to interact with any compliant tool — browser automation, databases, Python sandboxes — without being hardwired to a single SDK.
- **Transparency and traceability.** Built-in observability lets you see what your model did, how long it took, and how much it cost.

In short, Pydantic AI helps you go from “prompt engineering” to **real software engineering** for AI.

## How It’s Different from Other Frameworks

Most agentic frameworks abstract too much. They wrap everything in custom orchestration layers, invent new DSLs, or hide execution flow behind decorators and graphs. This works for demos, but it often breaks when you start shipping production code.

Pydantic AI is **minimal, explicit, and type-driven**. It does not replace Python — it extends it. You stay in control of your functions, your dependencies, and your data contracts. It focuses on correctness and composition rather than on prebuilt chains or black-box memory systems.

Another key difference is its **native support for MCP**. Instead of inventing its own plugin system, it aligns with the open standard that tools like Cursor, Windsurf, and Claude Desktop already use. This means the agents you build today can interoperate with a growing ecosystem of tools tomorrow.

Finally, Pydantic AI is **observability-first**. Every agent run emits structured traces that integrate seamlessly with any OpenTelemetry backend. That means you can actually debug, test, and measure your AI systems just like any other piece of software.

## How Datalumina Uses Pydantic AI

At [Datalumina](https://www.datalumina.com/), our AI development agency, we build and deploy production-grade AI systems for clients across industries. We use **parts of Pydantic AI**, not the entire stack, because it fits perfectly into our modular approach to building AI applications.

We rely heavily on:

- **Structured outputs and validation** to guarantee that our model responses conform to strict schemas before entering business logic.  
- **Easy provider and model switching** to test and compare performance across OpenAI, Anthropic, Google, and other APIs with a single configuration change.  
- **Tracing and evaluation** through Langfuse and OpenTelemetry to monitor model behavior, latency, and token usage in production.

However, for orchestration and workflow logic, we use our own internal framework — the [GenAI Launchpad](https://academy.datalumina.com/launchpad) — which provides declarative, FastAPI-based pipelines and background task execution (Celery, Postgres, vector DB, etc.). Pydantic AI plugs neatly into this setup as the engine for structured reasoning and tool invocation.

In short, we use Pydantic AI where it adds clarity, safety, and visibility — and we replace abstraction with our own composable systems where we need flexibility. It’s a perfect balance between using great open-source foundations and keeping full control of how our AI systems run in production.