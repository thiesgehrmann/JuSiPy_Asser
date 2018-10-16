#username: jusipy
#password: jusipy847T0

import requests
import os
dir_path = os.path.dirname(os.path.realpath(__file__))

################################################################################

data = {
    "GFSAD1KCD" : {
        "tif" : "https://e4ftl01.cr.usgs.gov/MEASURES/GFSAD1KCD.001/2007.01.01/GFSAD1KCD.2010.001.2016348142525.tif",
        "xml" : "https://e4ftl01.cr.usgs.gov/MEASURES/GFSAD1KCD.001/2007.01.01/GFSAD1KCD.2010.001.2016348142525.tif.xml",
        "url" : "https://lpdaac.usgs.gov/dataset_discovery/measures/measures_products_table/gfsad1kcd_v001",
        "lab" : ["Ocean", "Irrigated", "Irrigated Mixed Crops 1", "Irrigated Mixed Crops 2", "Rainfed", "Rainfed",
                    "Rainfed", "Rainfed Mixed Crops", "Fractions of Mixed Crops", "Non-Cropland" ]},
    "GFSAD1KCM" : {
        "tif" : "https://e4ftl01.cr.usgs.gov/MEASURES/GFSAD1KCM.001/2007.01.01/GFSAD1KCM.2010.001.2016348142550.tif",
        "xml" : "https://e4ftl01.cr.usgs.gov/MEASURES/GFSAD1KCM.001/2007.01.01/GFSAD1KCM.2010.001.2016348142550.tif.xml",
        "url" : "https://lpdaac.usgs.gov/dataset_discovery/measures/measures_products_table/gfsad1kcm_v001",
        "lab" : [ "Ocean", "Croplands, Irrigation", "Croplands, Irrigation", "Croplands, Rainfed",
                "Croplands, Rainfed", "Croplands, Rainfed", "unknown1", "unknown2", "Non-Cropland",]},
    "MCD12C1" : {}
}

################################################################################

class USGS(object):
    """
    Collect land cover features from the USGSself.
    https://lpdaac.usgs.gov/dataset_discovery?f%5B0%5D=im_field_spatial_extent%3A50&f%5B1%5D=im_field_product%3A6

    GFSAD1KCD:
    """

    __slots__ = [ '_dataset', '_matrix', '_username', '_password' ]

    def __init__(self, dataset, username='jusipy', password='jusipy847T0', overwrite=False):
        self._dataset  = dataset
        self._username = username
        self._password = password

        if dataset not in data:
            return None
        #fi

        tif, xml = data[dataset]['tif'], data[dataset]['xml']

        status, self._tif_filename, self.xml_filename = self._download_dataset(tif, xml, overwrite=overwrite)
    #edef

    def load_matrix(self):


    def _download_dataset(self, tif, xml, overwrite):
        tif_filename = "%s/usgs_%s.tif" % (dir_path, self._dataset)
        xml_filename = "%s/usgs_%s.xml" % (dir_path, self._dataset)
        tif_status = download_earthdata(tif, tif_filename, self._username, self._password, overwrite=overwrite)
        xml_status = download_earthdata(xml, xml_filename, self._username, self._password, overwrite=overwrite)

        return (tif_status and xml_status), tif_filename, xml_filename
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
