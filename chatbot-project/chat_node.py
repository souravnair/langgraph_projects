from langchain_ollama import ChatOllama
from langchain_core.messages import BaseMessage
from states import ChatState
from prompts import CHAT_SYSTEM_PROMPT

def chat_node(state:ChatState) -> list[BaseMessage]:
    model=ChatOllama(model="gemma3:latest")
    messages=state["messages"]
    response=model.invoke(messages)
    return {"messages":[response]}

