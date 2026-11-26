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


# Weather Tool

@tool
def get_weather(city: str) -> str:
    """
    Get the current weather for a given city.
    """
    url = f"https://wttr.in/{city}?format=j1"

    response = requests.get(url)

    if response.status_code != 200:
        return f"Could not get weather information for {city}."

    data = response.json()

    weather = data["current_condition"][0]

    return f"""
Temperature : {weather['temp_C']}°C
Weather Condition : {weather['weatherDesc'][0]['value']}
Humidity : {weather['humidity']}%
"""


# Country Information Tool

@tool
def get_country_info(country: str) -> str:
    """
    Get information about a given country.
    """
    url = f"https://restcountries.com/v3.1/name/{country}"

    response = requests.get(url)

    # Check if API request was successful
    if response.status_code != 200:
        return f"Could not find country information for '{country}'."

    data = response.json()

    # Check if API returned a list
    if not isinstance(data, list) or len(data) == 0:
        return f"Could not find country information for '{country}'."

    country_data = data[0]

    name = country_data["name"]["common"]

    capital = country_data.get(
        "capital",
        ["Not available"]
    )[0]

    population = country_data.get(
        "population",
        "Not available"
    )

    region = country_data.get(
        "region",
        "Not available"
    )

    return f"""
Country : {name}
Capital : {capital}
Population : {population}
Region : {region}
"""


# Create Agent

agent = create_agent(
    model=llm,
    tools=[get_weather, get_country_info],
    system_prompt="""
    You are a helpful assistant.

    Use get_weather for cities.]
    Use get_country_info only for countries.

    If the user gives a city, get its current weather.

    If the user gives a country, get its country information.

    Do not use get_country_info for cities.
    Do not use get_weather for countries unless the user specifically asks
    for weather in that country.
    """
)


# Build Streamlit frontend

st.title("Weather & Country Information Agent")

query = st.text_input("Enter city or country name")


if st.button("Find Information") and query:

    response = agent.invoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": f"What is the current weather and information about {query}?"
                }
            ]
        }
    )

    st.write(response["messages"][-1].content)
