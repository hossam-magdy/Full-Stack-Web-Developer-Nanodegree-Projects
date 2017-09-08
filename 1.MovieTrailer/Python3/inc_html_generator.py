# This file is to generate the html file.
# In lessons it is called "fresh_tomatoes",
# But this is an updated version

import webbrowser
import os
import re

# The full page layout, the only variable is "{movie_tiles}"
main_page_content = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <title>FSND Project: Movie Trailers</title>
    <!-- Bootstrap 4 alpha stylesheet -->
    <link rel="stylesheet" href="//maxcdn.bootstrapcdn.com/bootstrap/4.0.0-alpha.6/css/bootstrap.min.css">
    <style>
    #trailer-video-container {
        text-align: center;
    }
    #trailer-video-container iframe {
        top: 0; bottom: 0; left: 0; right: 0;
        width: 760px;
        height: 427px;
    }
    .movie-tile {
        display: none;
        margin: 10px auto 10px auto;
        width: 220px;
        height: 342px;
    }
    .movie-tile .movie-poster {
        position: absolute;
    }
    /*
        Used fade/alpha/opacity approach to show movie details instead of
        3D-180 degree rotation: to enable cross-browser design
    */
    .movie-tile .movie-content {
        padding: 2px;
        padding-top: 8%;
        opacity: 0;
        background-color: #fff;
        -webkit-transition: opacity 0.4s ease-in-out;
        -moz-transition: opacity 0.4s ease-in-out;
        -ms-transition: opacity 0.4s ease-in-out;
        -o-transition: opacity 0.4s ease-in-out;
    }
    .movie-tile.hovered .movie-content {
        opacity: 0.85;
    }
    .movie-tile .movie-poster img, .movie-tile .movie-content {
        border-radius: 15px;
        border: solid 1px rgba(0,0,0,0.5);
    }
    .movie-tile .movie-poster img, .movie-tile .movie-poster, .movie-tile .movie-content {
        width: inherit;
        height: inherit;
    }
    .hanging-close {
        display: block;
        color: #b00;
        font-weight: 900;        
        text-align: center;
        width: 24px;
        height: 24px;
        border-radius: 10px;
        background-color: white;
        position: absolute;
        top: -12px;
        right: -12px;
        z-index: 9001;
    }
    .hanging-close:hover {
        text-decoration: none;
    }
    </style>
</head>
<body>
    <!-- Main Page Content -->
    <div class="container">
        <nav class="navbar navbar-inverse bg-inverse">
          <a class="navbar-brand" href="#">FSND Project: Movie Trailers</a>
        </nav>
        <div class="row">
            <!-- Movies Tiles -->{movie_tiles}
        </div>
    </div>
    
    <!-- Trailer Video Modal -->
    <div class="modal fade" id="trailer" tabindex="-1">
        <div class="modal-dialog modal-lg" role="document">
            <div class="modal-content">
                <a href="#" class="hanging-close" data-dismiss="modal" aria-hidden="true">
                    <span aria-hidden="true">&times;</span>
                </a>
                <div class="modal-body" id="trailer-video-container"></div>
            </div>
        </div>
    </div>

    <!-- Load the JavaScript files: jQuery, Tether, Bootstrap4 -->
    <script src="//code.jquery.com/jquery-3.1.1.min.js"></script>
    <script src="//cdnjs.cloudflare.com/ajax/libs/tether/1.4.0/js/tether.min.js"></script>
    <script src="//maxcdn.bootstrapcdn.com/bootstrap/4.0.0-alpha.6/js/bootstrap.min.js"></script>

    <!-- Inline Javascript code for page initialization (assign event handlers, & show movies one by one) -->
    <script type="text/javascript" charset="utf-8">
        // Pause the video when the modal is closed
        $('#trailer').on('hidden.bs.modal', function (e) {
            $("#trailer-video-container").empty();
        });
        // Start playing the video whenever the trailer modal is opened
        $('#trailer').on('show.bs.modal', function (e) {
            var trailerYouTubeId = $(e.relatedTarget).attr('data-trailer-youtube-id');
            var sourceUrl = '//www.youtube.com/embed/' + trailerYouTubeId + '?autoplay=1&html5=1';
            $("#trailer-video-container").empty().append($("<iframe></iframe>", {
                'id': 'trailer-video',
                'type': 'text-html',
                'src': sourceUrl,
                'frameborder': 0
            }));
        });
        // Show/hide the movie details at mouse hover on poster
        $('.movie-tile').hover(function(){
            $(this).toggleClass('hovered');
        });
        // Animate in the movies when the page loads
        $(document).ready(function () {
            $('.movie-tile').first().show('fast', function showNext() {
                $(this).parent().next("div").find('.movie-tile').show("fast", showNext);
            });
        });
    </script>
</body>
</html>'''

# A single movie entry html template
movie_tile_content = '''
<div class="col-md-6 col-lg-4">
    <div class="movie-tile">
        <div class="movie-poster"><img src="{poster_image_url}"></div>
        <div class="movie-content text-center">
            <h4 class="movie-title">{movie_title}</h4>
            <button type="button" class="btn btn-secondary movie-show-trailer" data-trailer-youtube-id="{trailer_youtube_id}" data-toggle="modal" data-target="#trailer">Show Trailer</button>
            <p class="movie-storyline">{storyline}</p>
        </div>
    </div>
</div>'''

def create_movie_tiles_content(movies):
    # The HTML content for this section of the page
    content = ''
    for movie in movies:
        # Extract the youtube ID from the url
        youtube_id_match = re.search(
            # for regular youtube urls : https://www.youtube.com/watch?v=sUkZFetWYY0
            r'(?<=v=)[^&#]+', movie.trailer_youtube_url) or re.search(
            # for short youtu.be urls : https://youtu.be/sUkZFetWYY0
            r'(?<=be/)[^&#]+', movie.trailer_youtube_url)
        trailer_youtube_id = youtube_id_match.group(0) if youtube_id_match else None

        # Append the tile for the movie with its content filled in
        content += movie_tile_content.format(
            movie_title=movie.title,
            poster_image_url=movie.poster_image_url,
            trailer_youtube_id=trailer_youtube_id,
            storyline=movie.storyline
        )
    return content


def create_movies_html_page(movies, filename):
    # Create or overwrite the output file
    #(writes in UTF-8 encoding for special chars)
    # for any special characters in movie titles (like: WALL·E)
    output_file = open(filename, 'w', -1, 'utf-8')

    # Replace the placeholder for the movie tiles with the actual dynamically generated content
    # used .replace() instead of .format() as the page content string has {} in style & script
    # which lead to error in case of using .format()
    rendered_content = main_page_content.replace('{movie_tiles}',
                                                 create_movie_tiles_content(movies)
                                                 )

    # Output the file
    output_file.write(rendered_content)
    output_file.close()

    # Return the full path of the created file
    return 'file://' + os.path.abspath(output_file.name)


# Open the output file in the browser
def open_movies_page(movies, filename = 'FSND_Project_MovieTrailers.html'):
    page_full_path = create_movies_html_page(movies, filename)
    webbrowser.open(page_full_path, new=2) # open in a new tab, if possible

