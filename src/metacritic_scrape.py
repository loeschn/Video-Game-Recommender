import requests
from selenium.webdriver import Firefox
from .pymongo_functions import scrape_page
from bs4 import BeautifulSoup


def clean_title(game=""):
    """cleaning the title of the game as given from the mongodb,
        to something compatibible for metacritic"""
    empty=[':', ";", ".", ",", "'", "@", "*", "#", "/", "＠"]
    space=["&", "_", " - ", " "]

    game=game.lower()

    for element in empty:
        game=game.replace(element, "")

    for element in space:
        game=game.replace(element, "-")

    return game


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
