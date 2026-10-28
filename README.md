# AWS Architect Crew

A team of AI agents that review AWS architectures, built step by step with [Strands Agents](https://strandsagents.com) on Amazon Bedrock.

This is the code for the YouTube series on the Radio DevOps channel. Each episode adds one piece, and each episode's state is tagged (`ep01`, `ep02`, …), so you can check out the code exactly as it was in the video.

## Episodes

| # | Episode | Folder | Tag |
|---|---|---|---|
| 1 | Your first agent | `01_first_agent` | `ep01` |
| 2 | Built-in tools | coming soon | |
| 3 | Your own tools | coming soon | |
| 4 | MCP server | coming soon | |
| 5 | RAG | coming soon | |
| 6 | Multi-agent with A2A | coming soon | |
| 7 | Strands harness | coming soon | |

## What you need

- Python 3.13 and [uv](https://docs.astral.sh/uv/)
- An AWS account with credentials set up locally (`aws configure`, environment variables, or an SSO profile)
- Access to Claude Sonnet 4.6 in Amazon Bedrock. Strands uses it by default, through a global inference profile.

## Run Episode 1

```bash
git clone https://github.com/<you>/aws-architect-crew.git
cd aws-architect-crew
git checkout ep01        # the code as it was in Episode 1

uv sync
source .venv/bin/activate   # Windows: .venv\Scripts\activate

python -u 01_first_agent/architect.py
```

`-u` turns off output buffering, so the agent's answer and the DEBUG log lines print in the order they happen.

The DEBUG output shows the full request Strands sends to Bedrock (system prompt, your question, model ID) and the response that comes back. It also prints a few local paths, so check it before you share it.

## Every new terminal

Activate the environment again in each new terminal (`source .venv/bin/activate`). From Episode 4 on, you'll have a few terminals running at once.
