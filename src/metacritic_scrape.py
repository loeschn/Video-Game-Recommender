import requests
from selenium.webdriver import (Chrome, Firefox)

def scrape_game_page(title=""):
    """Returns list of  all users who reviewed a game, and a list of scores for the game"""
    browser = Firefox()

    title = title.lower()
    title=title.replace(" ", "-")

    #scores=[]
    users=[]
    scores_dict={}

    for i in range(100):
        url= f"https://www.metacritic.com/game/playstation-4/{title}/user-reviews?page={i}"
        browser.get(url)
        reviews = browser.find_elements_by_css_selector('li.user_review')

        for i in range(len(reviews)):
            #scores.append(int((reviews[i].text).split('\n')[2]))
            split = (reviews[i].text).split('\n')
            users.append(split[0])
            scores_dict[split[0]]=int(split[2])

        if len(reviews)==0:
            break

    return scores_dict, users

def scrape_user_page(username=""):
    "Returns list of all games a user has reviewed, and what score they gave the game"


    for i in range(100):
        url= f"https://www.metacritic.com/user/{username}?page={i}"
        browser.get(url)
