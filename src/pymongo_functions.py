import pymongo
import time
import random
from selenium.webdriver import Firefox


mc = pymongo.MongoClient()
db = mc['game_recommender']
raw_html_coll = db['raw_html']
raw_html_dict = {row['url']: row['html'] for row in raw_html_coll.find()}

amc=pymongo.MongoClient()
cb=amc['ps4_game_data']
games=cb['games']

def get_game_info(key="name", value=""):
    """Returns all game information for game given the key & value in the game dict"""
    return games.find_one({key : value})




def store_html(url, html, coll=raw_html_coll):
    """"Store raw HTML in MongoDB"""
    coll.delete_many({'url': url})
    coll.insert_one({'url': url, 'html': html})
    raw_html_dict['url'] = html

def retrieve_html(url, coll=raw_html_coll):
    """Retrieve page source for a URL from MongoDB"""
    if url in raw_html_dict:
        return raw_html_dict[url]
    retrieved_data = coll.find_one({'url': url})
    if retrieved_data:
        return retrieved_data.get('html')
    else:
        return None


def scrape_page(url, coll=raw_html_coll, browser=None):
    """Scrapes URL & stores raw HTML if it doesn't already exist in raw_html collection,
        returns HTML at end of function"""
    html = retrieve_html(url=url, coll=coll)
    if html:
        return html
    if browser is None:
        browser=Firefox()
    browser.get(url)
    time.sleep(5 + random.random() * 10)  # Wait 5-15 seconds
    #if browser.title.startswith('404'):
    #    return None
    html = browser.page_source
    store_html(url=url, html=html, coll=coll)
    return html
