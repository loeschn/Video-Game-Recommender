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

omc=pymongo.MongoClient()
cb = omc['ps4_game_data']
games = cb['games']

def flatten_game_dict(game_dict):
    for (game_id, user_score_dict) in game_dict.items():
        for (user_id, score) in user_score_dict.items():
            yield {'game_id': game_id, 'user_id': user_id, 'score': score}

def get_all_users(db=games):
    games_dict={}

    df = pd.DataFrame(list(db.find()))
    df =clean_df(df=df)


    game_titles = list(df.name)
    browser=Firefox()
    for game in game_titles:
        if scrape_game_page(title=game, browser=browser)=={}:
            continue
        games_dict[game] = scrape_game_page(title=game, browser=browser)

    flattened=flatten_game_dict(game_dict=games_dict)
    for review in flattened:
        reviews_coll.insert_one(review)

def make_preference_df(db=reviews_coll):
    df=pd.Dataframe(list(db.find()))
    df=df.pivot(index='username', columns='game_id', values='score' )
    return df
