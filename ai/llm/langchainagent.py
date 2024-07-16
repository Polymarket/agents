import os
from dotenv import load_dotenv
from langchain.agents import create_openai_functions_agent
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_openai.chat_models import ChatOpenAI

load_dotenv()

openai_api_key = os.getenv("OPEN_API_KEY")
tavily_api_key = os.getenv("TAVILY_API_KEY")

os.environ["OPENAI_API_KEY"] = openai_api_key
os.environ["TAVILY_API_KEY"] = tavily_api_key

llm = OpenAI(temperature=0)

tools = load_tools([""])

# what is a tool like this
name = tools.name
description = tools.description

agent = initialize_agents(tools, llm, agent="zero-shot-react-description", verbose=True)

agent.agent.llm_chain.prompt.template

agent.run(
    "What is the probability that Biden drops out of the US presidential election?"
)


## Helper Utilities ##
# Functions to make it easier to add new agent nodes #
 def create_agent(llm: ChatOpenAI, tools: list, system_prompt: str):
    # Each worker node will be given a name and some tools
    prompt = ChatPromptTemplate.from_messages(
        [(
            "system", 
            system_prompt,
          ),
          MessagesPlaceholder(variable_name="messages"),
          MesssagesPlaceholder(variable_name="agent_scratchpad"),
          ]
    )
    agent = create_openai_tools_agent(llm, tools, prompt)
    executor = AgentExecutor(agent=agent, tools=tools)

## CONSTRUCT GRAPH #

# the agent state is the input to each node in the graph
class AgentState(TypedDict):
    # the annotation tells the graph that new messages will always
    # be added to the current states
    messages: Annotated[Sequence[BaseMessage], operator.add]
    next: str
    # tool it should call or final result that it should pass
    agent_outcome: Union[AgentAction, AgentFinish, None]

## INVOKE ##
# with graph created, we can now invoke it and see how it performs #