# First agent - Weather prediction

# library 
import os   # to access api key file
from dotenv import load_dotenv   # to load api key

from groq import Groq   # accessing the LLM
import requests  # send HTTP request
import streamlit as st   # to built frontend

load_dotenv()  # loading api key

client = Groq(api_key = os.environ["GROQ_API_KEY"])  # client to access LLM

st.title("Weather Agent")
city = st.text_input("Enter city name")

def get_weather(city):
    url = f"https://wttr.in/{city}?format=j1"

    data = requests.get(url).json()

    weather = data["current_condition"][0]

    return f"""
                Tempearture : {weather["temp_C"]}
                Weather_conditon : {weather["weatherDesc"][0]["value"]}
                Humidity : {weather["humidity"]}
"""

if st.button("Get Weather") and city:
    weather = get_weather(city)
    response = client.chat.completions.create(
        model = "openai/gpt-oss-20b",
        messages = [
            {
                "role" : "system",
                "content" : "You are a helpful weather assistant."
            },
            {
                "role" : "user",
                "content" : f"What is the current weather in {city}. Weather data : {weather}"
            }
        ]
    )
    st.write(response.choices[0].message.content)