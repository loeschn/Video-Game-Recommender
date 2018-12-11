# Video Game Recommender
### What game should I play?



## Methods

### Content-based Filtering
#### Finding the most similar game
  Using [IGDB's API](https://igdb.github.io/api/endpoints/) I began storing requests in a MongoDB, focusing mainly on the endpoints [Game](https://igdb.github.io/api/endpoints/game/) & [Platform](https://igdb.github.io/api/endpoints/platform/).  Starting with games only on the platform Playstation 4 (later expanding to include Xbox One & Nintendo Switch game titles) and stored all game information in a MongoDB collection.  The four features I was interested in from all this information were:
  1. Genres
  1. Keywords
  1. Themes
  1. Game Modes
Each game had id tags for each of these categories.  There was no need to make requests as to what any of these ID tags were, when I was only interested in finding games that are similar.  I transfered the collection to a pandas dataframe and made dummy columns for each ID tag in my collection & dropped all other columns.  Jaccard Similarity was used for determining most similar.  

### Collaborative Filtering
Metacritic's website was used as the sole resource for creating my database used in my collaborative filtering model.  I used Selenium to open a browser and download the raw html of any page into a MongoDB.  From there I used Beautiful Soup to filter the username & score given from each review.
