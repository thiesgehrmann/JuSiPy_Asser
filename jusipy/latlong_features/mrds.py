from scipy.spatial import cKDTree
import os
import zipfile
import pandas as pd
import numpy as np

from .. import utils
from .. import GIS

dir_path = os.path.dirname(os.path.realpath(__file__))


class MRDS:
    """
    MRDS dataset for minerals
    https://mrdata.usgs.gov/mrds/

    Provides a get function that returns distances.
    """
    def __init__(self):
        dl_filename = '%s/data/mrds/mrds-csv.zip' % dir_path
        csv_filename = '%s/data/mrds/mrds.csv' % dir_path
        utils.dl.mkdir(filename=csv_filename)
        if not os.path.exists(csv_filename):
            print('downloading')
            utils.dl.download('https://mrdata.usgs.gov/mrds/mrds-csv.zip', dl_filename)
            zf = zipfile.ZipFile(file=dl_filename)
            zf.extract('mrds.csv', path=os.path.dirname(csv_filename))
        #fi
        self._df = pd.read_csv(csv_filename)
        self._df = self._df[['latitude','longitude','ore','gangue']]
        self._df = self._df[~(pd.isna(self._df.latitude) | pd.isna(self._df.longitude))]
        self._df.latitude = self._df.latitude.astype(np.number)
        self._df.longitude = self._df.longitude.astype(np.number)
        self._idx = cKDTree(list(zip(self._df.latitude, self._df.longitude)))
    #edef


    def calculate(self, lat, long):
        """
        Calculate the distance to the nearest mine for a single point
        Inputs:
            lat : latitude
            long: longitude
        Outputs:
            Corrected euclidean distance (see jusipy.GIS.projection.lat_distance_correction)
        """
        dist, idx = self._idx.query([(lat, long)], k=1)
        return(dist[0] * jusipy.GIS.projection.lat_distance_correction(lat))
    #edef

    def get(self, points, **kwargs):
        """
        For each point in point, return the distance to the nearest element in each dataset
        Downside... Distance is euclidean... Not geodesic...
        This exaggerates distances at the poles... How to fix?
        Input:
            points: a list of tuples, (lat, long)
            kwargs: Ignored inputs
        Output:
            distances: a DataFrame of EUCLIDEAN distances for each point (rows) to the
                       closest element in each dataset (columns)
        """
        dists, idxs = self._idx.query(points, k=1)
        corr = [ GIS.projection.lat_distance_correction(lat) for (lat,long) in points ]
        dist = np.array([ d*c for (d,c) in zip(dists, corr) ])
        return pd.DataFrame.from_dict({'distance_to_mine':dist})
    #edef
