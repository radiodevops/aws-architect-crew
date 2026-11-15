from strands import Agent

# The same question as cost_agent.py, but the agent has no tools: it answers from memory.
agent = Agent(
    system_prompt="""You are an AWS cost analyst.
Show a short breakdown per service and a monthly total.""",
)

agent(
    "My API gets 5 million requests a month. Each Lambda call runs for 120 ms with 512 MB of memory. "
    "I also store 200 GB of photos in S3, with 1 million uploads and 10 million downloads a month. "
    "What will this cost per month? And how much would I save by moving the Lambda function to Arm?"
)
