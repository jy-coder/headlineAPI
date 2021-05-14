import os
import sys
sys.path.append(os.getcwd())
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")
import django
django.setup()
from database.models import *
from newsfetch.google import google_search
from newsfetch.news import newspaper
import requests
from bs4 import BeautifulSoup
import json
from textblob import TextBlob

# scraping from rss
def get_rss(url):
    article_links = []

    try:
        r = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
        soup = BeautifulSoup(r.content, features='xml')
        articles = soup.findAll('item')
        #print(articles)     
        for a in articles:
            link = a.find('link').text
            #print(link)
            article_links.append(link)
        # print('The scraping job succeeded: ', r.status_code)
        return article_links[:4]
    except Exception as e:
        print(e)

# scraping from url
def get_url(source,url):
    article_links = []

    try:
        r = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
        soup = BeautifulSoup(r.content, features='xml')
        link = ""
        if source == "Yahoo News":
            articles = soup.find_all('h3', class_='Mb(5px)')
            for a in articles:
                b = a.find('a', href=True)
                link = "https://news.yahoo.com"+b['href']
                article_links.append(link)
        elif source == "Foxnews":
            articles = soup.find_all('h2', class_='title')
            for a in articles:
                b = a.find('a', href=True)
                link = "https://www.foxnews.com"+b['href']
                article_links.append(link)
        elif source == "Vox":
            articles = soup.find_all('h2', class_='c-entry-box--compact__title')
            for a in articles:
                b = a.find('a', href=True)
                link = b['href']
                article_links.append(link)
        elif source == "Mothership":
            articles = soup.find_all('div', class_='ind-article ')
            for a in articles:
                b = a.find('a', href=True)
                link = b['href']
                article_links.append(link)
        elif source == "Asiaone":
            articles = soup.find_all('li', class_='ant-list-item')
            for a in articles:
                b = a.find('a', href=True)
                link = "https://www.asiaone.com"+b['href']
                article_links.append(link)



        return article_links[:3]
    except Exception as e:
        print(e)

def extract_noun(title):
    blob = TextBlob(title)
    phrase = str(blob.noun_phrases).replace("'","").replace('"','').replace("[","").replace("]","").replace(", ",",")
    return phrase

def extract_info(article_links,category,source):
    for link in article_links:
        news = newspaper(link)
        title = news.headline
        summary = news.summary
        keywords = extract_noun(title)
        publication_date = news.date_publish
        image_url = news.image_url
        description = ""


        
        # need to scrape description from each website that we want
        if source == "The Straits Times":
            # TODO: scape image url
            description_list = []
            page = requests.get(link, headers={'User-Agent': 'Mozilla/5.0'})
            soup = BeautifulSoup(page.content, 'html.parser')
            result = soup.find_all("p")
            for r in result[2:len(result)-3]:
                description_list.append(r.get_text() + "\n")
                # print(description_list)
            description = " ".join(description_list)
        
        # put all the new website u scrape here
        elif source == "Channel News Asia":
            # TODO: scape image url
            description_list = []
            page = requests.get(link, headers={'User-Agent': 'Mozilla/5.0'})
            soup = BeautifulSoup(page.content, 'html.parser')
            result = soup.find_all("p")
            for r in result[1:len(result)-2]:
                description_list.append(r.get_text() + "\n")
                # print(description_list)
            description = " ".join(description_list)

        elif source == "CNBC":
            # TODO: scape image url
            description_list = []
            page = requests.get(link, headers={'User-Agent': 'Mozilla/5.0'})
            soup = BeautifulSoup(page.content, 'html.parser')
            result = soup.find_all("p")
            for r in result[0:len(result)-6]:
                description_list.append(r.get_text() + "\n")
                # print(description_list)
            description = " ".join(description_list)

        elif source == "New York Daily News":
            # TODO: scape image url
            description_list = []
            page = requests.get(link, headers={'User-Agent': 'Mozilla/5.0'})
            soup = BeautifulSoup(page.content, 'html.parser')
            result = soup.find_all("p")
            for r in result[0:len(result)]:
                description_list.append(r.get_text() + "\n")
                # print(description_list)
            description = " ".join(description_list)

        elif source == "The Guardian":
            # TODO: scape image url
            description_list = []
            page = requests.get(link, headers={'User-Agent': 'Mozilla/5.0'})
            soup = BeautifulSoup(page.content, 'html.parser')
            result = soup.find_all("p")
            for r in result[0:len(result)]:
                description_list.append(r.get_text() + "\n")
                # print(description_list)
            description = " ".join(description_list)

        elif source == "Yahoo News":
            # TODO: scape image url
            description_list = []
            page = requests.get(link, headers={'User-Agent': 'Mozilla/5.0'})
            soup = BeautifulSoup(page.content, 'html.parser')
            result = soup.find_all("div", class_='caas-body')
            for r in result:
                a = r.find_all("p")
                for b in a:
                    description_list.append(b.get_text() + "\n")
                description = " ".join(description_list)

        elif source == "Foxnews":
            # TODO: scape image url
            description_list = []
            page = requests.get(link, headers={'User-Agent': 'Mozilla/5.0'})
            soup = BeautifulSoup(page.content, 'html.parser')
            result = soup.find_all("div", class_='article-body')
            for r in result:
                a = r.find_all("p")
                for b in a:
                    if b.find('strong') is None:
                        description_list.append(b.get_text() + "\n")
                description = " ".join(description_list)

        elif source == "New York Post":
            # TODO: scape image url
            description_list = []
            page = requests.get(link, headers={'User-Agent': 'Mozilla/5.0'})
            soup = BeautifulSoup(page.content, 'html.parser')
            result = soup.find_all("div", class_='entry-content entry-content-read-more')
            for r in result:
                a = r.find_all("p")
                for b in a:
                    description_list.append(b.get_text() + "\n")
                description = " ".join(description_list)

        elif source == "Vox":
            # TODO: scape image url
            description_list = []
            page = requests.get(link, headers={'User-Agent': 'Mozilla/5.0'})
            soup = BeautifulSoup(page.content, 'html.parser')
            result = soup.find_all("div", class_='c-entry-content')
            for r in result:
                a = r.find_all("p")
                for b in a[0:len(a)-1]:
                    description_list.append(b.get_text() + "\n")
                description = " ".join(description_list)

        elif source == "The New York Times":
            # TODO: scape image url
            description_list = []
            page = requests.get(link, headers={'User-Agent': 'Mozilla/5.0'})
            soup = BeautifulSoup(page.content, 'html.parser')
            result = soup.find_all("section", class_='meteredContent css-1r7ky0e')
            for r in result:
                a = r.find_all("p")
                for b in a:
                    if b.get_text() != "Advertisement":
                        description_list.append(b.get_text() + "\n")
                description = " ".join(description_list)

        elif source == "The Independent":
            # TODO: scape image url
            description_list = []
            page = requests.get(link, headers={'User-Agent': 'Mozilla/5.0'})
            soup = BeautifulSoup(page.content, 'html.parser')
            result = soup.find_all('div', class_='sc-pQSDG dKhAFM sc-oUmjU gbrbtK')
            for r in result:
                s = r.find_all("span", class_='sc-pJgJK fgkDub')
                for n in s:
                    description_list.append(n.get_text())
                description = "".join(description_list)

                a = r.find_all("p")
                for b in a:
                    description_list.append(b.get_text() + "\n")
                description = " ".join(description_list)

        elif source == "The Online Citizen":
            # TODO: scape image url
            description_list = []
            page = requests.get(link, headers={'User-Agent': 'Mozilla/5.0'})
            soup = BeautifulSoup(page.content, 'html.parser')
            result = soup.find_all("div", class_='content-inner')
            for r in result:
                a = r.find_all("p")
                for b in a:
                    description_list.append(b.get_text() + "\n")
                description = " ".join(description_list)

        elif source == "Mothership":
            # TODO: scape image url
            description_list = []
            page = requests.get(link, headers={'User-Agent': 'Mozilla/5.0'})
            soup = BeautifulSoup(page.content, 'html.parser')
            result = soup.find_all("div", class_='content-article-wrap')
            for r in result:
                a = r.find_all("p")
                for b in a:
                    if b.find('h2') is None:
                        description_list.append(b.get_text() + "\n")
                description = " ".join(description_list)

        elif source == "Asiaone":
            # TODO: scape image url
            description_list = []
            page = requests.get(link, headers={'User-Agent': 'Mozilla/5.0'})
            soup = BeautifulSoup(page.content, 'html.parser')
            result = soup.find_all("div", class_='body')
            for r in result:
                a = r.find_all("p")
                for b in a:
                    description_list.append(b.get_text() + "\n")
                description = " ".join(description_list)



            #for r in result[0:len(result)]:
            #    description_list.append(r.get_text() + "\n")
                # print(description_list)
            #description = " ".join(description_list)

        summary = description[:2000]

        if not description.isspace():
            if not description == "":
                findList = ["Corona Virus","Covid-19","Coronavirus"]
                for x in range(len(findList)):
                    if findList[x].lower() in title.lower():
                        category = "Covid-19"
                try:
                    article = Article(title=title,link=link,summary=summary.strip(),keywords=keywords,category=category,source=source,publication_date=publication_date,description=description.strip(),image_url=image_url)
                    article.save()
                    print("article successfully saved to database")
                except Exception as e:
                    print(e)

  



        #print to check each article
        #article = {
        #     "title": title,
        #     "link": link,
        #     "summary": summary,
        #     "keywords": keywords,
        #     "category": category,
        #     "source": source
        # }
        #print(article)

if __name__ == '__main__':
    # add more to this section
    rss = {
      "The Straits Times" :{ 
        "world": {
            "world": "http://www.straitstimes.com/news/world/rss.xml"
        },
        "business": {
            "business":"https://www.straitstimes.com/news/business/rss.xml"
        },
        "life": {
            "life":"https://www.straitstimes.com/news/life/rss.xml"
        },
        "singapore": {
            "singapore":"https://www.straitstimes.com/news/singapore/rss.xml"
        },
        "opinion": {
            "opinion":"https://www.straitstimes.com/news/opinion/rss.xml"
        },
        "asia": {
            "asia":"https://www.straitstimes.com/news/asia/rss.xml"
        },
        "tech": {
            "tech":"https://www.straitstimes.com/news/tech/rss.xml"
        },
        "sport": {
            "sport":"https://www.straitstimes.com/news/sport/rss.xml"
        }
     },
    
      "Channel News Asia":{
        "sport": {
            "sport":"https://www.channelnewsasia.com/rssfeeds/8395838"
        },
        "asia": {
            "asia":"https://www.channelnewsasia.com/rssfeeds/8395744"
        },
        "business": {
            "business":"https://www.channelnewsasia.com/rssfeeds/8395954"
        },
        "singapore": {
            "singapore":"https://www.channelnewsasia.com/rssfeeds/8396082"
        },
        "world": {
            "world":"https://www.channelnewsasia.com/rssfeeds/8395884"
        }
     },


      "CNBC":{
        "business": {
            "business":"https://www.cnbc.com/id/10001147/device/rss/rss.html",
            "economy":"https://www.cnbc.com/id/20910258/device/rss/rss.html"
        },
        "tech": {
            "tech":"https://www.cnbc.com/id/19854910/device/rss/rss.html"
        },
        "world": {
            "world":"https://www.cnbc.com/id/100727362/device/rss/rss.html",
            "politics":"https://www.cnbc.com/id/10000113/device/rss/rss.html"
        },
        "asia": {
            "asia":"https://www.cnbc.com/id/19832390/device/rss/rss.html"
        },
        "life": {
            "health":"https://www.cnbc.com/id/10000108/device/rss/rss.html",
            "travel":"https://www.cnbc.com/id/10000739/device/rss/rss.html"
        }
     },

      "New York Daily News":{
        "world": {
            "world":"https://www.nydailynews.com/arcio/rss/category/news/world/?query=display_date:%5Bnow-2d+TO+now%5D+AND+revision.published:true&sort=display_date:desc#nt=instory-link",
            "crime":"https://www.nydailynews.com/arcio/rss/category/news/crime/?query=display_date:%5Bnow-2d+TO+now%5D+AND+revision.published:true&sort=display_date:desc#nt=instory-link",
            "politics":"https://www.nydailynews.com/arcio/rss/category/news/politics/?query=display_date:%5Bnow-2d+TO+now%5D+AND+revision.published:true&sort=display_date:desc#nt=instory-link",
            "us":"https://www.nydailynews.com/arcio/rss/category/news/national/?query=display_date:%5Bnow-2d+TO+now%5D+AND+revision.published:true&sort=display_date:desc#nt=instory-link"
        },
        "sport": {
            "sport":"https://www.nydailynews.com/arcio/rss/category/sports/?query=display_date:%5Bnow-2d+TO+now%5D+AND+revision.published:true&sort=display_date:desc#nt=instory-link"
        },
        "life": {
            "entertainment":"https://www.nydailynews.com/arcio/rss/category/snyde/?query=display_date:%5Bnow-2d+TO+now%5D+AND+revision.published:true&sort=display_date:desc#nt=instory-link"
        }
     },
    
      "The Guardian":{ 
        "world": {
            "environment":"https://www.theguardian.com/uk/environment/rss",
            "world":"https://www.theguardian.com/world/rss"
        },
        "covid-19": {
            "covid-19":"https://www.theguardian.com/world/coronavirus-outbreak/rss"
        },
        "tech": {
            "science":"https://www.theguardian.com/science/rss",
            "tech":"https://www.theguardian.com/uk/technology/rss"
        },
        "business": {
            "business":"https://www.theguardian.com/uk/business/rss"
        },
        "opinion": {
            "opinion":"https://www.theguardian.com/uk/commentisfree/rss"
        },
        "sport": {
            "sport":"https://www.theguardian.com/uk/sport/rss"
        },
        "life": {
            "games":"https://www.theguardian.com/games/rss",
            "music":"https://www.theguardian.com/music/rss",
            "books":"https://www.theguardian.com/books/rss",
            "art&design":"https://www.theguardian.com/artanddesign",
            "travel":"https://www.theguardian.com/uk/travel/rss",
            "money":"https://www.theguardian.com/uk/money/rss",
            "food":"https://www.theguardian.com/food/rss",
            "fashion":"https://www.theguardian.com/fashion/rss"
        },
      },

    "New York Post":{ 
        "tech": {
            "tech":"https://nypost.com/tech/feed/",
        },
        "sport": {
            "sport":"https://nypost.com/sports/feed/",
        },
        "business": {
            "business":"https://nypost.com/business/feed/",
        },
        "opinion": {
            "opinion":"https://nypost.com/opinion/feed/",
        },
        "life": {
            "entertainment":"https://nypost.com/entertainment/feed/",
            "fashion":"https://nypost.com/fashion/feed/",
        },
     },
    "The New York Times":{ 
        "tech": {
            "tech":"https://rss.nytimes.com/services/xml/rss/nyt/Technology.xml",
        },
        "world": {
            "world":"https://rss.nytimes.com/services/xml/rss/nyt/World.xml",
        },
        "business": {
            "business":"https://rss.nytimes.com/services/xml/rss/nyt/Business.xml",
            "money":"https://rss.nytimes.com/services/xml/rss/nyt/YourMoney.xml",
            "economy":"https://rss.nytimes.com/services/xml/rss/nyt/Economy.xml",
        },
        "sports": {
            "sports":"https://rss.nytimes.com/services/xml/rss/nyt/Sports.xml",
        },
        "life": {
            "health":"https://rss.nytimes.com/services/xml/rss/nyt/Health.xml",
            "art":"https://rss.nytimes.com/services/xml/rss/nyt/Arts.xml",
            "books":"https://rss.nytimes.com/services/xml/rss/nyt/Books.xml",
            "movies":"https://rss.nytimes.com/services/xml/rss/nyt/Movies.xml",
            "music":"https://rss.nytimes.com/services/xml/rss/nyt/Music.xml",
            "fashion":"https://rss.nytimes.com/services/xml/rss/nyt/FashionandStyle.xml",
            "travel":"https://rss.nytimes.com/services/xml/rss/nyt/Travel.xml",
        },
     },
    "The Independent":{ 
        "world": {
            "world":"https://www.independent.co.uk/news/world/rss",
        },
        "tech": {
            "tech":"https://www.independent.co.uk/life-style/gadgets-and-tech/rss",
        },
        "business": {
            "business":"https://www.independent.co.uk/news/business/rss",
            "money":"https://www.independent.co.uk/money/rss",
        },
        "sports": {
            "sports":"https://www.independent.co.uk/sport/rss",
        },
        "life": {
            "art":"https://www.independent.co.uk/arts-entertainment/art/rss",
            "fashion":"https://www.independent.co.uk/life-style/fashion/rss",
            "food&drink":"https://www.independent.co.uk/life-style/food-and-drink/rss",
            "travel":"https://www.independent.co.uk/travel/rss",
        },
       },
    "The Online Citizen":{ 
        "world": {
            "international":"https://www.theonlinecitizen.com/category/international/feed/",
            "politics":"https://www.theonlinecitizen.com/category/politics/feed/",
        },
        "asia": {
            "asia":"https://www.theonlinecitizen.com/category/asia/feed/",
        },
        "business": {
            "business":"https://www.theonlinecitizen.com/category/business/feed/",
            "economics":"https://www.theonlinecitizen.com/category/economics/feed/",
        },
        "life": {
            "art&culture":"https://www.theonlinecitizen.com/category/arts-culture/feed/",
            "travel":"https://www.theonlinecitizen.com/category/travel/feed/",
        },
     }

    }
      
        
    

    urlD = {
        "Yahoo News":{ 
            "world": {
                "world":"https://news.yahoo.com/world/",
                "politics":"https://news.yahoo.com/politics/"
            },
            "life": {
                "health":"https://news.yahoo.com/health/"
            },
            "tech": {
                "science":"https://news.yahoo.com/science/"
            }
        },
        "Foxnews":{ 
            "sport": {
                "sport":"https://www.foxnews.com/sports",
            },
            "world": {
                "politics":"https://www.foxnews.com/politics"
            },
            "opinion": {
                "opinion":"https://www.foxnews.com/opinion"
            },
            "tech": {
                "tech":"https://www.foxnews.com/tech"
            },
            "life": {
                "entertainment":"https://www.foxnews.com/entertainment",
                "lifestyle":"https://www.foxnews.com/lifestyle",
                "health":"https://www.foxnews.com/health"
            }
        },
        "Vox":{ 
            "world": {
                "politics":"https://www.vox.com/policy-and-politics",
                "world":"https://www.vox.com/world",
            },
            "covid-19": {
                "covid-19":"https://www.vox.com/coronavirus-covid19/",
            },
            "tech": {
                "technology":"https://www.vox.com/technology",
            },
            "business": {
                "business":"https://www.vox.com/business-and-finance",
            },
            "life": {
                "culture":"https://www.vox.com/culture",
                "sience&health":"https://www.vox.com/science-and-health",
            },
        },
        "Mothership":{
            "covid-19": {
                "covid-19":"https://mothership.sg/tag/covid-19/",
            },
            "life": {
                "drama":"https://mothership.sg/category/lifestyle/drama/",
                "travel":"https://mothership.sg/category/lifestyle/travel/",
                "lifestyle":"https://mothership.sg/category/lifestyle/lifestyle-news/",
            },
        },
        "Asiaone":{ 
            "world": {
                "world":"https://www.asiaone.com/world",
            },
            "business": {
                "money":"https://www.asiaone.com/money",
                "business":"https://www.asiaone.com/business",
            },
            "asia": {
                "asia":"https://www.asiaone.com/asia",
            },
            "singapore": {
                "singapore":"https://www.asiaone.com/singapore",
            },
            "life": {
                "entertainment":"https://www.asiaone.com/showbiz",
                "lifestyle":"https://www.asiaone.com/lifestyle",
                "food":"https://www.asiaone.com/food",
                "health":"https://www.asiaone.com/health",
                "travel":"https://www.asiaone.com/travel",
            },
        },

      
    }

    for source, _ in rss.items():
        for mainCategory, _ in rss[source].items():
            for category, url in rss[source][mainCategory].items():
                article_links = get_rss(url)
                print(article_links)
                extract_info(article_links, mainCategory, source)

    for source, _ in urlD.items():
        for mainCategory, _ in urlD[source].items():
            for category, url in urlD[source][mainCategory].items():
                article_links = get_url(source, url)
                print(article_links)
                extract_info(article_links, mainCategory, source)
