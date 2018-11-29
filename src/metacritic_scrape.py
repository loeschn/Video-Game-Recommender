import requests
from selenium.webdriver import (Chrome, Firefox)

def get_users_scores(title=""):
    """Returns list of  all users who reviewed a game, and a list of scores for the game"""
    browser = Firefox()

    title = title.lower()
    title=title.replace(" ", "-")

    scores=[]
    users=[]
    
    for i in range(100):
        url= f"https://www.metacritic.com/game/playstation-4/{title}/user-reviews?page={i}"
        browser.get(url)
        reviews = browser.find_elements_by_css_selector('li.user_review')

        for i in range(len(reviews)):
            scores.append(int((reviews[i].text).split('\n')[2]))
            users.append((reviews[i].text).split('\n')[0])

        if len(reviews)==0:
            break

    return scores, users
