import pandas as pd
import pymongo
from .metacritic_scrape import scrape_game_page
from selenium.webdriver import Firefox

mc = pymongo.MongoClient()
db = mc['ps4_game_data']
games = db['games']


def get_all_users(db=games):
    users=[]
    games_dict={}
    df = pd.DataFrame(list(db.find()))

    game_titles = list(df.name)
    browser=Firefox()
    for game in game_titles[:50]:
        games_dict[game], game_users = scrape_game_page(title=game, browser=browser)

        for user in game_users:
            if user not in users:
                users.append(user)

    return games_dict, users
