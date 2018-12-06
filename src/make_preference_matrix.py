import pandas as pd
import pymongo
from .metacritic_scrape import scrape_game_page
from .pandas_functions import clean_df
from selenium.webdriver import Firefox
import random
import time

mc = pymongo.MongoClient()
db =mc['game_recommender']
reviews_coll = db['reviews']
games=db['games']

#omc=pymongo.MongoClient()
#cb = omc['ps4_game_data']
#games = cb['games']

def flatten_game_dict(game_dict):
    """Take a dictionary of dictionaries & flatten it"""
    for (game_id, user_score_dict) in game_dict.items():
        for (user_id, score) in user_score_dict.items():
            yield {'game_id': game_id, 'user_id': user_id, 'score': score}

def store_all_users(db=games):
    """Take raw_html from a game's user review page, and store the game, username, & score
    as an entry in reviews collection"""
    games_dict={}

    df = pd.DataFrame(list(db.find()))
    #df =clean_df(df=df)

    game_titles = list(df.title)
    browser=Firefox()
    for game in game_titles:
        if scrape_game_page(title=game, browser=browser)=={}:
            continue
        games_dict[game] = scrape_game_page(title=game, browser=browser)

    flattened=flatten_game_dict(game_dict=games_dict)
    for review in flattened:
        if reviews_coll.count_documents({'title': title}) == 0:
            reviews_coll.insert_one(review)

def make_preference_df(db=reviews):
    """Go from all entries in reviews collection, to pandas dataframe, then pivot it to make
    preference matrix"""
    df=pd.DataFrame(list(db.find()))
    df=df.pivot(index='user_id', columns='game_id', values='score' )
    return df
