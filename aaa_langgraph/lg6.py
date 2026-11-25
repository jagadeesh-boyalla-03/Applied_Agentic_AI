# MultiAgent + conditional loop + Human in the loop => Langgraph

# AI student assistant : 

"""
Workflow:
START -> Questions_agent -> collect answer -> Perfomance_agent -> Human_review -> Another attempt or placement -> final verdict -> END
"""

# Libraries
import os
from dotenv import load_dotenv

from langchain_groq import ChatGroq

import streamlit as st
from typing_extensions import TypedDict  # define structure of state
from langgraph.graph import StateGraph, START, END

import sqlite3
from langgraph.checkpoint.sqlite import SqliteSaver
from pydantic import BaseModel  # define the MCQ question format
from typing import Literal  # restrict a value to options: A,B,C,D
from langgraph.types import interrupt, Command  # interrupt : Pause, command : Resume

# load the api key
load_dotenv()

# initialize LLM
llm = ChatGroq(
    model = "openai/gpt-oss-20b",
    api_key = os.getenv("GROQ_API_KEY"),
    temperature = 0.7
)

# MCQ structure with pydentic
# format of the data LLM need to generate
class MCQ(BaseModel):
    question : str
    A : str
    B : str
    C : str
    D : str
    correct_answer :  Literal["A", "B", "C", "D"]
    explanation : str

# define state
class StudentState(TypedDict):
    student_id : str
    topic : str
    question : str
    correct_answer : str
    explanation : str
    answer : str
    analysis : str
    attempt : int
    stage : str
    human_decision : str
    advice : str
    final_message : str

# START -> Questions_agent -> collect answer -> Perfomance_agent -> Human_review -> Question_agent or placement -> final verdict -> END

# Agent-1 : Question agent
def question_agent(state : StudentState):
    generator = llm.with_structured_output(MCQ)

    data = generator.invoke(
    f"""    Generate one multiple-choice question on {state['topic']}.

    You must provide all these fields:
    1. question: The question text
    2. A: First option
    3. B: Second option
    4. C: Third option
    5. D: Fourth option
    6. correct_answer: The correct option letter (A, B, C, or D)
    7. explanation: Explain why the answer is correct.

    Ensure that all required fields are included."""
    )

    question = f"""{data.question}

                    A : {data.A}
                    B : {data.B}
                    C : {data.C}
                    D : {data.D}"""

    return {
        "question" : question,
        "correct_answer" : data.correct_answer,
        "explanation" : data.explanation,
        "answer" : "",
        "attempt" : state['attempt'] + 1,
        "stage" : "student_test"
    }


# Node-2 : collect answer
def collect_answer(state):
    answer = interrupt("Waiting for Student answer")

    return {
        "answer" : answer,
        "stage" : "evaluating"
    }

# Node-3 : Perfomance_agent
def performance_agent(state):
    is_correct = (state['answer'].upper() == state['correct_answer'])

    response = llm.invoke(
        f"""Evaluate the Students answer
            Topic : {state['topic']}
            Question : {state['question']}
            The answer given by student is {is_correct} 

            Please Give perfomance analysis:
            1. Display Correct or Wrong
            2. Brief feedback
"""
    )

    return {
        "analysis" : response.content,
        "stage" : "human_review"
    }

# Node-4 : human review 
def human_review(state):
    decision = interrupt("Waiting for human decision")

    return {
        "human_decision" : decision,
        "stage" : "routing"
    }

# Node-5 : placement agent
def placement_agent(state):
    response = llm.invoke(
        f"Here is the student performance : {state['analysis']}"
        f"Here is the teacher feedback : {state['human_decision']}"
        f"Suggest should we refer to this student for placement or not based upon above data"
    )
    return {
        "advice" : response.content,
        "stage" : "Congratulation"
    }

# Node-6 : congratulation node
def congratulation_agent(state):
    response = llm.invoke("Give a short but motivating congratulation message. Give a funny title")
    return {
        "final_message" : response.content,
        "stage" : "completed"
    }


"""
Workflow:
START -> Questions_agent -> collect answer -> Perfomance_agent -> Human_review -> Another attempt or placement -> placment node -> congratulation -> END
"""

# routing function
def route_decision(state):
    if state['human_decision'] == "another":
        return "question"
    return "placement"

def build_app(checkpointer):
    graph = StateGraph(StudentState)

    graph.add_node("question", question_agent )
    graph.add_node("collect_answer", collect_answer)
    graph.add_node("performance", performance_agent )
    graph.add_node("human_review", human_review )
    graph.add_node("placement", placement_agent )
    graph.add_node("congratulation", congratulation_agent)

    graph.add_edge(START, "question")
    graph.add_edge("question","collect_answer" )
    graph.add_edge("collect_answer", "performance" )
    graph.add_edge("performance", "human_review" )

    graph.add_conditional_edges(
        "human_review",
        route_decision,
        {
            "question" : "question",
            "placement" : "placement"
        }
    )

    graph.add_edge("placement", "congratulation")
    graph.add_edge("congratulation", END)

    app = graph.compile(checkpointer = checkpointer)
    return app

# sql database to maintain the status of each student
conn = sqlite3.connect("student_assessment.db", check_same_thread=False)
checkpointer = SqliteSaver(conn)
checkpointer.setup()

app = build_app(checkpointer)

# frontend of the application
st.title("MultiAgent Human in loop langgraph")

student_id = st.text_input("student id", value = "student_101")
topic = st.text_input("Topic", placeholder = "Python, SQL, GenAI...")

config = {
    "configurable" : {"thread_id" : student_id}
}

if st.button("Start Assessment"):
    checkpointer.delete_thread(student_id)  # deleting if same student workflow is working
    initial_state ={
            "student_id" : student_id,
            "topic" : topic,
            "question" : "",
            "correct_answer" : "",
            "explanation" : "",
            "answer" : "",
            "analysis" : "",
            "attempt" : 0,
            "stage" : "starting",
            "human_decision" : "",
            "advice" : "",
            "final_message" : ""
    }

    app.invoke(initial_state, config = config )
    st.session_state["active_student"] = student_id
    st.rerun()

if st.session_state.get("active_student") == student_id and student_id and topic:
    # loading the latest state of the graph
    snapshot = app.get_state(config)
    state = snapshot.values

    if state:
        # Main heading
        st.divider()
        st.subheader(f"Topic : {state['topic']}")
        st.caption(f"Test sttempt: {state['attempt']}")

        # MCQ test heading
        if state['stage'] == "student_test":
            st.subheader(f"MCQ Test")
            st.text(state['question'])

            # receiving answer in form of radio button
            with st.form("Submit the Answer"):
                answer = st.radio(
                    "Select one option", 
                    ["A", "B", "C", "D"]
                )
                submitted = st.form_submit_button("SUBMIT")

            if submitted:
                app.invoke(
                    Command(resume = answer),
                    config = config
                )
        elif state['stage'] == "human_review":
            st.subheader("Performance of student")
            st.write(state['analysis'])

            col1, col2 = st.columns(2)

            if col1.button("Give Test again"):
                app.invoke(
                    Command(resume = "another"),
                    config = config
                )
                st.rerun()

            if col2.button("Go to Placment section"):
                app.invoke(
                    Command(resume = "finish"),
                    config = config
                )
                st.rerun()

        elif state["stage"] == "completed":
            st.subheader("Placement advice")
            st.success("Congratulations")
            st.write(state['advice'])
            st.subheader("final remarks")
            st.write(state['final_message'])