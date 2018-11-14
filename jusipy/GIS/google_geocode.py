import requests

class GoogleCode(object):
    """
    Use MapQuest API to lookup addresses and Lat/Long codes.
    (Uses OpenStreetMap data)
    Documentation for the API is available at: https://developer.mapquest.com/documentation/open/geocoding-api/

    Provides two functions:
        * address: Look up the lat/longitude of an address
        * latlong: Look up the address of a lat/longitude pair

    Queries are Cached to prevent exceeding the limit
    """

    __slots__ = [ '_cache', '_key', '_urls' ]

    def __init__(self, key="AIzaSyBLDh-LJ-bJBEIwLRgEosD1cdn_OtuS1Kg ", cache={}):
        """
        Initialize the Geocode object
        Inputs:
            key: String. API Key for MapQuest
            cache: Use this object as a cache (default is dict.)
        Output:
            Geocode object
        """
        self._cache = cache
        self._key = key
        self._urls = { "address": "https://maps.googleapis.com/maps/api/geocode/json?address=%s&key=%s",
                       "latlong": "https://maps.googleapis.com/maps/api/geocode/json?latlng=%f,%f&key=%s"}

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
            result = self._queryLatlong(lat, long)
            try:
                res = result['results'][0]
                res = { '_'.join(f['types']): f['long_name'] for f in res['address_components']  }
                self._cache[(lat, long)] = res
            except Exception as e:
                self._cache[(lat, long)] = {}
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
        address = address.lower()
        if address not in self._cache:
            result = self._queryAddress(address)
            try:
                result = result['results'][0]['geometry']['location']
                self._cache[address] = (result['lat'], result['lng'])
            except Exception as e:
                self._cache[address] = (None, None)
            #fi
        #fi
        return self._cache[address]
    #edef


    def _queryAddress(self, address):
        """
        Perform a query with a POST format.
        Inputs:
            address: address text
        Output: JSON result
        """
        address = '+'.join(address.replace('&=;', '').split())
        url = self._urls["address"] % (address, self._key)
        response = requests.get(url)

        return response.json()
    #edef

    def _queryLatlong(self, lat, long):
        """
        Perform a query with a POST format.
        Inputs:
            address: address text
        Output: JSON result
        """

        url = self._urls["latlong"] % (float(lat), float(long), self._key)
        response = requests.get(url)

        return response.json()
    #edef
#eclass
