import requests

class Geocode(object):
    """
    Use MapQuest API to lookup addresses and Lat/Long codes.
    (Uses OpenStreetMap data)
    Documentation for the API is available at: https://developer.mapquest.com/documentation/open/geocoding-api/

    Provides two functions:
        * address: Look up the lat/longitude of an address
        * latlong: Look up the address of a lat/longitude pair

    Queries are Cached to prevent exceeding the limit
    """

    __slots__ = [ '_cache', '_key', '_urls', '_open' ]

    def __init__(self, key="oMQYBjXNZvdZetQhVAnAz1N6IJvQk8FD", open=True, cache={}):
        """
        Initialize the Geocode object
        Inputs:
            key: String. API Key for MapQuest
            Use this object as a cache (default is dict.)
        Output:
            Geocode object
        """
        self._cache = cache
        self._key = key
        self._open = open

        if open:
            self._urls = { "POST" : { False: "http://open.mapquestapi.com/geocoding/v1/reverse?key=%s",
                                      True: "http://open.mapquestapi.com/geocoding/v1/address?key=%s" },
                            "GET" : { False: "http://open.mapquestapi.com/geocoding/v1/reverse?key=%s&%s",
                                      True: "http://open.mapquestapi.com/geocoding/v1/address?key=%s&%s"}}
        else:
            self._urls = { "POST" : { False: "http://mapquestapi.com/geocoding/v1/reverse?key=%s",
                                      True: "http://mapquestapi.com/geocoding/v1/address?key=%s" },
                            "GET" : { False: "http://mapquestapi.com/geocoding/v1/reverse?key=%s&%s",
                                      True: "http://mapquestapi.com/geocoding/v1/address?key=%s&%s"}}
        #fi

    #edef

    def latlong(self, lat, long):
        """
        Lookup Lat/Longitude positions and return an address
        Inputs:
            lat: Latitude. Float
            long: Longitude. Float
        Output:
            Address in String format.
        """

        if (lat, long) not in self._cache:
            result = self._queryGet(False, { "location": '%f,%f' % (lat, long) })
            try:
                result = result['results'][0]['locations'][0]
                result = ','.join([result[f] for f in ['street', 'adminArea5', 'postalCode', 'adminArea1']])
                self._cache[(lat, long)] = result
            except Exception as e:
                self._cache[(lat, long)] = None
            #fi
        #fi
        return self._cache[(lat, long)]
    #edef


    def address(self, address):
        """
        Lookup an address and return lat/long in JSON format
        Input:
            Address: String
        Output:
            Tuple (latitude, longitude), (Float, Float)
        """
        if address not in self._cache:
            result = self._queryPost(True, {"location":address})
            try:
                latlng = result['results'][0]['locations'][0]['latLng']
                self._cache[address] = (latlng['lat'], latlng['lng'])
            except Exception as e:
                self._cache[address] = (None, None)
            #fi
        #fi
        return self._cache[address]
    #edef


    def _queryPost(self, address, data):
        """
        Perform a query with a POST format.
        Inputs:
            address: Boolean True if we want to lookup lat/Long of addresses or vice/versa
            data: Dictionary with POST data
        Output: JSON result
        """

        url = self._urls["POST"][address] % self._key
        response = requests.post(url, data=data)

        return response.json()
    #edef

    def _queryGet(self, address, data={}):
        """
        Perform a query with a POST format.
        Inputs:
            address: Boolean True if we want to lookup lat/Long of addresses or vice/versa
            data: Dictionary key/value pairs
        Output: JSON result
        """

        url = self._urls["GET"][address] % (self._key, '&'.join(['%s=%s' % (k,v) for (k,v) in data.items() ]))
        response = requests.get(url)

        return response.json()
    #edef
#eclass
