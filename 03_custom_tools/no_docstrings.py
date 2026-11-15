import json

from strands import tool

# Step 1: the Lambda calculator from cost_agent.py as a tool, but without a docstring.
# Run it to see what the model is told about a tool nobody described.
LAMBDA_PRICE_PER_MILLION_REQUESTS = 0.20
LAMBDA_PRICE_PER_GB_SECOND = {"x86_64": 0.0000166667, "arm64": 0.0000133334}


@tool
def estimate_lambda_cost(
    monthly_requests: int,
    avg_duration_ms: float,
    memory_mb: int,
    architecture: str = "x86_64",
) -> dict:
    if not 128 <= memory_mb <= 10240:
        raise ValueError("memory_mb must be between 128 and 10240")
    if architecture not in LAMBDA_PRICE_PER_GB_SECOND:
        raise ValueError('architecture must be "x86_64" or "arm64"')

    gb_seconds = monthly_requests * (avg_duration_ms / 1000) * (memory_mb / 1024)
    request_cost = monthly_requests / 1_000_000 * LAMBDA_PRICE_PER_MILLION_REQUESTS
    compute_cost = gb_seconds * LAMBDA_PRICE_PER_GB_SECOND[architecture]

    return {
        "gb_seconds": round(gb_seconds, 2),
        "request_cost_usd": round(request_cost, 2),
        "compute_cost_usd": round(compute_cost, 2),
        "total_usd": round(request_cost + compute_cost, 2),
    }


if __name__ == "__main__":
    print(json.dumps(estimate_lambda_cost.tool_spec, indent=2))
