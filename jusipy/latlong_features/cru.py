import pandas as pd
import numpy as np

from .. import GIS

import os
dir_path = os.path.dirname(os.path.realpath(__file__))

class CRU(object):
    def __init__(self):
        '''
        Loading the weather datasets
        Data from Center of Enviromental Data Analysis, data mean values between 2011-2016
        Data link: http://data.ceda.ac.uk/badc/cru/data/cru_ts/cru_ts_4.01/data/
        '''
        # loads pre, cld, temp
        self._missingvalue = -999
        pre =  np.load(open('%s/data/weather_data/pre.npy' % dir_path, 'rb'))
        cld =  np.load(open('%s/data/weather_data/cld.npy' % dir_path, 'rb'))
        tmp =  np.load(open('%s/data/weather_data/tmp.npy' % dir_path, 'rb'))
        pet =  np.load(open('%s/data/weather_data/pet.npy' % dir_path, 'rb'))
        self._data = { 'rain' :pre, #  precipitation: mm/month
                       'cloud':cld, #  cloud cover: percentage
                       'temp':tmp,  #  near-surface temperature: degrees Celsius
                       'pet':pet    #  potential evapotranspiration:  mm/day
                     }

    #edef

    def lookup_single(self, feature, lat, long, pixel_window=0):
        '''
        Look for lat and long and return the mean values for the pixel window
        '''
        v = GIS.projection.latlong_lookup(self._data[feature], lat, long, pixel_window)
        v = v[v!=self._missingvalue]

        if len(v) == 0:
            return 0 # we don't query over water
        #fi
        return np.mean(v)
    #edef

    def lookup(self, lat, long, pixel_window=0):
        """

        """
        return np.array([ self.lookup_single(feat, lat, long, pixel_window) for feat in self._data ])
    #edef

    def get(self, coords, pixel_window=0):
        '''

        '''
        D = np.array([self.lookup(lat, long, pixel_window=pixel_window) for (lat,long) in coords])
        return pd.DataFrame(D, columns=list(self._data.keys()))
    #edef
