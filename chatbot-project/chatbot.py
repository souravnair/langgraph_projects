from langgraph.graph import StateGraph, START, END 
from langgraph.graph.message import add_messages
from typing import TypedDict, Literal, Annotated
from pydantic import BaseModel, Field
from langchain_ollama import ChatOllama
from langchain_core.messages import BaseMessage, HumanMessage
from operator import add
from chat_node import chat_node

class ChatState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]

graph=StateGraph(ChatState)

graph.add_node("chat_node", chat_node)

graph.add_edge(START, "chat_node")
graph.add_edge("chat_node", END)

chat_workflow=graph.compile()

if __name__=="__main__":
    # init_state={
    #     "messages": [HumanMessage(content="what is the capital of india?")]
    # }
    # graph_response=chat_workflow.invoke(init_state)
    # final_response=graph_response["messages"][-1].content
    # print(final_response)
    while True:
        user_message=input("Type here: ")
        print("User Message", user_message)
        if user_message.strip().lower() in ["exit", "quit", "bye"]:
            break
        init_state={"messages": [HumanMessage(content=user_message)]}
        graph_response=chat_workflow.invoke(init_state)
        response_content=graph_response["messages"][-1].content
        print("AI Message: ", response_content)