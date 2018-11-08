#"""
#API_1_DS2_en_csv_v2_10181830.csv
#https://data.worldbank.org/topic/agriculture-and-rural-development?view=chart
#"""

import os
dir_path = os.path.dirname(os.path.realpath(__file__))

from .sources import WorldBank

class ARD(WorldBank):
    """
    Agriculture and Rural Development indicators

    Provides the following properties:
        features: A matrix of features
        M: The matrix with raw data
    """

    def __init__(self):
        super(ARD, self).__init__('%s/ARD_API_1_DS2_en_csv_v2_10181830.csv' % dir_path, sep=',', skiprows=3)
    #edef
#eclass
