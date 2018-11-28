import requests
from selenium.webdriver import (Chrome, Firefox)

def get_users_scores(title=""):
    """Returns 1 page of user review scoresfor a given title"""
    browser = Firefox()

    title = title.lower()
    title=title.replace(" ", "-")

    url= f"https://www.metacritic.com/game/playstation-4/{title}/user-reviews"
    browser.get(url)
    reviews = browser.find_elements_by_css_selector('li.user_review')

    scores=[]
    users=[]

    for i in range(len(reviews)):
        scores.append(int((reviews[i].text).split('\n')[2]))
        users.append((reviews[i].text).split('\n')[0])
    return scores, users
