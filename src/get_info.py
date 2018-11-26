

def get_game_info(key="name", value=""):
    """Returns all game information for game given the key & value in the game dict"""
    return games.find_one({key : value})
