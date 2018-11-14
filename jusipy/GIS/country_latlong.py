import geopandas as gpd
import pandas as pd
import shapely as sp
import os
dir_path = os.path.dirname(os.path.realpath(__file__))

class CountryLatLong(object):
    """
    Retrieve the country for a given latitude/longitude pair
    Uses data from https://github.com/johan/world.geo.json (lat/long are INVERTED GRRR)

    Provides:
      function lookup, to look up a single coordinate, and
      function get, to look up multiple points in one go.

      property countries_iso3 : A list of country names present in this dataset
    """
    def __init__(self):
        path='%s/data/world_geo/' % dir_path
        files = [ '%s/%s' % (path, f) for f in os.listdir(path) if 'geo.json' in f]
        polygons = pd.concat([ gpd.read_file(f) for f in files ])
        self._polygons = { r.id : r.geometry for i, r in polygons.iterrows()}
    #edef

    @property
    def countries_iso3(self):
        """
        Countries represented
        """
        return sorted(self._polygons.keys())
    #edef

    def lookup(self, lat, long):
        """
        Lookup the ISO3 country code for a given coordinate
        Returns:
            ISO3 country code if present in countries, else None
        """
        for iso3, polygon in self._polygons.items():
            if polygon.contains(sp.geometry.Point(long, lat)):
                return iso3
            #fi
        #efor
        return None
    #edef

    def get(self, coords):
        """
        Lookup the ISO3 country code for a given coordinate
        Input:
            coords: An array of pairs (lat,long) of coordinates
        Returns:
            An array of length of input with values:
            ISO3 country code if present in countries, else None
        """
        return [self.lookup(c[0], c[1]) for c in coords]
    #edef
#eclass
