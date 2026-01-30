# UV: The Fast Python Package Manager

UV is a Rust-based "Cargo for Python" that replaces pip, pip-tools, pipx, poetry, pyenv, and virtualenv with a single tool. Written by Astral (creators of Ruff), it delivers **10-100x performance improvements** - think TensorFlow installs in 25 seconds instead of 3 minutes.

**Installation:** [Download and install UV here](https://docs.astral.sh/uv/getting-started/installation/)

## Why developers are switching

- **Speed**: CI/CD pipelines drop from 25+ minutes to seconds
- **Simplicity**: No more juggling multiple tools or activating venvs
- **Modern**: Built-in Python version management and dependency groups
- **Compatible**: Works with existing pip/poetry workflows

But beyond all that, it makes working with Python much more enjoyable. I've been working with Python for over 10 years, and setting up a new project, managing dependencies, and getting everything to work has always been one of my least favorite parts of this programming language. UV solves all of that. This guide will cover the basics that everyone needs to know. You can find the [official documentation here](https://docs.astral.sh/uv/getting-started/) to learn more about specific use cases.

## About Astral and Ruff

UV comes from [Astral](https://astral.sh/), the same team behind [Ruff](https://docs.astral.sh/ruff/) - the extremely fast Python linter and formatter that I highly recommend to everyone. Like UV, Ruff is written in Rust and delivers massive performance improvements (100x faster than flake8). If you're not using Ruff yet, you should be - it replaces flake8, isort, black, and more with a single blazingly fast tool.

## Most common real-world workflows

## Starting a new Python project

Create a new project:

```bash
uv init my-ai-app
cd my-ai-app
```

Project structure:

```
my-web-app/
├── .gitignore
├── .python-version    # Pins Python version
├── README.md
├── hello.py
└── pyproject.toml     # Modern Python packaging
```

Add dependencies and run:

```bash
uv add openai fastapi
uv run hello.py
```

UV automatically creates the venv, installs dependencies, and generates `uv.lock` for reproducible builds.

## Working with existing projects

Clone and sync:

```bash
git clone https://github.com/org/project.git
cd project
uv sync
```

`uv sync` creates the venv and installs exact versions from `uv.lock` for identical team setups.

Production deployments (exclude dev dependencies):

```bash
uv sync --no-dev
```

## Python version management

Built-in Python version management (replaces pyenv):

```bash
# Install Python versions
uv python install 3.12
uv python install 3.11 3.12 3.13  # Multiple at once

# Pin project to specific version
uv python pin 3.12  # Creates .python-version

# List available versions
uv python list
```

**Automatic Python installation**: UV installs missing Python versions during `uv sync`.

## Development vs production dependencies

UV uses modern dependency groups following PEP 735:

```toml
[project]
name = "my-app"
dependencies = [
    "fastapi>=0.100.0",
    "sqlalchemy>=2.0.0",
]

[dependency-groups]
dev = [
    "pytest>=7.4.0",
    "black>=23.0.0",
]
```

Managing dependency groups:

```bash
uv add --dev pytest black        # Add to dev group
uv sync                          # Install everything
uv sync --no-dev                 # Production only
```

## Essential commands

Most common UV commands:

```bash
# Project setup
uv init myproject           # Create new project
uv add requests             # Add dependency
uv remove requests             # Remove dependency
uv sync                     # Install from lockfile

# Running code
uv run script.py    # Run in project environment
uv run pytest              # Run tests

# Python management
uv python install 3.12     # Install Python version
uv python pin 3.12         # Set project Python

# Tool usage
uvx black .                # Run tool temporarily
uv tool install ruff       # Install tool globally

# Package management (pip-compatible)
uv pip install requests  # Direct pip replacement
uv pip install -r requirements.txt
```

## New project flow

```bash
uv init my-project
cd my-project
cursor .

uv add openai python-dotenv fastapi
uv add --dev ipykernel
echo "API_KEY=your-key" > .env

git init
git add .
git commit -m "Initial commit"

# Create new repo with GitHub CLI
gh repo create my-project --private --source=. --remote=origin --push
```