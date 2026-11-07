from strands import Agent
from strands.vended_interventions.hitl import HumanInTheLoop
from strands.vended_tools import shell

inspector = Agent(
    tools=[shell],
    # Every tool call stops and asks for your approval in the terminal.
    interventions=[HumanInTheLoop(ask="stdio")],
    system_prompt="""You inspect an AWS account with the AWS CLI.
Only run read-only commands: sts get-caller-identity, and describe, list or get commands.
Never create, change or delete anything. Add --output json and keep each command small.""",
)

inspector(
    "Give me a quick overview of this AWS account: who am I, which region am I using, "
    "and how many S3 buckets and Lambda functions are there?"
)
