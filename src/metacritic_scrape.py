import requests
from selenium.webdriver import Firefox

def clean_title(title=""):
    """cleaning the title of the game as given from the mongodb,
        to something compatibible for metacritic"""
    empty=[':', ";", ".", ",", "'", "@", "*", "#", "/", "＠"]
    space=["&", "_", " - ", " "]

    title=title.lower()
"""This is all cleaning for specific games I found problematic formatting into a metacritic url
    I'm commenting this out for now but will probably not use it going forward
    
    title=title.replace("\ufeff", "")
    title=title.replace("Final Fantasy XIV: A Realm Reborn", "final-fantasy-xiv-online-a-realm-reborn")
    title=title.replace("Warriors 8", "warriors-8-empires")
    title=title.replace("Guilty Gear Xrd", "guilty-gear-xrd--sign-")
    title=title.replace("Runner2", "bittrip-presentsrunner2")
    title=title.replace("All Points Bulletin", "APB")
    title=title.replace("Radial-G : Racing Revolved", "radial-g-racing-revolved")
    title=title.replace(" : ", "-")
    title=title.replace("Û", "u")
    title=title.replace("Oddworld: New 'n' Tasty", "oddworld-abes-oddysee---new-n-tasty")
    title=title.replace("2+", "2-+")
    title=title.replace(" - V", "---v")
    title=title.replace(" FIA World Rally Championship", "")
    title=title.replace("ö", "o")
    title=title.replace("Yorbie - Episode 1: Payback's A Bolt", "yorbie---episode-one-paybacks-a-bolt")
    title=title.replace("Everybody's Tennis", "hot-shots-tennis")
    title=title.replace("Score Edition", "edition")
    title=title.replace("the Flood", "the-flood-complete-edition")
"""
    for element in empty:
        title=title.replace(element, "")

    for element in space:
        title=title.replace(element, "-")

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
