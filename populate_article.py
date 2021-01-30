import os
# django project name is adleads, replace adleads with your project name
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")
import django
django.setup()
from database.models import *
from newsfetch.google import google_search
from newsfetch.news import newspaper
import requests
from bs4 import BeautifulSoup
import json

# scraping function
def get_rss(url):
    article_links = []

    try:
        r = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
        soup = BeautifulSoup(r.content, features='xml')
        articles = soup.findAll('item')        
        for a in articles:
            link = a.find('link').text
            article_links.append(link)
        # print('The scraping job succeeded: ', r.status_code)
        return article_links[:3]
    except Exception as e:
        print(e)

def extract_info(article_links,category,source):
    for link in article_links:
        news = newspaper(link)
        title = news.headline
        summary = news.summary
        keywords = news.keywords
        publication_date = news.date_publish,
        article = Article(title=title,link=link,summary=summary,keywords=keywords,category=category,source=source,publication_date=publication_date)
        article.save()
        print("article successfully saved to database")
        # article = {
        #     "title": title,
        #     "link": link,
        #     "summary": summary,
        #     "keywords": keywords,
        #     "category": category,
        #     "source": source
        # }
        # print(article)

if __name__ == '__main__':
    records = {
      "straitstimes" :{ 
        "world": "http://www.straitstimes.com/news/world/rss.xml",
        "business":"https://www.straitstimes.com/news/business/rss.xml"
        }
    }

    for source, _ in records.items():
        for category, url in records[source].items():
            article_links = get_rss(url)
            extract_info(article_links, category,source)




