
# langgraph with conditional edge

# A conditional edge dynamically selects the next node based upon current state

# start -> analyze(Node1) -> conditional edge -> revision(Node2) or success(Node3) -> end

# Libraries
import streamlit as st
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END

# State
class StudentState(TypedDict):
    marks: int
    feedback: str

# Node 1 (analyze)
def analyze(state):
    print("Analyzing marks")
    return {}

# Node 2 (revision)
def revision(state):
    return {"feedback": "Please revise the concepts"}

# Node 3 (success)
def success(state):
    return {"feedback": "Congratulations"}

# Routing function for conditional edge
def decide(state):
    if state['marks'] >= 36:
        return "pass"
    else:
        return "fail"

# Create the graph
graph = StateGraph(StudentState)

graph.add_node("analyze", analyze)
graph.add_node("revision", revision)
graph.add_node("success", success)

graph.add_edge(START, "analyze")

graph.add_conditional_edges(
    "analyze",
    decide,
    {
        "pass": "success",
        "fail": "revision"
    }
)

graph.add_edge("success", END)
graph.add_edge("revision", END)

app = graph.compile()

# Streamlit UI
st.title("Conditional Edge in LangGraph")
marks = st.number_input("Marks", min_value=0, max_value=100, value=0)

if st.button("CHECK"):
    result = app.invoke({
        "marks": int(marks),
        "feedback": ""
    })
    st.info(result["feedback"])
