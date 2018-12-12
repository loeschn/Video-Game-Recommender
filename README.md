# Video Game Recommender
### What game should I play?
  A major hobby of mine is playing video games, and just like any hobby as broad as this (watching movies or TV shows, reading books, listening to podcasts) I inevitably get to a point where I finish a game and don't know what to play next.  This is my attempt at solving that problem, through creating a recommender that is an ensemble of a content-based model, and one made through collaborative filtering.

## Methods

### Content-based Filtering
#### Finding the most similar game
  Using [IGDB's API](https://igdb.github.io/api/endpoints/) I began storing requests in a MongoDB collection, focusing mainly on the endpoints [Game](https://igdb.github.io/api/endpoints/game/) & [Platform](https://igdb.github.io/api/endpoints/platform/).  Starting with games only on the platform Playstation 4 (later expanding to include Xbox One & Nintendo Switch game titles) and stored all game information in a MongoDB collection.  The five features I was interested in from all this information were:
  1. Genres
  1. Keywords
  1. Themes
  1. Game Modes
  1. Player Perspective

  Each game had id tags for each of these categories.  There was no need to make requests as to what any of these ID tags were, when I was only interested in finding games also had the same ID tags.  I transferred the collection to a pandas data frame and made dummy columns for each ID tag in my collection & dropped all other columns.  Jaccard Similarity was used for determining most similar.

### Collaborative Filtering
Metacritic's website was used as the sole resource for creating my database used in my collaborative filtering model.  I used Selenium to open a browser and download the raw html of any page into a MongoDB collection.  From there I used Beautiful Soup to filter the username & score given from each review.
Every game on Metacritic's platform game page was scraped for reviews & stored in a collection.  The collection was then transferred to a Spark data frame.  Spark's own pipeline for transforming data frames into models, and I used their ALS (Alternating Least Squares Model).  Once the model was trained I extracted the item factor matrix.
I created a function that takes in a dictionary of game titles and scores (0-10) that would then return the top 5 highest predicted scores through `NumPy` and some `Pandas`.

### Upcoming Improvements:
* Make a model that uses both models in some aspect.  I have two approaches that I will try:
  * Use the content-based model as a solution to a Cold-Start that will give several recommendations that are similar to the one game provided, from there the ALS model can predict rating off of more than one user input.
  * Weight both models equally when scoring what the best games to be recommended are.
* Upscale everything:
  * Expand upon the platforms being used, increasing the total number of games to be considered.
  * Explore other popular websites where people leave game reviews and scrape those pages as well, increasing the total number of users and reviews.
* Create a website to deploy the model to.
