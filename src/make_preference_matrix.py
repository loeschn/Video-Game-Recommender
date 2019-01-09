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

def store_all_users(coll=games):
    """Take raw_html from a game's user review page, and store the game, username, & score
    as an entry in reviews collection"""
    games_dict={}
    print('loading collection')
    df = pd.DataFrame(list(coll.find()))
    #df =clean_df(df=df)

    game_titles = list(df.title)
    browser=Firefox()
    print('making games dict')
    for game in game_titles:
        result= scrape_game_page(title=game, browser=browser)
        if not result:
            continue
        games_dict[game] = result
    print('finding existing reviews')
    existing_game_reviews=set((r['game_id'], r['user_id'])
                                for r in reviews_coll.find())
    print('flattening')
    flattened=flatten_game_dict(game_dict=games_dict)
    for review in flattened:
        game_id = review['game_id']
        user_id = review['user_id']
        if (game_id, user_id) not in existing_game_reviews:
            reviews_coll.insert_one(review)

def make_preference_df(coll=reviews_coll):
    """Go from all entries in reviews collection, to pandas dataframe"""
    df=pd.DataFrame(list(coll.find()))

    """Creating columns that have the count of reviews a user has given
    & reviews a game has recieved"""
    user_group_df = pd.DataFrame(df.groupby('user_id').size(),
                              columns=['num_username_reviews'])

    game_group_df = pd.DataFrame(df.groupby('game_id').size(),
                              columns=['num_game_reviews'])

    df = df.join(user_group_df, on='user_id')
    df = df.join(game_group_df, on='game_id')

    """Filtering out all users who gave less than 17 reviews,
    determined by evaluating RMSE in Pyspark_ALS.ipynb"""
    df = df[df.num_username_reviews>=17]

    """Set of unique user & game IDs"""
    users=set(df['user_id'])
    games=set(df['game_id'])

    """Zipping a number to each unique user & game ID aka actually making IDs"""
    game_id_lookup = dict(zip(games, range(len(games))))
    user_id_lookup = dict(zip(users, range(len(users))))

    df['game_number']=df['game_id'].apply(game_id_lookup.get)
    df['user_number']=df['user_id'].apply(user_id_lookup.get)
    #df=df.pivot(index='user_number', columns='game_number', values='score' )
    return df
