import pandas as pd
import numpy as np
from src.make_preference_matrix import make_preference_df
import pymongo
from fuzzywuzzy import process

mc = pymongo.MongoClient()
db =mc['game_recommender']
games=db['games']



df=make_preference_df()
item_arr=np.load('filtered_item_arr.npy')

game_titles = list(df.game_id.unique())

def get_game_ids(prefs={}):
    """Returns a list of the game IDs given the game title"""
    game_ids=[]
    for key in prefs:
        game_ids.append(int(df[df['game_id']==key].game_number.unique()))
    return game_ids


def make_prefernce_vector(prefs={}):
    """A user will give a dictionary of game_titles and scores for each,
    The function will return a vector of predicted scores for each game
    in the database"""

    scores=[]
    for key in prefs:
        scores.append(prefs[key])
    ratings=np.array(scores)


    game_ids=get_game_ids(prefs=prefs)
    user_item_arr = item_arr[game_ids]

    X, residuals, rank, s =np.linalg.lstsq(user_item_arr,
                                            ratings,
                                            rcond=None)
    new_factor_list = []
    for i in range(len(item_arr)):
        new_factor_list.append(np.dot(X, item_arr[i]))

    return np.array(new_factor_list)

def make_dict():
    d={}
    game=input("Game title: ")
    correct_title = process.extractOne(game, game_titles)[0]
    #if not games.find_one({'title': game}):
    #    return "Error: game not in database"
    score=input("Score: ")
    while score and game:
        d[correct_title]=int(score)
        game=input("Game title: ")
        correct_title = process.extractOne(game, game_titles)[0]
        #if not games.find_one({'title': game}):
        #    break
        score=input("Score: ")

    return d


def give_recommendation(prefs={}):
    """Returns the top 5 games with highest predicted score"""

    predicted_scores=make_prefernce_vector(prefs=prefs)
    game_ids = get_game_ids(prefs=prefs)


    predicted_scores = np.delete(predicted_scores, game_ids)

    best=[]
    for ind in predicted_scores.argsort()[-5:][::-1]:
        best.append(df[df['game_number']==ind]['game_id'].unique()[0])

    return best
