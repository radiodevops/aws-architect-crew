# Episode 3: Writing your own tools

Video: [VIDEO LINK]

Two cost calculator tools, one for AWS Lambda and one for S3, and an agent that uses them. The model decides what to calculate; Python does the arithmetic.

## Run it

Three files, in the order the video uses them:

```bash
python -u 03_custom_tools/no_tools.py        # the question without tools: the model answers from memory
python -u 03_custom_tools/no_docstrings.py   # a tool nobody described: what the model is told
python -u 03_custom_tools/cost_agent.py      # the real thing: tool spec, then the agent with both tools
```

`cost_agent.py` first prints `estimate_lambda_cost.tool_spec`, which is everything the model is told about the tool. Compare it with the one from `no_docstrings.py`. Then the agent answers the cost question in the file.

Expected numbers for that question:

| Item | Monthly cost |
|---|---|
| Lambda, x86 (5M requests, 120 ms, 512 MB) | $6.00 |
| Lambda, Arm | $5.00 |
| S3 Standard (200 GB, 1M uploads, 10M downloads) | $13.60 |
| Total on x86 | $19.60 |

## What's in the code

| Part | What it does |
|---|---|
| `@tool` | Turns a Python function into a tool the agent can call. |
| The docstring | Becomes the tool's description, and the `Args:` section describes each parameter. The model never sees the function body, only the name, docstring and types. |
| `tools=[estimate_lambda_cost, estimate_s3_cost]` | The agent can only use tools listed here. |

Without a docstring (`no_docstrings.py`) the description is just the function name and every parameter is "Parameter <name>". With one, the summary becomes the description and each `Args:` line becomes its parameter's description.

## Prices used

us-east-1 on-demand list prices, checked November 2026, free tier not included:

| Service | Price |
|---|---|
| Lambda requests | $0.20 per 1M |
| Lambda compute, x86 | $0.0000166667 per GB-second |
| Lambda compute, Arm | $0.0000133334 per GB-second |
| S3 Standard storage | $0.023 per GB-month |
| S3 PUT, COPY, POST, LIST | $0.005 per 1,000 |
| S3 GET | $0.0004 per 1,000 |

Check the [Lambda](https://aws.amazon.com/lambda/pricing/) and [S3](https://aws.amazon.com/s3/pricing/) pricing pages before relying on these.

Previous: [Episode 2](../02_built_in_tools/) · Next: [Episode 4, sharing tools with MCP](../04_mcp/)
