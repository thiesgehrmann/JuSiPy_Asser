import urllib
import gzip
import os
dir_path = os.path.dirname(os.path.realpath(__file__))

from PIL import Image
import numpy as np

from .. import utils

class Glcf_avhrr(object):
    """
    Look up land cover classifications from the Global Land Cover Foundation, using AVHRR data.

    Provides:
     * lookup(), which provides a classification at the 1degree scale.
     * columns, the names of the features provided by this dataset

    """

    __slots__ = [ '_dataFile', '_resolution', '_matrix', 'labels' ]

    def __init__(self, resolution="8km"):
        """
        Create the object
        Inputs:
            resolution: Resolution to use. String. [1deg|8km|1km]
        """
        self._dataFile = self._downloadResolution(resolution)
        self._matrix = np.array(Image.open(gzip.open(self._dataFile)))
        self._resolution = resolution
        self.labels = ['Water', 'Evergreen Needleleaf Forest', 'Evergreen Broadleaf Forest',
         'Deciduous Needleleaf Forest', 'Deciduous Broadleaf Forest', 'Mixed Forest',
         'Woodland', 'Wooded Grassland', 'Closed Shrubland', 'Open Shrubland', 'Grassland',
         'Cropland', 'Bare Ground', 'Urban and Built' ]
    #edef

    def _downloadResolution(self, resolution):
        urls = { "1deg" : "ftp://ftp.glcf.umd.edu/glcf/Global_Land_Cover/Global/1deg/AVHRR_1deg_LANDCOVER_1981_1994.GLOBAL.tif.gz",
                 "8km" : "ftp://ftp.glcf.umd.edu/glcf/Global_Land_Cover/Global/8km/AVHRR_8km_LANDCOVER_1981_1994.GLOBAL.tif.gz",
                 "1km" : "ftp://ftp.glcf.umd.edu/glcf/Global_Land_Cover/Global/1km/AVHRR_1km_LANDCOVER_1981_1994.GLOBAL.tif.gz"}


        resolution = resolution.lower()
        if resolution not in urls:
            return None
        #fi

        fileName = '%s/glcf_avhrr_%s.tif.gz' % (dir_path, resolution)
        if not(utils.dl.download_ftp(urls[resolution], fileName)):
            return None
        #fi

        return fileName
    #edef

    def lookup(self, lat, long, pixel_window=0):
        """
        Lookup the land cover classification at this location
        Inputs:
            lat, long: Floats. Latitude and Longitude

        Output:
            numpy array of features

        Depending upon the resolution, we multiply the latitude and longitude by a constant to index the data matrix.
        """

        if self._matrix is None:
            return None

        if self._resolution == '1deg':
            mult = 1
        elif self._resolution == '8km':
            mult = 100.0/8.0
        elif self._resolution == '1km':
            mult = 100.0
        else:
            return None
        #fi

        lat  = mult * (180 - (lat + 90))
        long = mult * (long + 180)

        lat  = int(lat)
        long = int(long)

        pix_sum  = None
        n_pixels = 0

        for pixel_i in range((lat-pixel_window),(lat+pixel_window+1)):
            for pixel_j in range((long-pixel_window), (long+pixel_window+1)):
                val      = self._dummy_labels(self._matrix[pixel_i, pixel_j])
                pix_sum  = val if (pix_sum is None) else (pix_sum + val)
                n_pixels = n_pixels + 1
            #efor
        #efor

        return pix_sum / n_pixels
    #edef

    def _dummy_labels(self, value):
        labels = np.zeros(14)
        labels[value] = 1
        return labels
    #edef

    @property
    def columns(self):
        return [ 'avrhh_%s_%s' % (self._resolution, c.lower().replace(' ','_')) for c in self.labels]
    #edef

#eclass
