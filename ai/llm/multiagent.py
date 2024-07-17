import os
import json
from dotenv import load_dotenv
from langchain_openai import OpenAI
from langchain_core.messages import AIMessage, BaseMessage, ChatMessage, FunctionMessage, HumanMessage
from langgraph.graph import END, StateGraph
from langgraph.prebuilt.tool_executor import ToolExecutor, ToolInvocation

from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.agents import create_openai_functions_agent, AgentExecutor
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_openai.chat_models import ChatOpenAI

load_dotenv()

openai_api_key = os.getenv("OPEN_API_KEY")
tavily_api_key = os.getenv("TAVILY_API_KEY")
langchain_api_key=

# CREATE AGENT #
# helper functions will create agents #
def create_agent(llm, tools, system_message: str):
 """ Create an agent """
 functions = [format_tool_to_openai_function(t) for t in tools]

 prompt = ChatPromptTemplate.from_messages(
    [
       (
          "system",
          "You are a helpful AI assistant, collaborating with other assistants"
       ),
       MessagesPlaceholder(variable_name="messages"),
    ]
 )
 prompt = prompt.partial(system_message=system_message)
 prompt = prompt.partial(tool_names=" , ".join([tool.name for tool in tools]))
 return prompt | llm.bind_functions(functions)

llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)

# Research agent and node
research_agent = create_agent(llm,
                              [tavily_tool],
                              system_message="You should provide accurate data for the pricing agent")
research_node = functools.partial()

# chart generator
chart_agent = create_agent(
 llm,
 [python_repl]
)

# Define Tool Node #
tools = [tavily_tool, python_repl]
def tool_node(state):
 """" This runs tools in the graph
 
It takes in an agent action and calls that tool and returns the result."""
messages = state["messages"]
# Based on the continue condition


# INVOKE ##
with graph created, we can now invoke it and see how it performs #
