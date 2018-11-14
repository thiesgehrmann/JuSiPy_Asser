#username: jusipy
#password: jusipy847T0

from PIL import Image
import matplotlib.pylab as plt
import requests
import os
import numpy as np
import pandas as pd
dir_path = os.path.dirname(os.path.realpath(__file__))

from .. import GIS
from .. import utils

################################################################################

data = {
    "GFSAD1KCD" : {
        "dat" : "https://e4ftl01.cr.usgs.gov/MEASURES/GFSAD1KCD.001/2007.01.01/GFSAD1KCD.2010.001.2016348142525.tif",
        "url" : "https://lpdaac.usgs.gov/dataset_discovery/measures/measures_products_table/gfsad1kcd_v001",
        "type" : "tif",
        "lab" : ["No Data", "Ocean", "Irrigated", "Irrigated Mixed Crops 1", "Irrigated Mixed Crops 2", "Rainfed",
                    "Rainfed", "Rainfed Mixed Crops", "Fractions of Mixed Crops", "Non-Cropland" ]},

    "GFSAD1KCM" : {
        "dat" : "https://e4ftl01.cr.usgs.gov/MEASURES/GFSAD1KCM.001/2007.01.01/GFSAD1KCM.2010.001.2016348142550.tif",
        "url" : "https://lpdaac.usgs.gov/dataset_discovery/measures/measures_products_table/gfsad1kcm_v001",
        "type" : "tif",
        "lab" : [ "Ocean", "Croplands, Irrigation", "Croplands, Irrigation", "Croplands, Rainfed",
                "Croplands, Rainfed", "Croplands, Rainfed", "unknown1", "unknown2", "Non-Cropland",]},

    "MCD12C1" : {
        "hdf" : "https://e4ftl01.cr.usgs.gov/MOTA/MCD12C1.006/2017.01.01/MCD12C1.A2017001.006.2018257171411.hdf",
        "url" : "https://lpdaac.usgs.gov/dataset_discovery/modis/modis_products_table/mcd12c1",
        "type" : "hdf",
        "lab" : []
    }
}

################################################################################

class USGS(object):
    """
    Collect land cover features from the USGS.
    https://lpdaac.usgs.gov/dataset_discovery?f%5B0%5D=im_field_spatial_extent%3A50&f%5B1%5D=im_field_product%3A6

    Available datasets:
     * GFSAD1KCD
     * GFSAD1KCM
     * MCD12C1 (MODIS - NEED a different way to load this dataset...)
    """

    __slots__ = [ '_dataset', '_matrix', '_username', '_password', '_lookup', '_draw', '_dat_filename' ]

    def __init__(self, dataset, username='jusipy', password='jusipy847T0', overwrite=False):
        """
        Inputs:
            dataset: String.
             * GFSAD1KCD - GEOTIFF
             * GFSAD1KCM - GEOTIFF
             * MCD12C1 (MODIS - NEED a different way to load this dataset...)
            username: String. EARTHDATA.nasa.gov username
            password: String. EARTHDATA.nasa.gov password
            overwrite: Boolean. Overwrite the downloaded file (or not)
        """
        print('\rLoading GLCF(%s)%s' % (dataset, ' '*100), end='' )
        self._dataset  = dataset
        self._username = username
        self._password = password

        if dataset not in data:
            return None
        #fi
        dat, dat_type = data[dataset]['dat'], data[dataset]['type']
        status, self._dat_filename = self._download_dataset(dat, overwrite=overwrite, dat_type=dat_type)

        if not(status):
            return None
        #fi

        Image.MAX_IMAGE_PIXELS = 815068801
        if dat_type == 'tif':
            self._matrix = np.array(Image.open(self._dat_filename))
            self._lookup = self._lookup_tif
            self._draw   = self._draw_tif
        elif dat_type in 'hdf':
            self._matrix = None
            self._lookup = self._lookup_hdf
            self._draw   = self._draw_hdf
        else:
            return None
        #fi

    #edef

    def _download_dataset(self, dat, overwrite, dat_type):
        dat_filename = "%s/data/usgs/usgs_%s.%s" % (dir_path, self._dataset, dat_type)
        utils.dl.mkdir(filename=dat_filename)
        dat_status = download_earthdata(dat, dat_filename, self._username, self._password, overwrite=overwrite)

        return dat_status, dat_filename
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
        return self._lookup(lat, long, pixel_window)
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
        return pd.DataFrame([ self.lookup(lat, long) for (lat,long) in points ])
    #edef

    def _draw_tif(self, lat, long, **kwargs):
        return GIS.projection.draw(self._matrix, lat, long, **kwargs)
    #edef

    def _draw_hdf(self, lat, long):
        return None
    #edef

    def draw(self, lat=0, long=0, **kwargs):
        return self._draw(lat, long, **kwargs)
    #edef


    def _lookup_tif(self, lat, long, pixel_window):
        """
        See docstring for lookup
        """

        if self._matrix is None:
            return None
        #

        rel_region = GIS.projection.latlong_lookup(self._matrix, lat, long, pixel_window=pixel_window)

        pix_sum  = None

        return rel_region

        for idx in np.nditer(rel_region):
            val      = self._dummy_labels(rel_region[idx])
            pix_sum  = val if (pix_sum is None) else (pix_sum + val)
        #efor

        return pix_sum / np.prod(rel_region.shape)
    #edef

    def _lookup_hdf(self, lat, long, pixel_window):
        """
        See docstring for lookup
        """
        return None
    #edef

#eclass

################################################################################
# Earthdata download code taken from
# https://wiki.earthdata.nasa.gov/display/EL/How+To+Access+Data+With+Python

# overriding requests.Session.rebuild_auth to mantain headers when redirected
class SessionWithHeaderRedirection(requests.Session):
    AUTH_HOST = 'urs.earthdata.nasa.gov'
    def __init__(self, username, password):
        super().__init__()
        self.auth = (username, password)
    # Overrides from the library to keep headers when redirected to or from
    # the NASA auth host.

    def rebuild_auth(self, prepared_request, response):
        headers = prepared_request.headers
        url = prepared_request.url

        if 'Authorization' in headers:
            original_parsed = requests.utils.urlparse(response.request.url)
            redirect_parsed = requests.utils.urlparse(url)

            if (original_parsed.hostname != redirect_parsed.hostname) and \
                    redirect_parsed.hostname != self.AUTH_HOST and \
                    original_parsed.hostname != self.AUTH_HOST:
                    del headers['Authorization']
            #fi
        #fi
        return
    #edef
#eclass

def download_earthdata(url, filename, username, password, overwrite=False):
    if not(os.path.exists(filename)) or overwrite:
        # create session with the user credentials that will be used to authenticate access to the data
        session = SessionWithHeaderRedirection(username, password)

        try:
            # submit the request using the session
            response = session.get(url, stream=True)

            # raise an exception in case of http errors
            response.raise_for_status()

            # save the file
            with open(filename, 'wb') as fd:
                for chunk in response.iter_content(chunk_size=1024*1024):
                    fd.write(chunk)
                #efor
            #ewith
            return True
        except requests.exceptions.HTTPError as e:
            return False
        #etry
    #fi
    return True
#edef
