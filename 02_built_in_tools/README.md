# Episode 2: Giving agents tools, safely

Video: [VIDEO LINK]

Two agents that use tools built into Strands. One reads the AWS documentation before it answers. The other runs AWS CLI commands against your account, and every command waits for your approval first.

## Before you start

- The setup from [episode 1](../01_first_agent/)
- For `account_inspector.py`: the [AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html), configured for the same account
- Windows: run `account_inspector.py` inside WSL. The `shell` tool runs commands through `sh`.

## Run it

```bash
python -u 02_built_in_tools/docs_agent.py
python -u 02_built_in_tools/account_inspector.py
```

`docs_agent.py` calls `web_fetch` on the Lambda quotas page and answers with the numbers it found there.

`account_inspector.py` stops before every command and asks:

```
Approve "shell"?
  Input: {"command": "aws sts get-caller-identity --output json"} (y/n):
```

Type `y` to run it or `n` to refuse. When you refuse, the agent is told and has to work around it.

## What's in the code

| Part | What it does |
|---|---|
| `web_fetch` | Fetches a page and answers a question about it with a separate model call, so the whole page never lands in the agent's context. |
| `shell` | Runs a shell command and returns its output. It can run anything, so it's paired with an approval step. |
| `HumanInTheLoop(ask="stdio")` | An intervention that pauses every tool call and asks you in the terminal. |

The system prompt asks for read-only commands, but a prompt is a request. The approval step is what actually stops a command.

To let some tools run without asking, pass them in `allowed_tools`:

```python
HumanInTheLoop(ask="stdio", allowed_tools=["web_fetch"])
```

`allowed_tools=["*"]` turns the prompts off completely. Only do that on a sandbox account.

Previous: [Episode 1](../01_first_agent/) · Next: [Episode 3, writing your own tools](../03_custom_tools/)
