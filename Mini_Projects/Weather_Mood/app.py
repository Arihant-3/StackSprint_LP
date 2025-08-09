import streamlit as st
import pandas as pd 
import requests
import json
import os 
from dotenv import load_dotenv
load_dotenv()

st.title("☁️ Live Weather Dashboard and Mood App ")
city = st.text_input("Enter City Name")

# API URLs and key
weather_url = 'https://api.openweathermap.org/data/2.5/weather'
quote_url = 'https://zenquotes.io/api/random'
api_key = os.getenv('OPEN_WEATHER_API_KEY')

weather_mood_cat = {
    'Clear': 'Joyful',
    'Sunny': 'Joyful',
    'Rain': 'Melancholic',
    'Snow': 'Peaceful',
    'Clouds': 'Neutral',
    'Thunderstorm': 'Tense',
    'Drizzle': 'Melancholic',
    'Mist': 'Neutral',
    'Fog': 'Neutral',
    'Haze': 'Neutral',
    'Smoke': 'Tense'
    }


# Only run if user has entered a city
if city:
    weather_param = {
        'appid' : api_key,
        'units' : 'metric',
        'q' : city
    }

    response = requests.get(weather_url, params=weather_param)

    if response.status_code == 200:
        data = response.json()

        weather = data['weather'][0]['main']
        temp = data['main']['temp']

        mood = weather_mood_cat.get(weather, 'Neutral')

        mood_response = requests.get(quote_url)
        if mood_response.status_code == 200:
            quote_data = mood_response.json()
            quote = quote_data[0]['q']
            author = quote_data[0]['a']
        else:
            quote = "No quote available for this mood."
            author = ""

        st.markdown(f"""
        ### 🏙️ City ~ {city}
        - Weather : {weather}, {temp} °C
        - Mood : {mood}
        - Quote : 
        > *{quote}*  
        \- **{author}**
        ---
        """)
        
    else:
        st.error("City not found. Please try again.")
