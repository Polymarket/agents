import getpass
import os
from langchain import hub
from langchain.agents import AgentExecutor, create_openai_functions_agent
from langchain_openai import ChatOpenAI
from langchain_community.tools.tavily_search import TavilySearchResults

os.environ["TAVILY_API_KEY"] = "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"
os.environ["OPENAI_API_KEY"] = (
    "sk-proj-BbAO2Flvd5STq4UMuvQLT3BlbkFJhshpJAztZbDHVznU1p9T"
)

instructions = """You are an assistant."""
base_prompt = hub.pull("langchain-ai/openai-functions-template")
prompt = base_prompt.partial(instructions=instructions)
llm = ChatOpenAI(temperature=0)
tavily_tool = TavilySearchResults()
tools = [tavily_tool]
agent = create_openai_functions_agent(llm, tools, prompt)
agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True,
)

agent_executor.invoke({"query": "What happened in the latest burning man floods"})
