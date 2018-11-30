import pymongo


mc = pymongo.MongoClient()
db = mc['ps4_game_data']
games = db['games']
raw_html_coll = db['raw_html']



def get_game_info(key="name", value=""):
    """Returns all game information for game given the key & value in the game dict"""
    return games.find_one({key : value})

def store_html(url, html, coll=raw_html_coll):
    """"Store raw HTML in MongoDB"""
    coll.update_one(
        {'url': url, {'url': url, 'html': html} }, upsert=True
    )

def retrieve_html(url, coll=raw_html_coll):
"""Retrieve page source for a URL from MongoDB"""
    retrieved_data = coll.find_one({'url': url})
    if retrieved_data:
        return retrieved_data.get('html')
    else:
        return None


def scrape_page(url, coll=raw_html_coll):
    html = retrieve_html(url=url, coll=coll):
    if html:
        return html
    browser.get(url)
    time.sleep(5 + random.random() * 10)  # Wait 5-15 seconds
    if browser.title.startswith('404'):
        return None
    html = browser.page_source
    store_html(url=url, html=html, coll=coll)
    return html
