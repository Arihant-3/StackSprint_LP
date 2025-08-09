# github_dashboard.py

import streamlit as st
import requests
import pandas as pd
import os
from dotenv import load_dotenv

# Load token from .env file
load_dotenv()
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

# Headers with authentication
headers = {
    "Authorization": f"Bearer {GITHUB_TOKEN}",
    "Accept": "application/vnd.github+json"
}

st.title("🐙 GitHub Developer Dashboard")

# User input
username = st.text_input("Enter GitHub username", value="octocat")

if username:
    # Get user info
    user_url = f"https://api.github.com/users/{username}"
    user_resp = requests.get(user_url, headers=headers).json()

    if 'message' in user_resp and user_resp['message'] == 'Not Found':
        st.error("User not found.")
    else:
        st.subheader(f"{user_resp['login']} - {user_resp.get('name', '')}")
        st.markdown(f"- 📍 Location: {user_resp.get('location', 'N/A')}")
        st.markdown(f"- 📦 Public Repos: {user_resp['public_repos']}")
        st.markdown(f"- 👥 Followers: {user_resp['followers']}, Following: {user_resp['following']}")
        st.image(user_resp['avatar_url'], width=100)

        # Get repositories
        repo_url = f"https://api.github.com/users/{username}/repos?per_page=100"
        repo_resp = requests.get(repo_url, headers=headers).json()

        if isinstance(repo_resp, list):
            df = pd.DataFrame([{
                'Name': r['name'],
                '⭐ Stars': r['stargazers_count'],
                '🍴 Forks': r['forks_count'],
                '🔤 Language': r['language'],
                '📅 Updated': r['updated_at'][:10]
            } for r in repo_resp])
            
            st.dataframe(df.sort_values(by="⭐ Stars", ascending=False))
            
            st.write("Top 5 Repositories:")
            st.dataframe(df.head(5).sort_values(by="📅 Updated", ascending=False))
            
            st.bar_chart(df.set_index('Name')[['⭐ Stars', '🍴 Forks']])
            
        else:
            st.warning("Could not fetch repositories.")
