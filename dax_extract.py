import requests
from bs4 import BeautifulSoup
import csv
from datetime import datetime

urls = [
    "https://www.fxempire.com/indices/de30-eur/news"
]

def extract_dax_news_from_url(url):
    dax_news = []
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    soup = BeautifulSoup(response.content, 'html.parser')
    articles = soup.find_all('a', href=True)
    
    
    for article in articles:
        
        title = article.get_text(strip=True)

        date_tag = article.find_parent('article').find('time') if article.find_parent('article') else None
        publish_date = None
        
        if date_tag and date_tag.has_attr('datetime'):
            publish_date = date_tag['datetime']
        
        if not publish_date and date_tag:
            publish_date = date_tag.get_text(strip=True)
        
        if not publish_date:
            continue
        
        dax_news.append({'title': title, 'publish_date': publish_date})

    return dax_news

csv_file = 'dax_news.csv'
file_exists = False
try:
    with open(csv_file, 'r', newline='', encoding='utf-8'):
        file_exists = True
except FileNotFoundError:
    pass

with open(csv_file, 'a', newline='', encoding='utf-8') as csvfile:
    fieldnames = ['date', 'title']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    if not file_exists:
        writer.writeheader()

    for url in urls:
        print(f"Scraping news from {url}...")
        dax_news = extract_dax_news_from_url(url)
        
        for news in dax_news:
            writer.writerow({'date': news['publish_date'], 'title': news['title']})

print(f"All DAX-related articles have been saved to '{csv_file}'.")