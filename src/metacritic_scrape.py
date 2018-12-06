from selenium.webdriver import Firefox
from .pymongo_functions import scrape_page
from bs4 import BeautifulSoup
import pymongo

mc = pymongo.MongoClient()
db = mc['game_recommender']
games_coll = db['games']

def store_game_title(title, games_coll=games_coll):
    """Add a new title to the games collection."""
    if games_coll.count_documents({'title': title}) == 0:
        games_coll.insert_one({'title': title})

def clean_title(game=""):
    """cleaning the title of the game to something compatibible for metacritic URL"""
    empty=[':', ";", ".", ",", "'", "@", "*", "#", "/", "＠"]
    space=["&", "_", " "]

    game=game.lower()

    for element in empty:
        game=game.replace(element, "")

    for element in space:
        game=game.replace(element, "-")

    return game

def make_game_db(platform='ps4', browser=None):
    """Scrape platform game page for all titles on metacritic"""
    if browser is None:
        browser = Firefox()
    max_pages=9
    for i in range(max_pages):
        url=f'https://www.metacritic.com/browse/games/release-date/available/{platform}/metascore?page={i}'
        html=scrape_page(url=url, browser=browser)
        soup=BeautifulSoup(html, 'html.parser')
        titles=soup.select('div.basic_stat.product_title')
        for game in titles:
            plain=game.text
            title= (" ".join(plain.split()))
            store_game_title(title=title)



def scrape_game_page(title="", browser=None, platform="playstation-4"):
    """Returns a dictionary for a game in the form:
        game_title[username]=user_score"""
    if browser is None:
        browser = Firefox()

    game_title=clean_title(game=title)
    scores_dict={}

    for i in range(100):
        url= f"https://www.metacritic.com/game/{platform}/{game_title}/user-reviews?page={i}"
        html = scrape_page(url=url, browser=browser)
        if html is None:
            return None
        soup=BeautifulSoup(html, 'html.parser')
        reviews = soup.select('li.user_review')

        for i in range(len(reviews)):
            split = (reviews[i].text).split('\n')
            scores_dict[split[7]]=int(split[12])

        if len(reviews)==0:
            break

    return  scores_dict

def scrape_user_page(username=""):
    "Returns list of all games a user has reviewed, and what score they gave the game"
    browser = Firefox()
    title_dict={}

    for i in range(100):
        url= f"https://www.metacritic.com/user/{username}?page={i}"
        html = scrape_page(url=url)
        soup=BeautifulSoup(html, 'html.parser')
        reviews = soup.select('li.user_review')

        for i in range(len(reviews)):
            split = (reviews[i].text).split('\n')
            title_dict[split[7]] = int(split[12])

        if len(reviews)==0:
            break

    return title_dict
