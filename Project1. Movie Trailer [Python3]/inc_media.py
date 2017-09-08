class Movie:
    # Reminder: the following (""") documentaion can be accessed via:
    # media.Movie.__doc__
    """ This class provides a way to store movie-related information """

    # This is a CLASS-Variable (a variable whose value is same for all objects)
    # as it doesn't start with self.* so its is not object specific
    VALID_RATINGS = ["G", "PG", "PG-13", "R"]


    # The method that initializes the instance
    def __init__(self, title, story, poster_url, trailer_url):
        # Set the instance variables
        self.title = title
        self.storyline = story
        self.poster_image_url = poster_url
        self.trailer_youtube_url = trailer_url


    # A method that opens the movie trailer in web browser
    def show_trailer(self):
        # Import the webbrowser module only when needed
        import webbrowser

        # Open the trailer in web browser
        webbrowser.open(self.trailer_youtube_url)

