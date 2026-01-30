## How to Automate Anything with Python Inside Claude Desktop (Using MCP)

This tutorial shows how to build a minimal Model Context Protocol (MCP) server in Python, manage and run it with `uv`, and connect it to Claude Desktop or Claude Code. We’ll use a practical example: fetch the transcript of any YouTube video on demand so you can summarize it and decide whether it’s worth watching.

Why MCP? It’s perfect for developer-side automations you want to trigger immediately from your IDE or desktop assistant—no deployments or UIs required. Great for personal workflows; not aimed at production apps.

### Prerequisites

- Python 3.12+
- uv (see [https://docs.astral.sh/uv/](https://docs.astral.sh/uv/getting-started/installation/))
- Claude Desktop or Claude Code

Replace any absolute paths below with your own, for example: `<ABSOLUTE_PATH_TO_THIS_DIR>`.

### Project layout

```
mcp/servers/youtube/
  server.py              # MCP entrypoint with tools
  src/
    __init__.py
    service.py           # YouTubeTranscriptService wrapper
    utils.py             # helpers (extract_video_id)
  pyproject.toml         # deps for this server when using uv
  README.md              # this guide
```

---

### Step: 1 Add a uv script header to simplify running

At the very top of `server.py`, add the script metadata so `uv run server.py` resolves everything automatically:

```
# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "mcp[cli]>=1.12.3",
#     "pydantic>=2.11.7",
#     "python-dotenv>=1.1.1",
#     "requests>=2.32.4",
#     "youtube-transcript-api>=1.2.2",
# ]
# ///
```

This lets `uv` create an isolated environment and install only what this script needs.


### Step 2: Create your server

Create your `server.py`, implement any logic and register your tools. Use `stdio` for easy local servers without needing deployment.


### Step 3: Run the dev server locally

From this directory:

```
mcp dev server.py
```

Test the server with the MCP Inspector tool. Connect > Tools > List Tools > get_transcript > Insert URL > Run Tool.


### Step 4: Proxy support (Optional)

The transcript service supports [Webshare](https://www.webshare.io/) proxies if you set these environment variables (otherwise it uses a direct connection):

```
WEBSHARE_USERNAME=<your_username>
WEBSHARE_PASSWORD=<your_password>
```


### Step 5: Connect from Claude Desktop

Go to Claude Desktop > Settings > Developer > Edit Config > Edit §claude_desktop_config.json` and add:

```
{
  "mcpServers": {
    "YouTube": {
      "command": "uv",
      "args": [
        "--directory",
        "<ABSOLUTE_PATH_TO_THIS_DIR>",
        "run",
        "server.py"
      ]
    }
  }
}
```

Restart Claude Desktop. You should see tools like `get_transcript` available.

### Step 6: Connect from Claude Code (CLI)

From anywhere:

```
claude mcp add --transport stdio YouTube -- \
  uv --directory "<ABSOLUTE_PATH_TO_THIS_DIR>" run server.py
```

Then list tools:

```
claude mcp tools YouTube
```

## Typical workflow (why this is useful)

1) A new video drops and you don’t have time to watch it.
2) In Claude Desktop or Code, call `get_transcript` with the URL.
3) Paste the transcript to your model for a quick summary.
4) Decide if it’s worth a full watch—all without opening a browser tab.

This pattern generalizes to countless “small but effective” dev automations.