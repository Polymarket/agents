import os
from dotenv import load_dotenv
from langchain.agents import load_tools
from langchain.agents import initialize_agent
from langchain_openai import OpenAI

# from langchain_openai import ChatOpenAI
# from langchain_community.tools.tavily_search import TavilySearchResults
# from langchain_core.messages import HumanMessage
# from langgraph.checkpoint.sqlite import SqliteSaver
# from langgraph.prebuilt import create_react_agent

# Create the agent
# memory = SqliteSaver.from_conn_string(":memory:")
# model = ChatOpenAI(model_name="gpt-4")
# search = TavilySearchResults(max_results=2)
# tools = [search]
# agent_executor = create_react_agent(model, tools, checkpointer=memory)

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
