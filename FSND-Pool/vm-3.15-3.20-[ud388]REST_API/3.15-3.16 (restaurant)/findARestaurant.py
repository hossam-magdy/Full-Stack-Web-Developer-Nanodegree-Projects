from geocode import getGeoLocation
import json
import httplib2

import sys
import codecs
sys.stdout = codecs.getwriter('utf8')(sys.stdout)
sys.stderr = codecs.getwriter('utf8')(sys.stderr)

#google_api_key = "PASTE_YOUR_ID_HERE"
foursquare_client_id = "0UK5OMAR5R4XHPCONM3NE1KYGYV4A1M25UI32FZTY2GTWDRD"
foursquare_client_secret = "JNSRTD2VV12OGADYVU2JKP3SNO253DHIZ2JW0V411BCVJA4K"

def findARestaurant(mealType,location):
	#1. Use getGeocodeLocation to get the latitude and longitude coordinates of the location string.
	#2.  Use foursquare API to find a nearby restaurant with the latitude, longitude, and mealType strings.
	#HINT: format for url will be something like https://api.foursquare.com/v2/venues/search?client_id=CLIENT_ID&client_secret=CLIENT_SECRET&v=20130815&ll=40.7,-74&query=sushi
	#3. Grab the first restaurant
	#4. Get a  300x300 picture of the restaurant using the venue_id (you can change this by altering the 300x300 value in the URL or replacing it with 'orginal' to get the original picture
	#5. Grab the first image
	#6. If no image is available, insert default a image url
	#7. Return a dictionary containing the restaurant name, address, and image url	

    lat, lng = getGeoLocation(location)
    h = httplib2.Http()
    url = "https://api.foursquare.com/v2/venues/search?client_id={client_id}&client_secret={client_secret}&v=20170529&ll={lat},{lng}&query={mealType}&limit=1".format(
        client_id = foursquare_client_id,
        client_secret = foursquare_client_secret,
        lat = lat,
        lng = lng,
        mealType = mealType
        )
    response, content = h.request(url, "GET")
    data = json.loads(content)
    if data['response']['venues']:
        venue = {}
        venue_id = data['response']['venues'][0]['id']
        venue['name'] = data['response']['venues'][0]['name']
        venue['address'] = "".join(data['response']['venues'][0]['location']['formattedAddress'])

        url = "https://api.foursquare.com/v2/venues/{venue_id}?client_id={client_id}&client_secret={client_secret}&v=20170529".format(
            client_id = foursquare_client_id,
            client_secret = foursquare_client_secret,
            venue_id = venue_id
            )
        response, content = h.request(url, "GET")
        data = json.loads(content)
        try:
            #venue['photo'] = "{}{}".format(data['response']['venue']['photos']['groups'][0]['items'][0]['prefix'], data['response']['venue']['photos']['groups'][0]['items'][0]['suffix'][1:])
            for i in data['response']['venue']['tips']['groups'][0]['items']:
                if 'photourl' in i:
                    venue['photo'] = i['photourl'].replace("/original/", "/300x300/")
                    break
            if 'photo' not in venue:
                raise IndexError
        except IndexError:
            #print venue
            venue['photo'] = "http://www.tamaoho.maori.nz/sites/all/modules/media_gallery/images/empty_gallery.png"
	    #restaurantInfo = {'name':restaurant_name, 'address':restaurant_address, 'image':imageURL}
        print u"Restaurant Name: {}".format(venue['name'])
        print u"Restaurant Address: {}".format(venue['address'])
        print u"Image: {}".format(venue['photo'])
        print u""
        return venue #[venue['name'], venue['address'], venue['photo']]
    else:
        return u"No Restaurants Found"


if __name__ == '__main__':
	findARestaurant("Pizza", "Tokyo, Japan")
	findARestaurant("Tacos", "Jakarta, Indonesia")
	findARestaurant("Tapas", "Maputo, Mozambique")
	findARestaurant("Falafel", "Cairo, Egypt")
	findARestaurant("Spaghetti", "New Delhi, India")
	findARestaurant("Cappuccino", "Geneva, Switzerland")
	findARestaurant("Sushi", "Los Angeles, California")
	findARestaurant("Steak", "La Paz, Bolivia")
	findARestaurant("Gyros", "Sydney Australia")
	