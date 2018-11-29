import requests
from selenium.webdriver import Firefox

def clean_title(title=""):
    """cleaning the title of the game as given from the mongodb,
        to something compatibible for metacritic"""
    empty=[':', ";", ".", ",", "'", "@", "*", "#", "!", "/"]
    space=["&", "_"]

    title=title.lower()

    title=title.replace("\ufeff", "")

    for element in empty:
        title=title.replace(element, "")

    for element in space:
        title=title.replace(element, " ")

    title=title.replace(" - ", "-")
    title=title.replace(" ", "-")

    return title

def scrape_game_page(platform="playstation-4", title=""):
    """Returns list of  all users who reviewed a game, and a list of scores for the game"""
    browser = Firefox()

    game=clean_title(title)

    users=[]
    scores_dict={}

    for i in range(100):
        url= f"https://www.metacritic.com/game/{platform}/{game}/user-reviews?page={i}"
        browser.get(url)
        reviews = browser.find_elements_by_css_selector('li.user_review')

        for i in range(len(reviews)):
            split = (reviews[i].text).split('\n')
            users.append(split[0])
            scores_dict[split[0]]=int(split[2])

        if len(reviews)==0:
            break

    return scores_dict, users

def scrape_user_page(username=""):
    "Returns list of all games a user has reviewed, and what score they gave the game"
    browser = Firefox()
    title_dict={}

    for i in range(100):
        url= f"https://www.metacritic.com/user/{username}?page={i}"
        browser.get(url)
        reviews = browser.find_elements_by_css_selector('li.user_review')

        for i in range(len(reviews)):
            split = (reviews[i].text).split('\n')
            title_dict[split[0]] = int(split[3])

        if len(reviews)==0:
            break

    return title_dict
