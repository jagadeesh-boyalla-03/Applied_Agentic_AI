# Agent with Langchain + Memory

# Libraries
import os
from dotenv import load_dotenv

import requests
import streamlit as st

from langchain_groq import ChatGroq
from langchain_core.tools import tool
from langchain.agents import create_agent
from langgraph.checkpoint.memory import InMemorySaver  # reserve the memory of the agent
# load the api key from .env file
load_dotenv()

# initialize the llm
llm = ChatGroq(
    model = "openai/gpt-oss-20b",
    api_key = os.environ["GROQ_API_KEY"]
)

@tool
def get_weather(city : str):

    """Get the current weather (Temperature, Weather condition and humidy) from a given city"""
    # above docstring is compulsory in tool section
    # above docstring tell to the LLM what is the use of this particular tool

    url = f"https://wttr.in/{city}?format=j1"

    data = requests.get(url).json()

    weather = data["current_condition"][0]

    return f"""
                Tempearture : {weather["temp_C"]}
                Weather_conditon : {weather["weatherDesc"][0]["value"]}
                Humidity : {weather["humidity"]}
"""

# create memory
memory = st.cache_resource(InMemorySaver)()

agent = create_agent(
    model = llm,
    tools = [get_weather],
    system_prompt = "You are a helpful weather assistant who have memory. Answer the question by using the provided tool",
    checkpointer = memory
)

st.title("Weather Chat Agent with Memory")

# creating  a chat list, to store the previous chat
if "chat" not in st.session_state:
    st.session_state.chat = []
# writtinhg all 
for msg in st.session_state.chat:
    st.chat_message(msg["role"]).write(msg["content"])

user_input = st.chat_input("Ask about weather..")

if user_input:
    st.chat_message("user").write(user_input)

    response = agent.invoke(
        {"messages" : [{"role" : "user", "content" : user_input}]},
        config = {"configurable" : {"thread_id" : "1"}}  # access the memory of thread =1 chat
    )

    answer = response["messages"][-1].content
    st.chat_message("assistant").write(answer)

    st.session_state.chat.append({"role": "user", "content" : user_input})
    st.session_state.chat.append({"role" : "assistant", "content" : answer})