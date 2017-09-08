# Use only Python3
import sys
if sys.version_info[0] != 3:
    print('Requires Python 3')
    sys.exit()

# Import required modules with simplified alias naming
import inc_html_generator as html_generator  # was "fresh_tomatoes"
import inc_grab_movie_data as grab_movie_data

# Array of "movie title" or ["movie title", YEAR]
movies = [
    ['WALL-E', 2008],
    ['Up', 2009],
    'Braveheart',
    'Inside Out',
    'The Pursuit of Happyness',
    'The Martian',
    'Warrior',
    '127 Hours',
    ['The Dark Knight', 2008],
    ['The Dark Knight', 2012],
    ]

# Create movie-instances of favorite movies
movies_instances = grab_movie_data.movie_titles_to_instances(movies)
html_generator.open_movies_page(movies_instances,
                                'FSND_Project_MovieTrailers.html')

