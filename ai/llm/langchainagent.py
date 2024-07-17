import os
from dotenv import load_dotenv
from langchain_openai import OpenAI
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.agents import create_openai_functions_agent, AgentExecutor
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_openai.chat_models import ChatOpenAI

load_dotenv()

openai_api_key = os.getenv("OPEN_API_KEY")
tavily_api_key = os.getenv("TAVILY_API_KEY")

llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are an assistant called Max"),
        ("human", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ]
)


def get_llm_response(user_input: str) -> str:
    system_message = SystemMessage(content=str(prompts.market_analyst))
    human_message = HumanMessage(content=user_input)
    messages = [system_message, human_message]
    result = llm.invoke(messages)
    return result.content


# Initialize the tool with your API key
search = TavilySearchResults(tavily_api_key=tavily_api_key)

tools = [search]

agent = create_openai_functions_agent(llm=llm, prompt=prompt, tools=tools)

agentExecutor = AgentExecutor(agent=agent, tools=tools)

response = agentExecutor.invoke({"input": "Hello"})

print(response)
