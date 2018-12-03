import pandas as pd
import pymongo
from .metacritic_scrape import scrape_game_page
from .pandas_functions import clean_df
from selenium.webdriver import Firefox
import random
import time

mc = pymongo.MongoClient()
db =mc['game_recommender']
omc=pymongo.MongoClient()
cb = omc['ps4_game_data']
games = cb['games']


def get_all_users(db=games):
    games_dict={}

    df = pd.DataFrame(list(db.find()))
    df =clean_df(df=df)


    game_titles = list(df.name)
    browser=Firefox()
    for game in game_titles:
        games_dict[game] = scrape_game_page(title=game, browser=browser)
        
    return games_dict
