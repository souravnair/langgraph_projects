from langgraph.graph import StateGraph, MessagesState, START, END
from langchain.chat_models import init_chat_model
from langchain_core.messages import AIMessage
from pydantic import BaseModel

class StructureResponse(BaseModel):
    message: str
    score: int

def mock_llm(state: MessagesState):
    model=init_chat_model(
        "ollama:gemma3:latest"
    )
    structured_model=model.with_structured_output(StructureResponse)
    print(state["messages"])
    # for token in model.stream(state["messages"]):
    #     print(token.text, end="")
    response=structured_model.invoke("hi. please rate my english out of 10")
    print(type(response))
    ai_msg=AIMessage(content=f"{response.message} '\n' 'score: {response.score}", additional_kwargs={"structured_data":response.model_dump()})
    # print("Response==",response, "\n", type(response))
    # print(state["messages"])    
    return {"messages": ai_msg}

graph=StateGraph(MessagesState)
graph.add_node(mock_llm)
graph.add_edge(START, "mock_llm")
graph.add_edge("mock_llm", END)
mock_workflow=graph.compile()
response=mock_workflow.invoke({"messages":[{"role":"user", "content":"hello"}]})
print(response)
print(response["messages"][-1].content)

