import media
import requests
import fresh_tomatoes


# Open Movie Database (OMDb) API call to fetch info about a particular movie
def get_movie(movie):
    r = requests.get('http://www.omdbapi.com/?t='+movie+'&y=&plot=short&r=json')  # noqa
    return r.json()  # converting response to a json format for convenience


# Creating 6 objects of the Movie class each of which contains a different
# movie passed to a Movie constructor as a parameter
inception = media.Movie(get_movie('inception'),
                        'https://www.youtube.com/watch?v=8hP9D6kZseM')
catch_me_if_you_can = media.Movie(get_movie('catch me if you can'),
                                  'https://www.youtube.com/watch?v=71rDQ7z4eFg')  # noqa
source_code = media.Movie(get_movie('source code'),
                          'https://www.youtube.com/watch?v=NkTrG-gpIzE')
pulp_fiction = media.Movie(get_movie('pulp fiction'),
                           'https://www.youtube.com/watch?v=s7EdQ4FqbhY')
fight_club = media.Movie(get_movie('fight club'),
                         'https://www.youtube.com/watch?v=SUXWAEX2jlg')
shawshank_redemption = media.Movie(get_movie('shawshank redemption'),
                                   'https://www.youtube.com/watch?v=6hB3S9bIaco')  # noqa

# Creating a tuple 'movies'. Tuple was chosen because it's immutable
# (in our usecase 'movies' is aslways static and doesn't change)
# as such it is more efficient than an array.
movies = (inception, catch_me_if_you_can, source_code, pulp_fiction,
          fight_club, shawshank_redemption)

# Open a page with movies in a browser
fresh_tomatoes.open_movies_page(movies)
