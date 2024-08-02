import openai
import pandas as pd
import numpy as np
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()
openai.api_key = os.getenv('OPENAI_API_KEY')

# Function to load scraped data
def load_data(filename='web-scraped.csv'):
    return pd.read_csv(filename)

# Function to get embeddings for a given text
def get_embedding(text):
    try:
        response = openai.Embedding.create(
            model='text-embedding-ada-002',
            input=text
        )
        return response['data'][0]['embedding']
    except Exception as e:
        print(f"Error getting embedding for text: {text}\n{e}")
        return np.nan

# Function to process the data and get embeddings
def process_data(df):
    df['embedding'] = df['summary'].apply(get_embedding)
    return df

# Function to save embeddings to a file
def save_embeddings(df, filename='scrapped.csv'):
    df.to_csv(filename, index=False)
    print(f"Embeddings saved to {filename}")

if __name__ == '__main__':
    # Load scraped data
    data = load_data()

    # Process data to get embeddings
    data_with_embeddings = process_data(data)

    # Save embeddings to a file
    save_embeddings(data_with_embeddings)
