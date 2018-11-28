import pymongo
import pandas as pd
import numpy as np

mc = pymongo.MongoClient()
db = mc['ps4_game_data']
games = db['games']

def get_game_info(key="name", value=""):
    """Returns all game information for game given the key & value in the game dict"""
    return games.find_one({key : value})

def make_id_list(column):
    """Making a list of unique ids in a given column"""
    id_list=[]
    for item in column:
        if type(item)==list:
            for entry in item:
                if entry not in id_list:
                    id_list.append(entry)
    (id_list.sort())
    return id_list

def is_val_in_col(column, i):
    if type(column)!=list:
        return 0
    elif i in column:
        return 1
    else:
        return 0


def clean_df(db=games):
    df = pd.DataFrame(list(db.find()))

    useful_columns = [ 'player_perspectives',
                        'game_modes',
                        'themes',
                        'genres']

    """Filling in the nans"""
    for col in useful_columns:
        df[col].fillna(0)

    """Dummifying the useful_columns"""
    for column in useful_columns:
        for i in make_id_list(df[column]):
            df[f'{column}_{i}'] = df[column].apply(lambda col: is_val_in_col(col, i))

    """Dropping columns to avoid games that are very similar:
    Category = 1 = DLC/Add-On
    Category = 2 = Expansion
    Category = 3 = Bundle
    Dropping any game that has a parent version:
    i.e. Overwatch Legendary Edition vs just plain Overwatch"""
    df = df.drop(df[df.category == 3].index)
    df = df.drop(df[df.category==2].index)
    df = df.drop(df[df.category==1].index)
    df = (df[df.version_parent.isnull()])

    """Making a similarity dataframe with only the dummy columns & the name"""
    similarity_df = df.iloc[:,53:]
    similarity_df['name'] = df['name']

    return similarity_df



def find_most_similar(title="", db=games):

    similarity_df = clean_df(db=games)
    sim_matrix = (similarity_df.values)[:,:-1]

    target = (similarity_df[similarity_df.name == title].values)[0]
    jaccard_scores=[]

    for i in range(len(sim_matrix)):
        jaccard_scores.append( (sim_matrix[i] & target[:-1]).sum() /
                               (sim_matrix[i] | target[:-1]).sum())


    idx =  np.argsort(-(np.array(jaccard_scores)))[1]

    return similarity_df.iloc[idx,:]['name']
