from strands import Agent
from strands.vended_tools import web_fetch

docs_agent = Agent(
    tools=[web_fetch],
    system_prompt="""You are an AWS expert who answers from the official documentation, not from memory.
For AWS Lambda limits and quotas, read this page:
https://docs.aws.amazon.com/lambda/latest/dg/gettingstarted-limits.html
Quote the numbers you find and say which page they came from.""",
)

docs_agent("What are the maximum timeout and the maximum memory for a Lambda function?")
