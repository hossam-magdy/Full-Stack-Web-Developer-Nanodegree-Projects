# for class Movie
import inc_media as media
# for urllib.parse.quote (as urlencode in PHP)
import urllib.parse
# for urllib.request.urlopen
import urllib.request
# for json.loads (parses/decodes json string)
import json
import ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

# Function that sends a GET request & return the response
def get_json_request(url):
    try:
        conn = urllib.request.urlopen(url, context=ctx)
        response = conn.read().decode('utf-8')
        #print(response)
        #sys.exit()
        try:
            #print(response)
            response = json.loads(response)
            #from pprint import pprint     #print(response)
            conn.close()
            #sys.exit()
            return response
        #except:# ValueError, e:
        except Exception as e:
            print("ERROR decoding JSON: (" + type(e).__name__ + "); "\
                  "url: " + url + "; " + response)
    except urllib.error.HTTPError as e:
        print("ERROR: {urllib.error.HTTPError}: " + str(e.code) +
              "; url : " + url)
    except Exception as e:
        print("ERROR: (" + type(e).__name__ + "); url: " + url + ";")
    return ""

"""
Function that returns List/Array of Movie instances (with full data)
from List/Array containing only movie titles and Year (optional)
Uses:
- http://www.omdbapi.com/?t=The%20Martian&y=2015&r=json
- https://www.googleapis.com/youtube/v3/search?order=relevance
          &maxResults=1&part=snippet&key=****&q=The%20Martian%202015%20Trailer
  - https://developers.google.com/youtube/v3/docs/search/list#q
  - https://console.developers.google.com/apis/api/youtube/overview
Input: movies=['WALL-E', ['The Dark Knight', 2008], ['The Dark Knight', 2012]]
Output: movies=[media.Movie(...), media.Movie(...), media.Movie(...)]
"""
def movie_titles_to_instances(movies):
    print("Please wait ... (grabbing movies info via API's)")

    # API key to use Youtube API v3
    youtube_API_key = "AIzaSyDEtuy2AtiN1M3cjO3uPPuml7DRdHirJgs"

    # Array/List should be filled with instances of media.Movie(...)
    movies_instances = []
    for i,movie in enumerate(movies):
        # Print current progress as requests may take some time
        print("({}/{}): {}".format(
            str(i+1),
            str(len(movies)),
            str(movie)
            ))
            # OMDB_API: prepare url
        if type(movie) is list and len(movie)==2:  # Title & Year
            url_ombdAPI = ("http://www.omdbapi.com/?r=json&t="+
                urllib.parse.quote(str(movie[0]))+
                "&y="+str(movie[1]) )
        else:
             url_ombdAPI = ("http://www.omdbapi.com/?r=json&t="+
                 urllib.parse.quote(str(movie)) )

        # OMDB_API: Send request & parse the json response
        response_ombdAPI = get_json_request(url_ombdAPI)

        # Youtube_API_v3: prepare url
        url_youtubeAPI = "https://www.googleapis.com/youtube/v3/search?"\
                         "order=relevance&maxResults=1&part=snippet&"\
                         "key={}&q={}%20{}%20Trailer".format(
            youtube_API_key,
            urllib.parse.quote(response_ombdAPI['Title']),
            urllib.parse.quote(str(response_ombdAPI['Year']))
            )

        # Youtube_API_v3: Send request & parse the json response
        response_youtubeAPI = get_json_request(url_youtubeAPI)
            
        try:
            # Append this instance to the instances array
            movies_instances.append(
                media.Movie(
                    # Title = Movie Title (Year)
                    "{} ({})".format(
                        #html.escape(response_ombdAPI['Title']),
                        response_ombdAPI['Title'],
                        str(response_ombdAPI['Year'])
                        ),
                    # Short plot
                    response_ombdAPI['Plot'],
                    # Poster URL
                    response_ombdAPI['Poster'],
                    # Trailer URL
                    "https://www.youtube.com/watch?v={}".format(
                        response_youtubeAPI['items'][0]['id']['videoId'])
                    )
                )

        except Exception as e:
            print("Failed to get data for: (" + type(e).__name__ + ") {}".format(str(movie)))
        # Just for debugging
        #print(movies_instances)

    print("Grabbing info finished.")
    return movies_instances

