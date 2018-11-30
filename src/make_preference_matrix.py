import pandas as pd
import pymongo
from .metacritic_scrape import scrape_game_page
from .pandas_functions import clean_df
from selenium.webdriver import Firefox
import random
import time

mc = pymongo.MongoClient()
db = mc['ps4_game_data']
games = db['games']


def get_all_users(db=games):
    #users=[]
    games_dict={}

    df = pd.DataFrame(list(db.find()))
    df =clean_df(df=df)


    game_titles = list(df.name)
    browser=Firefox()
    for game in game_titles:
        games_dict[game] = scrape_game_page(title=game, browser=browser)
        time.sleep(random.randint(0,5))
        #for user in game_users:
        #    if user not in users:
        #        users.append(user)

    return games_dict#, users
