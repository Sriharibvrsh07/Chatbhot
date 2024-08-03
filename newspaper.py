import requests
from bs4 import BeautifulSoup
import pandas as pd

def scrape_aluminum_news():
    url = "https://news.metal.com/list/industry/aluminium"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    articles = soup.find_all('div', class_='newsItem___wZtKx')
    
    news_data = []
    for article in articles:
        title_tag = article.find('div', class_='title___1baLV')
        description_tag = article.find('div', class_='description___z7ktb descriptionspec___lj3uG')
        link_tag = article.find('a', href=True)
        date_tag = article.find('div', class_='date___3dzkE')  # Class for the date

        if title_tag and description_tag and link_tag:
            title = title_tag.get_text(strip=True)
            description = description_tag.get_text(strip=True)
            link = link_tag['href']
            date = date_tag.get_text(strip=True) if date_tag else "No date found"  # Extract date if available
            
            news_data.append({
                'title': title,
                'link': link,
                'description': description,
                'date': date  # Add the date to the news data
            })
    
    return pd.DataFrame(news_data)

news_df = scrape_aluminum_news()
news_df.to_csv('aluminum_news.csv', index=False)
