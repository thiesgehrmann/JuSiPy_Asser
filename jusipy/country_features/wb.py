#"""
#API_1_DS2_en_csv_v2_10181830.csv
#https://data.worldbank.org/topic/agriculture-and-rural-development?view=chart
#"""

import os
dir_path = os.path.dirname(os.path.realpath(__file__))

from .sources import WorldBank

class WB_ARD(WorldBank):
    """
    Agriculture and Rural Development indicators

    Provides the following properties:
        features: A matrix of features
        M: The matrix with raw data
    """

    def __init__(self):
        super(WB_ARD, self).__init__('%s/data/ARD_API_1_DS2_en_csv_v2_10181830.csv' % dir_path, sep=',', skiprows=3)
    #edef
#eclass


class WB_SPL(WorldBank):
    """
    Social Protection & Labor

    Provides the following properties:
        features: A matrix of features
        M: The matrix with raw data
    """

    def __init__(self):
        super(WB_SPL, self).__init__('%s/data/SPL_API_10_DS2_en_csv_v2_10189431.csv' % dir_path, sep=',', skiprows=3)
    #edef
#eclass

class WB_SD(WorldBank):
    """
    Social Development indicators

    Provides the following properties:
        features: A matrix of features
        M: The matrix with raw data
    """

    def __init__(self):
        super(WB_SD, self).__init__('%s/data/SD_API_15_DS2_en_csv_v2_10186395.csv' % dir_path, sep=',', skiprows=3)
    #edef
#eclass
