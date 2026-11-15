import json

from strands import Agent, tool

# us-east-1 on-demand prices, checked November 2026. Free tier not included.
LAMBDA_PRICE_PER_MILLION_REQUESTS = 0.20
LAMBDA_PRICE_PER_GB_SECOND = {"x86_64": 0.0000166667, "arm64": 0.0000133334}
S3_STANDARD_PRICE_PER_GB_MONTH = 0.023
S3_PRICE_PER_1000_PUT = 0.005
S3_PRICE_PER_1000_GET = 0.0004


@tool
def estimate_lambda_cost(
    monthly_requests: int,
    avg_duration_ms: float,
    memory_mb: int,
    architecture: str = "x86_64",
) -> dict:
    """Estimate the monthly cost of one AWS Lambda function in us-east-1.

    Use it whenever someone asks what a Lambda function will cost. Do not do
    this math yourself: call the tool once per function and use its numbers.
    Prices are on-demand list prices, without the free tier.

    Args:
        monthly_requests: How many times the function runs per month, e.g. 5000000.
        avg_duration_ms: Average run time of one invocation in milliseconds, e.g. 120.
        memory_mb: Memory configured for the function, between 128 and 10240.
        architecture: "x86_64" or "arm64". Arm is about 20% cheaper per GB-second.

    Returns:
        A dict with request_cost_usd, compute_cost_usd, total_usd and gb_seconds.
    """
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


@tool
def estimate_s3_cost(storage_gb: float, monthly_put_requests: int, monthly_get_requests: int) -> dict:
    """Estimate the monthly cost of an S3 Standard bucket in us-east-1.

    Use it whenever someone asks what S3 storage will cost. Covers storage and
    requests only; data transfer out to the internet is not included.

    Args:
        storage_gb: Average amount of data stored during the month, in GB.
        monthly_put_requests: Uploads per month (PUT, COPY, POST and LIST requests).
        monthly_get_requests: Downloads per month (GET requests).

    Returns:
        A dict with storage_cost_usd, request_cost_usd and total_usd.
    """
    storage_cost = storage_gb * S3_STANDARD_PRICE_PER_GB_MONTH
    request_cost = (
        monthly_put_requests / 1000 * S3_PRICE_PER_1000_PUT
        + monthly_get_requests / 1000 * S3_PRICE_PER_1000_GET
    )

    return {
        "storage_cost_usd": round(storage_cost, 2),
        "request_cost_usd": round(request_cost, 2),
        "total_usd": round(storage_cost + request_cost, 2),
    }


if __name__ == "__main__":
    print(json.dumps(estimate_lambda_cost.tool_spec, indent=2))  # exactly what the model is told about the tool

    cost_agent = Agent(
        tools=[estimate_lambda_cost, estimate_s3_cost],
        system_prompt="""You are an AWS cost analyst.
Always use your tools for prices and arithmetic, never estimate numbers yourself.
Show a short breakdown per service and a monthly total.""",
    )

    cost_agent(
        "My API gets 5 million requests a month. Each Lambda call runs for 120 ms with 512 MB of memory. "
        "I also store 200 GB of photos in S3, with 1 million uploads and 10 million downloads a month. "
        "What will this cost per month? And how much would I save by moving the Lambda function to Arm?"
    )
