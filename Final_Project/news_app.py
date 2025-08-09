import streamlit as st
import pandas as pd 
import requests
from transformers import pipeline
import os
from dotenv import load_dotenv


# Initialize summarizer
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

# Streamlit UI
st.title("📰 News Summarizer App")
st.markdown("Get the latest headines with quick summaries")

# Load token from .env file
load_dotenv()
api_key = os.getenv("NEWS_API_KEY")

country = st.selectbox("Select Country :", ['in', 'us', 'gb', 'ca'])
query = st.text_input("Enter Keyword (optional) :")

if st.button("Get News"):
    url = f"https://newsapi.org/v2/top-headlines?country={country}&q={query}&apiKey={api_key}"
    response = requests.get(url)
    
    articles = response.json().get('articles', [])
    all_summaries = []
    
    for article in articles[:3]: # Top 5 article
        title = article['title']
        content = article.get('content', '')
        link = article['url']
        
        st.header(title)
        if content:
            summary = summarizer(content, max_length = 50, min_length = 25, do_sample = False)[0]
            st.write(summary)
            all_summaries.append({
                "Title" : title,
                "Summary" : summary,
                "Article Link" : article['url']
            })
            
        else:
            st.write("No content to summarize.")
            st.markdown(f"[Read more]({article['url']})")
            
    if all_summaries:
        df = pd.DataFrame(all_summaries)
        csv_data = df.to_csv(index=False)
        
        st.markdown("### 📁 Download News")
        st.download_button(
            label="📥CSV Format",
            data=csv_data,
            file_name="top_news.csv",
            mime="text/csv",
            help="Download the top 3 news as a CSV file"
        )
    
    else:
        st.markdown('''#### ❌ There is no articles as of now!
                       - Try Different country or query...''')
            
    

            