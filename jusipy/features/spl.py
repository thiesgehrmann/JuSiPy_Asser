#"""
#API_1_DS2_en_csv_v2_10181830.csv
#https://data.worldbank.org/topic/agriculture-and-rural-development?view=chart
#"""

import os
dir_path = os.path.dirname(os.path.realpath(__file__))

from .sources import WorldBank

class SPL(WorldBank):
    """
    Social Protection & Labor

    Provides the following properties:
        features: A matrix of features
        M: The matrix with raw data
    """

    def __init__(self):
        super(SPL, self).__init__('%s/SPL_API_10_DS2_en_csv_v2_10189431.csv' % dir_path, sep=',', skiprows=3)
    #edef
#eclass
