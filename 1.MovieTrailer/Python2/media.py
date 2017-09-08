import webbrowser

class Movie:
    """ This class provides a way to store movie-related information """

    # This is a CLASS-Variable (a variable whose value is same for all objects)
    # as it doesn't start with self.* so its is not object specific
    VALID_RATINGS = ["G", "PG", "PG-13", "R"]
    
    def __init__(self, title, story, poster_url, trailer_url):
        self.title = title
        self.storyline = story
        self.poster_image_url = poster_url
        self.trailer_youtube_url = trailer_url

    def show_trailer(self):
        webbrowser.open(self.trailer_youtube_url)
