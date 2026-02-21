from langgraph.graph import StateGraph,START,END
from typing import TypedDict,Literal
from pydantic import BaseModel,Field
from langchain_ollama import ChatOllama

class SentimentState(BaseModel):
    sentiment:Literal["positive","negative"]=Field(description="Sentiment of the Review")

sentiment_model=ChatOllama(model="gemma3:latest")
structured_sentiment_model=sentiment_model.with_structured_output(schema=SentimentState)

# response=structured_sentiment_model.invoke(input="This is a very good item")
# print(response)

class ReviewState(TypedDict):
    review:str
    sentiment:SentimentState
    diagnosis: dict
    response: str


def provide_review_sentiment(state:ReviewState) -> ReviewState:
    prompt=f"Based on the review given below, identify it is a positive or negative review: {state["review"]}"
    response=structured_sentiment_model.invoke(input=prompt)
    return{"sentiment":response}

def handle_review(state:ReviewState)->Literal["positive_response","negative_response"]:
    if(state["sentiment"].sentiment=="positive"):
        return "positive_response"
    return "negative_response"

def positive_response(state:ReviewState)->str:
    prompt=f"You're a customer service agent. Your job is to respond back to ther user with an appropriate response for the given user review.The user has provided the below feedback:\n {state["review"]}.\nThe sentiment is: {state["sentiment"].sentiment}.\n Based on the review, provide a response/thank you note to the user.Do not give any suugestions about how to handle the review, you andle it yourself and respond to the user accordingly."
    response=sentiment_model.invoke(prompt)
    return {"response":response.content}

def negative_response(state:ReviewState)->str:
    prompt=f"You're a customer service agent who responds to the user directly. Your job is to respond back to ther user with an appropriate response for the given user review. The user has provided the below feedback:\n {state["review"]}.\nThe sentiment is: {state["sentiment"].sentiment}.\n Based on the review, provide an apology to the user and make sure you'll work on the issue. Do not give any suugestions about how to handle the review, you andle it yourself and respond to the user accordingly."
    response=sentiment_model.invoke(prompt)
    return {"response":response.content}

graph=StateGraph(ReviewState)

graph.add_node("provide_review_sentiment",provide_review_sentiment)
graph.add_node("negative_response", negative_response)
graph.add_node("positive_response",positive_response)

graph.add_edge(START, "provide_review_sentiment")

graph.add_conditional_edges("provide_review_sentiment",handle_review)

graph.add_edge("positive_response", END)
graph.add_edge("negative_response", END)

workflow=graph.compile()

if __name__=="__main__":
    user_response=input("Provide Response: ")
    init_state={"review": user_response}
    graph_response=workflow.invoke(input=init_state)
    print(graph_response["response"])