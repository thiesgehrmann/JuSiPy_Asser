import urllib
import gzip
import os
dir_path = os.path.dirname(os.path.realpath(__file__))

from PIL import Image
import pandas as pd
import numpy as np

from .. import utils
from .. import GIS

_labels = { '1deg' : [ 'Water', 'Broadleaf Evergreen Forest', 'Coniferous Evergreen Forest and Woodland',
                       'High latitude Deciduous Forest and Woodland', 'Tundra',
                       'Mixed Coniferous Forest and Woodland', 'Wooded Grassland', 'Grassland',
                       'Bare Ground', 'Shrubs and Bare Ground', 'Cultivated Crops',
                       'Broadleaf Deciduous Forest and Woodland', 'Data Unavailable'],
            '8km' : ['Water', 'Evergreen Needleleaf Forest', 'Evergreen Broadleaf Forest',
                     'Deciduous Needleleaf Forest', 'Deciduous Broadleaf Forest', 'Mixed Forest',
                     'Woodland', 'Wooded Grassland', 'Closed Shrubland', 'Open Shrubland', 'Grassland',
                     'Cropland', 'Bare Ground', 'Permanent snow and ice', 'coding_error_do_not_use_feature' ],
            '1km' : ['Water', 'Evergreen Needleleaf Forest', 'Evergreen Broadleaf Forest',
                     'Deciduous Needleleaf Forest', 'Deciduous Broadleaf Forest', 'Mixed Forest',
                     'Woodland', 'Wooded Grassland', 'Closed Shrubland', 'Open Shrubland', 'Grassland',
                     'Cropland', 'Bare Ground', 'Permanent snow and ice', 'Urban and Built' ]         }

class GLCF(object):
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
        print('\rLoading GLCF(%s)%s' % (resolution, ' '*100), end='' )
        self._dataFile = self._downloadResolution(resolution)
        Image.MAX_IMAGE_PIXELS = 648000001
        self._matrix = np.array(Image.open(gzip.open(self._dataFile)))
        self._resolution = resolution
        self.labels = _labels[self._resolution]
    #edef

    def _downloadResolution(self, resolution):
        urls = { "1deg" : "ftp://ftp.glcf.umd.edu/glcf/Global_Land_Cover/Global/1deg/AVHRR_1deg_LANDCOVER_1981_1994.GLOBAL.tif.gz",
                 "8km" : "ftp://ftp.glcf.umd.edu/glcf/Global_Land_Cover/Global/8km/AVHRR_8km_LANDCOVER_1981_1994.GLOBAL.tif.gz",
                 "1km" : "ftp://ftp.glcf.umd.edu/glcf/Global_Land_Cover/Global/1km/AVHRR_1km_LANDCOVER_1981_1994.GLOBAL.tif.gz"}


        resolution = resolution.lower()
        if resolution not in urls:
            return None
        #fi

        fileName = '%s/data/glcf_avhrr/glcf_avhrr_%s.tif.gz' % (dir_path, resolution)
        utils.dl.mkdir(filename=fileName)
        if not(utils.dl.download_ftp(urls[resolution], fileName)):
            return None
        #fi

        return fileName
    #edef

    def draw(self, lat=0, long=0, **kwargs):
        return GIS.projection.draw(self._matrix, lat, long, **kwargs)
    #edef

    def lookup(self, lat, long, pixel_window=0):
        """
        Lookup the land cover classification at this location
        Inputs:
            lat, long: Floats. Latitude and Longitude
            pixel_window: Integer. Return the average counts per pixel in an PxP square around the location given.

        Output:
            numpy array of features

        Depending upon the resolution, we multiply the latitude and longitude by a constant to index the data matrix.
        """

        if self._matrix is None:
            return None
        #fi

        rel_region = GIS.projection.latlong_lookup(self._matrix, lat, long, pixel_window)

        pix_sum = None
        for value in np.nditer(rel_region):
            val      = self._dummy_labels(value)
            pix_sum  = val if (pix_sum is None) else (pix_sum + val)
        #efor

        return pix_sum / np.prod(rel_region.shape)
    #edef

    def get(self, points, pixel_window=0):
        """
        Perform a lookup for many points
        Inputs:
            points: A list of tuples or lat/long locations
            pixel_window: The range in which to look around the relevant pixel
        Outputs:
            DataFrame of feature percentages
        """
        return pd.DataFrame([ self.lookup(lat, long, pixel_window=pixel_window) for (lat,long) in points ], columns=self.labels)
    #edef

    def _dummy_labels(self, value):
        labels = np.zeros(len(self.labels))
        labels[value] = 1
        return labels
    #edef

    @property
    def columns(self):
        return [ 'avrhh_%s_%s' % (self._resolution, c.lower().replace(' ','_')) for c in self.labels]
    #edef

#eclass
