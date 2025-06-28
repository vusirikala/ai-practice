## Run `langgraph dev` to run and debug this file in langsmith online interface.
import os
import dotenv
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import create_react_agent
from typing import Annotated, TypedDict
from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages

dotenv.load_dotenv()
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
os.environ["LANGSMITH_API_KEY"] = os.getenv("LANGSMITH_API_KEY")
os.environ["LANGSMITH_PROJECT"] = "langgraph-project"
os.environ["LANGSMITH_ENDPOINT"] = "https://api.smith.langchain.com"


llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)

class State(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]

def make_default_graph():
    graph_workflow = StateGraph(State)
    def call_model(state):
        return {"messages": llm.invoke(state["messages"])}
    
    graph_workflow.add_node("agent", call_model)
    graph_workflow.add_edge(START, "agent")
    graph_workflow.add_edge("agent", END)

    agent = graph_workflow.compile()
    return agent

agent = make_default_graph()






