import streamlit as st
import requests
from datetime import datetime
import os 
from dotenv import load_dotenv
load_dotenv()

st.title("🎉 Holiday Finder App")

st.sidebar.header("Select Parameters")
country = st.sidebar.selectbox("Country", ["IN", "US", "GB", "CA", "AU"])
year = st.sidebar.slider("Year", min_value=2000, max_value=datetime.now().year, value=datetime.now().year)

# API Key (You can use st.secrets when deployed)
API_KEY = os.getenv('CALENDARIFIC_API_KEY')

# Fetch data
url = f"https://calendarific.com/api/v2/holidays?api_key={API_KEY}&country={country}&year={year}"
response = requests.get(url)

if response.status_code == 200:
    data = response.json()
    holidays = data["response"]["holidays"]
    
    st.success(f"Found {len(holidays)} holidays for {country} in {year} 🎊")

    for h in holidays:
        st.markdown(f"""
        ### {h['name']}
        - 📅 Date: {h['date']['iso']}
        - 📂 Type: {', '.join(h['type'])}
        - 📜 Description: {h['description']}
        ---
        """)
else:
    st.error("API call failed. Check API key or rate limit.")
