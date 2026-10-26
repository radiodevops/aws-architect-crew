import logging

from strands import Agent

# Show everything Strands sends to the model and gets back.
logging.getLogger("strands").setLevel(logging.DEBUG)
logging.basicConfig(
    format="%(levelname)s | %(name)s | %(message)s",
    handlers=[logging.StreamHandler()],
)

architect = Agent(
    system_prompt="""You are a senior AWS solutions architect.
You give practical, opinionated advice, you explain trade-offs briefly,
and you keep answers short enough to read in a minute.""",
)
architect(
    "I'm building a photo-sharing app for about 10,000 users. "
    "Which AWS services would you start with, and why?"
)