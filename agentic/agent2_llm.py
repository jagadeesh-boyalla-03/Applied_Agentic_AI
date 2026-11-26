import os
from dotenv import load_dotenv
import requests
import streamlit as st

from langchain_groq import ChatGroq
from langchain_core.tools import tool
from langchain.agents import create_agent

# loading api key
load_dotenv()

# initializing the client to access LLM

llm = ChatGroq(
    api_key=os.environ["GROQ_API_KEY"],
    model="openai/gpt-oss-20b"
)

@tool
def get_weather(city: str) -> str:
    """
    Get the current weather for a given city.
    """
    url = f"https://wttr.in/{city}?format=j1"

    data = requests.get(url).json()

    weather = data["current_condition"][0]

    return f"""
Temperature : {weather['temp_C']}°C
Weather Condition : {weather['weatherDesc'][0]['value']}
Humidity : {weather['humidity']}%
"""

agent = create_agent(
    model=llm,
    tools=[get_weather],
    system_prompt="You are a helpful weather assistant. Use available tools to get the current weather for a given city."
)

# Build Streamlit frontend

st.title("Weather Agent")

city = st.text_input("Enter city name")

if st.button("Find Weather Condition") and city:

    response = agent.invoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": f"What is the current weather in {city}?"
                }
            ]
        }
    )

    st.write(response["messages"][-1].content)
