import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup
import openai
import json

# Function to retrieve OpenAI API key
def get_openai_key(email):
    url = 'http://52.66.239.27:8504/get_keys'
    payload = json.dumps({"email": email})
    headers = {'Content-Type': 'application/json'}
    
    response = requests.post(url, headers=headers, data=payload)
    
    if response.status_code == 200:
        return response.json().get('key')  # Adjust based on the actual response structure
    else:
        st.error("Failed to retrieve API key.")
        return None

# Set your OpenAI API key from the API call
email = "venkatasrihari.b_2025@woxsen.edu.in"  # Replace with your actual email address
openai.api_key = get_openai_key(email)

# Function to extract and summarize article
def summarize_article(url):
    try:
        # Send a request to fetch the article content
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')

        # Extract article content
        content_div = soup.find('div', class_='content FUFa')  # Adjust class based on actual structure
        paragraphs = content_div.find_all('p') if content_div else []
        article_content = ' '.join([p.get_text() for p in paragraphs])

        # Use OpenAI API to summarize the article
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": f"Summarize this article: {article_content}"}
            ],
            max_tokens=150,
            temperature=0.7,
        )
        summary = response['choices'][0]['message']['content']

        return summary
    except Exception as e:
        return str(e)  # Return error message

# Load the news data
news_df = pd.read_csv('aluminum_news.csv')

# Streamlit application
st.set_page_config(page_title='News Chatbot', page_icon=':newspaper:', layout='wide')
st.markdown(
    """
    <style>
    body {
        background-color: skyblue;
    }
    .enter-button {
        background-color: white;
        color: black;
        padding: 10px;
        border: none;
        border-radius: 5px;
        cursor: pointer;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title('News Chatbot')

query = st.text_input("Ask me anything about aluminum industry news")

if st.button("Enter", key="submit"):
    if query:
        results = news_df[news_df.apply(lambda row: query.lower() in row['title'].lower() or query.lower() in row['description'].lower(), axis=1)]

        if not results.empty:
            for index, row in results.iterrows():
                url = row['link']
                title = row['title']  # Get the title from the CSV
                date = row['date']    # Get the published date from the CSV
                summary = summarize_article(url)  # Get summary from the article

                st.write(f"### {title}")
                st.write(f"**Published on:** {date}")  # Display the date from CSV
                st.write(f"**Summary:**")
                st.text_area(label="", value=summary, height=150)  # Box for summary
        else:
            st.write("No matching articles found.")
