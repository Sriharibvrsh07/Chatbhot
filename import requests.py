import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime, timedelta

# Define the URL and the time range for scraping (last 45 days)
url = 'https://news.metal.com/list/industry/aluminium'
end_date = datetime.now()
start_date = end_date - timedelta(days=45)

def scrape_news(url):
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception(f"Failed to load page {url}")
    
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Print the soup content to understand its structure
    print(soup.prettify()[:2000])  # Print the first 2000 characters of the HTML

    articles = []

    # Adjust this part based on the actual HTML structure
    for item in soup.find_all('div', class_='newsItemContent___2oFIU'):
        title_tag = item.find('div', class_='title___1baLV')
        summary_tag = item.find('div', class_='description__z7ktb descriptionspec__lj3uG')
        date_tag = item.find('div', class_='date___3dzkE')
        
        title = title_tag.get_text().strip() if title_tag else 'No title'
        summary = summary_tag.get_text().strip() if summary_tag else 'No summary'
        date_str = date_tag.get_text().strip() if date_tag else 'No date'
        
        try:
            date = datetime.strptime(date_str, '%b %d, %Y %H:%M')
            if start_date <= date <= end_date:
                articles.append({
                    'title': title,
                    'summary': summary,
                    'date': date.strftime('%Y-%m-%d %H:%M')
                })
        except ValueError:
            print(f"Date format error with date: {date_str}")

    return articles

def save_to_csv(articles, filename='web-scraped.csv'):
    df = pd.DataFrame(articles)
    if df.empty:
        raise ValueError("No data scraped; DataFrame is empty.")
    df.to_csv(filename, index=False)
    print(f"Data saved to {filename}")

if __name__ == '__main__':
    articles = scrape_news(url)
    save_to_csv(articles)
