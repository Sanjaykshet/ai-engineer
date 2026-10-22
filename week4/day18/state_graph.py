from typing import TypedDict
from langgraph.graph import StateGraph, START, END

class newState(TypedDict):
    number:int

def double(state:newState)->dict:
    num = state["number"]
    if num*2 <100:
        new_num = num*2
        print(num,"->",new_num)
        return {"number":new_num}
    return {"number":100}
    
def helper(s:newState):
    if s["number"] <100:
        return "double"
    elif s["number"] >= 100:
        return END
    
builder = StateGraph(newState) # initializes a state graph

builder.add_node("double",double) # add nodes to graph (node_name,function_name )
builder.add_edge(START,"double")

builder.add_conditional_edges(
    "double",
    helper,
    {"double":"double",END:END}) # edge form which node to which node ,decision making function

graph = builder.compile()

result = graph.invoke({"number":4})
print("final result:",result)