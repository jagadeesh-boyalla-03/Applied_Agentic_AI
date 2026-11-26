# Build Langchain Agent which can make Decision

# Build a agent which can decide weather to carry the Umbrella or not based upon weather

# Libraries
import os
from dotenv import load_dotenv
import requests
import streamlit as st
from langchain_groq import ChatGroq
from langchain_core.tools import tool
from langchain.agents import create_agent

# loading the api key from .env file
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

# creating agent using langchian function
agent = create_agent(
    model = llm,
    tools = [get_weather],
    system_prompt = """You are a weather decision making agent.

                        Use the get_weather tool to predict about weather 

                        if weather condition is not good then recommand Umbrella otherwise not.
    """
)

# building frontend
st.title("Weather Decision making Agent")

city = st.text_input("Enter City Name")

if st.button("Check Umbrella needed or not") and city:
    response = agent.invoke({
        "messages" : [{"role" : "user", "content" : f"Should i Carry an Umbrella in {city} based upon weather"}]
    })

    st.write(response["messages"][-1].content)