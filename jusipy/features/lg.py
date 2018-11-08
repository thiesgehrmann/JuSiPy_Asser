
import os
dir_path = os.path.dirname(os.path.realpath(__file__))

from .sources import LandPortal

class LG(LandPortal):
    """
    Land and Gender distribution per country

    Provides the following properties:
        features: A matrix of features
        M: The matrix with raw data
    """

    __slots__ = [ '_matrix', '_pmatrix', '_countries', '_countries_iso3', '_features', '_nt', '_year_index' ]

    def __init__(self):
        super(LG, self).__init__('%s/landportal-TI-CPI.csv' % dir_path, sep=';')
    #edef
#eclass
