# Use only Python2
import sys
if sys.version_info[0] != 2:
    print('Requires Python 2')
    sys.exit()

# Import required modules
import fresh_tomatoes
import media

# Array of Movie-objects
movies = [  media.Movie('WALL-E (2008)',
                        'In the distant future, a small waste-collecting'\
                        ' robot inadvertently embarks on a space journey'\
                        ' that will ultimately decide the fate of mankind.',
                        'https://images-na.ssl-images-amazon.com/images/M/'\
                        'MV5BMjExMTg5OTU0NF5BMl5BanBnXkFtZTcwMjMxMzMzMw@@.'\
                        '_V1_SY1000_CR0,0,674,1000_AL_.jpg',
                        'https://www.youtube.com/watch?v=alIq_wG9FNk'),
            media.Movie('Inside Out (2015)',
                        'After young Riley is uprooted from her Midwest life'\
                        ' and moved to San Francisco, her emotions - Joy,'\
                        ' Fear, Anger, Disgust and Sadness - conflict on how'\
                        ' best to navigate a new city, house, and school.',
                        'https://images-na.ssl-images-amazon.com/images/M/MV'\
                        '5BOTgxMDQwMDk0OF5BMl5BanBnXkFtZTgwNjU5OTg2NDE@._V1_'\
                        'SY1000_CR0,0,674,1000_AL_.jpg',
                        'https://www.youtube.com/watch?v=WIDYqBMFzfg'),
            media.Movie('The Martian (2015)',
                        'An astronaut becomes stranded on Mars after his'\
                        ' team assume him dead, and must rely on his'\
                        ' ingenuity to find a way to signal to Earth that'\
                        ' he is alive.',
                        'http://t2.gstatic.com/images?q=tbn:ANd9GcTkKPZ7EI'\
                        'OafEsemyn6zTIDeGYthKC_Okgxi1eX6diuOT3xKWXQ',
                        'https://www.youtube.com/watch?v=ej3ioOneTy8'),
            media.Movie('Warrior (2011)',
                      'The youngest son of an alcoholic former boxer returns'\
                        ' home, where he\'s trained by his father for'\
                        ' competition in a mixed martial arts tournament -'\
                        ' a path that puts the fighter on a collision course'\
                        ' with his estranged, older brother.',
                      'https://images-na.ssl-images-amazon.com/images/M/MV5B'\
                        'MTk4ODk5MTMyNV5BMl5BanBnXkFtZTcwMDMyNTg0Ng@@._V1_SY'\
                        '1000_CR0,0,648,1000_AL_.jpg',
                      'https://www.youtube.com/watch?v=kY7HcUACs58'),
            media.Movie('127 Hours (2010)',
                        'An adventurous mountain climber becomes trapped'\
                        ' under a boulder while canyoneering alone near'\
                        ' Moab, Utah and resorts to desperate measures in'\
                        ' order to survive.',
                        'https://images-na.ssl-images-amazon.com/images/M/'\
                        'MV5BMTc2NjMzOTE3Ml5BMl5BanBnXkFtZTcwMDE0OTc5Mw@@.'\
                        '_V1_SY1000_CR0,0,675,1000_AL_.jpg',
                        'https://www.youtube.com/watch?v=OlhLOWTnVoQ'),
            media.Movie('Fury (2014)',
                        'A grizzled tank commander makes tough decisions as'\
                        ' he and his crew fight their way across Germany in'\
                        ' April, 1945.',
                        'https://images-na.ssl-images-amazon.com/images/M/'\
                        'MV5BMjA4MDU0NTUyN15BMl5BanBnXkFtZTgwMzQxMzY4MjE@.'\
                        '_V1_SY1000_CR0,0,674,1000_AL_.jpg',
                        'https://www.youtube.com/watch?v=ej3ioOneTy8')
            ]

fresh_tomatoes.open_movies_page(movies, '_FSND_Project_MovieTrailers_.html')

