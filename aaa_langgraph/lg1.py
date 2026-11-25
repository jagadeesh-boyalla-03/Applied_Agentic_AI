# Multiple nodes in Langgraph

# Node-1 : Calculate the student result
# Node-2 : Generate feedback

# Start -> Analyze(Node1) -> Feedback(Node2) -> END

# Libraries
import streamlit as st
from typing_extensions import TypedDict  # define structure of state
from langgraph.graph import StateGraph, START, END

# State : information to store
class StudentState(TypedDict):
    name : str
    marks : int
    result : str
    feedback : str

# Node1 -> Analyze if pass or fail based upon marks
def analyze_marks(state : StudentState):
    if state["marks"] >= 36 :
        res = "Pass"
    else:
        res = "Fail"

    return {"result" : res }

# Node-2 : Feedback
def generate_feedback(state):
    if state["result"] == "Pass":
        salahar = "Congratulation, Still keep updating"
    else:
        salahar = "Nuvk malli try chei"

    return {"feedback" :salahar}

# create the graph
# Start -> Analyze(Node1) -> Feedback(Node2) -> END
graph = StateGraph(StudentState)

graph.add_node("analyze", analyze_marks)
graph.add_node("feedback", generate_feedback)

graph.add_edge(START, "analyze")
graph.add_edge("analyze", "feedback" )
graph.add_edge("feedback", END)

app = graph.compile()

st.title("Multinode langgraph student application")

name = st.text_input("Enter Student Name")
marks = st.number_input("Marks", min_value = 0, max_value = 100, value = 0)

if st.button("CHECK FEEDBACK") and name and marks:
    result = app.invoke({"name" : name, "marks" : int(marks), "result" : "", "feedback" : ""})
    st.write(f"{result["name"]} - {result["result"]}")
    st.info(result["feedback"])