import os
from dotenv import load_dotenv
from langchain.agents import load_tools
from langchain.agents import initialize_agent
from langchain_openai import OpenAI

load_dotenv()

openai_api_key = os.getenv("OPEN_API_KEY")
tavily_api_key = os.getenv("TAVILY_API_KEY")

os.environ["OPENAI_API_KEY"] = openai_api_key
os.environ["TAVILY_API_KEY"] = tavily_api_key

tools = load_tools(["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", "llm-math"], llm=llm)

agent = initialize_agent(
    tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True
)

agent.run(
    "Who is most likely to be the Republican VP nominee for the upcoming 2024 US Presidential Election?"
)
