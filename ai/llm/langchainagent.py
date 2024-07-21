# import os
# from dotenv import load_dotenv
# from typing import Any, AsyncIterator, Dict, Iterator, List, Optional
# from ai.llm import tools, prompts
# from langchain import hub
# from langchain.agents import AgentExecutor, create_react_agent
# from langchain_openai import OpenAI, ChatOpenAI
# from langchain_core.prompts import ChatPromptTemplate
# from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
# from langchain_core.messages import (
#     AIMessage,
#     BaseMessage,
#     FunctionMessage,
#     HumanMessage,
#     SystemMessage,
#     ToolMessage,
# )

# # This is based on the ReAct pattern. ReAct: Synergizing Reasoning and Acting in Language Models
# # https://arxiv.org/abs/2210.03629

# load_dotenv()

# openai_api_key = os.getenv("OPEN_API_KEY")


# def get_llm_response(user_input: str):
#     # this could be additional prompts
#     prompt = prompts.superforecaster()
#     # this could be additional tools
#     tools = tools.TavilySearchResults()
#     llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
#     agent = create_react_agent(llm, tools, prompt)
#     agent_executor = AgentExecutor(agent=agent, tools=tools verbose=True)
#     result = agent_executor.invoke({"input": {user_input}})
#     return result


# # TODO: Add outputparser.JSON - send parsed message as JSON
