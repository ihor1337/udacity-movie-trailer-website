import webbrowser
import os
import re


# Styles and scripting for the page
main_page_head = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <title>Fresh Tomatoes!</title>
    <!-- Bootstrap 3 -->
    <link rel="stylesheet" href="https://netdna.bootstrapcdn.com/bootstrap/3.1.0/css/bootstrap.min.css">
    <link rel="stylesheet" href="https://netdna.bootstrapcdn.com/bootstrap/3.1.0/css/bootstrap-theme.min.css">
    <script src="http://code.jquery.com/jquery-1.10.1.min.js"></script>
    <script src="https://netdna.bootstrapcdn.com/bootstrap/3.1.0/js/bootstrap.min.js"></script>
    <style type="text/css" media="screen">
        body {
            padding-top: 80px;
        }
        #trailer .modal-dialog {
            margin-top: 200px;
            width: 640px;
            height: 480px;
        }
        .hanging-close {
            position: absolute;
            top: -12px;
            right: -12px;
            z-index: 9001;
        }
        #trailer-video {
            width: 100%;
            height: 100%;
        }
        .scale-media {
            padding-bottom: 56.25%;
            position: relative;
        }
        .scale-media iframe {
            border: none;
            height: 100%;
            position: absolute;
            width: 100%;
            left: 0;
            top: 0;
            background-color: white;
        }
        .left {
            float: left;
        }
        .poster{
            width: 20%;
            margin-right: 25px;
        }

        .movie-info{
            width: 75%;
        }
        .panel-body{
            background-color: #eeeeee;
        }
        ul li{
            line-height: 20px;
        }
        ul li p{
            line-height: 1.5;
        }
        a {
            color: inherit;
        }
        a:hover {
            color: #000000;
            text-decoration: underline;
        }
        .trailer{
            font-size: 18px;
            cursor: pointer;
        }

        .trailer:hover{
            color: #000000;
            text-decoration: underline;
        }

    </style>
    <script type="text/javascript" charset="utf-8">
        // Pause the video when the modal is closed
        $(document).on('click', '.hanging-close, .modal-backdrop, .modal', function (event) {
            // Remove the src so the player itself gets removed, as this is the only
            // reliable way to ensure the video stops playing in IE
            $("#trailer-video-container").empty();
        });
        // Start playing the video whenever the trailer modal is opened
        $(document).on('click', '.trailer', function (event) {
            var trailerYouTubeId = $(this).attr('data-trailer-youtube-id')
            var sourceUrl = 'http://www.youtube.com/embed/' + trailerYouTubeId + '?autoplay=1&html5=1';
            $("#trailer-video-container").empty().append($("<iframe></iframe>", {
              'id': 'trailer-video',
              'type': 'text-html',
              'src': sourceUrl,
              'frameborder': 0
            }));
        });
        // Animate in the movies when the page loads
        $(document).ready(function () {
          $('.movie').hide().first().show("fast", function showNext() {
            $(this).next("div").show("fast", showNext);
          });
        });
    </script>
</head>
'''


# The main page layout and title bar
main_page_content = '''
  <body>
    <!-- Trailer Video Modal -->
    <div class="modal" id="trailer">
      <div class="modal-dialog">
        <div class="modal-content">
          <a href="#" class="hanging-close" data-dismiss="modal" aria-hidden="true">
            <img src="https://lh5.ggpht.com/v4-628SilF0HtHuHdu5EzxD7WRqOrrTIDi_MhEG6_qkNtUK5Wg7KPkofp_VJoF7RS2LhxwEFCO1ICHZlc-o_=s0#w=24&h=24"/>
          </a>
          <div class="scale-media" id="trailer-video-container">
          </div>
        </div>
      </div>
    </div>
    <!-- Main Page Content -->
    <div class="container">
      <div class="navbar navbar-inverse navbar-fixed-top" role="navigation">
        <div class="container">
          <div class="navbar-header">
            <a class="navbar-brand" href="#">Fresh Tomatoes Movie Trailers</a>
          </div>
        </div>
      </div>
    </div>
    <div class="container">
      {movie_tiles}
    </div>
  </body>
</html>
'''


#A single movie entry html template
movie_tile_content = '''
<div class="col-md-12 movie">
    <div class="panel panel-info">
      <div class="panel-heading">
        <h3 class="panel-title">{movie_title}</h3>
      </div>
      <div class="panel-body">
        <div class="poster left">
            <img class="img-thumbnail" src="{poster_image_url}">
        </div>

        <div class="movie-info left">
            <a href="{imdb_link}" target="_blank"><h2 class="movie-title">{movie_title} </h2><em>({movie_rated})</em></a>
            <ul class="list-unstyled">
                <li><strong>Release date: </strong>{release_date}</li>
                <li><strong>Genre: </strong>{movie_genre}</li>
                <li><strong>Directed by: </strong>{movie_director}</li>
                <li><strong>Actors: </strong>{movie_actors}</li>
                <li><strong>IMDB: </strong><span>{imdb_rating} </span>({imdb_votes} votes)</li>
                <li><strong>Plot: </strong> <p>{movie_plot}</p></li>
            </ul>
            <strong class="trailer" data-trailer-youtube-id="{trailer_youtube_id}" data-toggle="modal" data-target="#trailer">
                <i class="glyphicon glyphicon-film"></i>
                <span> Watch a trailer</span>
            </strong>
        </div>
      </div>
    </div>
</div>
'''

def create_movie_tiles_content(movies):
    # The HTML content for this section of the page
    content = ''
    for movie in movies:
        # Extract the youtube ID from the url
        youtube_id_match = re.search(
            r'(?<=v=)[^&#]+', movie.trailer_youtube_url)
        youtube_id_match = youtube_id_match or re.search(
            r'(?<=be/)[^&#]+', movie.trailer_youtube_url)
        trailer_youtube_id = (youtube_id_match.group(0) if youtube_id_match
                              else None)

        # Append the tile for the movie with its content filled in
        content += movie_tile_content.format(
            movie_title=movie.title,
            poster_image_url=movie.poster_image_url,
            trailer_youtube_id=trailer_youtube_id,
            movie_plot = movie.storyline,
            movie_rated = movie.rated,
            release_date = movie.released,
            movie_genre = movie.genre,
            movie_director = movie.director,
            movie_actors = movie.actors,
            imdb_rating = movie.imdb_rating,
            imdb_votes = movie.imd_votes,
            imdb_link = movie.imdb_link
        )
    return content


def open_movies_page(movies):
    # Create or overwrite the output file
    output_file = open('fresh_tomatoes.html', 'w')

    # Replace the movie tiles placeholder generated content
    rendered_content = main_page_content.format(
        movie_tiles=create_movie_tiles_content(movies))

    # Output the file
    output_file.write(main_page_head + rendered_content)
    output_file.close()

    # open the output file in the browser (in a new tab, if possible)
    url = os.path.abspath(output_file.name)
    webbrowser.open('file://' + url, new=2)