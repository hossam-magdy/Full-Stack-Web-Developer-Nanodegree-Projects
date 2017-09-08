import httplib2
import json

def getGeoLocation(inputStr):
    google_api_key = "AIzaSyAdxNWi43am-8cDATTLnVW4eBK-NhD9m0U"
    locationStr = inputStr.replace(" ", "+")
    url = "https://maps.googleapis.com/maps/api/geocode/json?key={}&address={}".format(google_api_key, locationStr)
    h = httplib2.Http()
    response, content = h.request(url, "GET")
    result = json.loads(content)
    lat = result["results"][0]["geometry"]["location"]["lat"]
    lng = result["results"][0]["geometry"]["location"]["lng"]
    #print lat, lng
    #print content
    return [lat, lng]


if __name__ == '__main__':
    getGeoLocation("Cairo")
    