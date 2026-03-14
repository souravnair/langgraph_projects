from langgraph.graph import StateGraph, START, END
from langchain_ollama import ChatOllama
from typing import TypedDict, Annotated
from pydantic import BaseModel, Field
import operator

model=ChatOllama(model='gemma3:latest')

class EvaluationSchema(BaseModel):
    feedback:str=Field(description="detailed feedback for the essay")
    score:int =Field(description="score out of 10", ge=0, le=10)

structured_model=model.with_structured_output(EvaluationSchema)

essay="""
Indian philosophy has long proclaimed, “Santosham param sukham” – contentment is the greatest happiness. The saying, “Contentment is natural wealth; luxury is artificial poverty,” beautifully captures this eternal wisdom. It implies that true prosperity lies not in possessing more, but in feeling fulfilled with what one has. Conversely, unending desires and the pursuit of luxury create a sense of inner emptiness – a kind of poverty masked by material abundance. In essence, while contentment springs from within and reflects harmony with oneself and nature, luxury often stems from external craving and comparison, leaving the individual spiritually impoverished despite material success. This profound thought, rooted deeply in Indian and global philosophical traditions, reminds us that real wealth lies in peace of mind and simplicity, not in the glitter of possessions. In today’s world of consumerism and competition, this idea holds timeless relevance, urging us to rediscover balance, gratitude, and the inner richness that material comfort alone can never provide. 
"""

# prompt=f"rate my essay: {essay}"
# print(prompt)
# response=structured_model.invoke(prompt)
# print(response)

#define State
class UPSCState(TypedDict):
    essay:str
    language_feedback: str
    analysis_feedback: str
    clarity_feedback:str
    overall_feedback: str
    individual_scores:Annotated[list[int], operator.add]
    avg_score: float
    
def evaluate_language(state:UPSCState):
    prompt=f"Evaluate the language quality of the given essay and provide a feedback and score for the same.\n Essay:{state["essay"]}"    
    response=structured_model.invoke(prompt)
    print("Evaluating language quality...")
    return {"language_feedback":response.feedback, "individual_scores":[response.score]}
def evaluate_analysis(state:UPSCState):
    prompt=f"Evaluate the depth of analysis of the given essay and provide a feedback and score for the same.\n Essay:{state["essay"]}"
    
    response=structured_model.invoke(prompt)
    print("Evaluating depth of analysis...")
    return {"analysis_feedback":response.feedback, "individual_scores":[response.score]}
def evaluate_thought(state:UPSCState):
    prompt=f"Evaluate the clarity of thought of the given essay and provide a feedback and score for the same.\n Essay:{state["essay"]}"
    
    response=structured_model.invoke(prompt)
    print("Evaluating clarity of thought...")
    return {"clarity_feedback":response.feedback, "individual_scores":[response.score]}
def final_evaluation(state:UPSCState) -> float:
    average_score=sum(state["individual_scores"])/len(state["individual_scores"])
    print("Final evaluation underway...")
    prompt=f"based on the feedbacks given below, create a final summary covering each feedback thoroughly.\n Feedbacks:\n language_feedback:{state["language_feedback"]}\n analysis_feedback: {state["analysis_feedback"]}\n clarity_feedback: {state["clarity_feedback"]}"
    final_summary=model.invoke(prompt).content
    return{"overall_feedback": final_summary, "avg_score": average_score}


graph=StateGraph(UPSCState)
graph.add_node("evaluate_language", evaluate_language)
graph.add_node("evaluate_analysis", evaluate_analysis)
graph.add_node("evaluate_thought", evaluate_thought)
graph.add_node("final_evaluation", final_evaluation)

#add edges(parallel)
graph.add_edge(START, "evaluate_language")
graph.add_edge(START, "evaluate_analysis")
graph.add_edge(START, "evaluate_thought")

#MERGE 3 parallels into a single node
graph.add_edge("evaluate_language","final_evaluation")
graph.add_edge("evaluate_analysis","final_evaluation")
graph.add_edge("evaluate_thought","final_evaluation")

graph.add_edge("final_evaluation", END)

workflow=graph.compile()

output=workflow.invoke({"essay":essay})
 
print(output)
