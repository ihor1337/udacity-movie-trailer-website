import webbrowser


class Movie:
    # defining an init function and initialising class properties with a fetched from API data
    def __init__(self, movie, trailer):
        self.title = movie['Title']
        self.storyline = movie['Plot']
        self.poster_image_url = movie['Poster']
        self.trailer_youtube_url = trailer
        self.rated = movie['Rated']
        self.released = movie['Released']
        self.genre = movie['Genre']
        self.director = movie['Director']
        self.actors = movie['Actors']
        self.imdb_rating = movie['imdbRating']
        self.imd_votes = movie['imdbVotes']
        self.imdb_link = 'http://www.imdb.com/title/'+movie['imdbID']