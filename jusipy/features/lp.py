from .sources import LandPortal
import os
dir_path = os.path.dirname(os.path.realpath(__file__))

class TI_CPI(LandPortal):
    """
    Corruption perceived index

    Provides the following properties:
        features: A matrix of features
        M: The matrix with raw data
    """

    __slots__ = [ '_matrix', '_pmatrix', '_countries', '_countries_iso3', '_features', '_nt', '_year_index' ]

    def __init__(self):
        super(TI_CPI, self).__init__('%s/data/landportal-TI-CPI.csv' % dir_path, sep=';')
    #edef
#eclass

class WB_LG(LandPortal):
    """
    Land and Gender distribution per country

    Provides the following properties:
        features: A matrix of features
        M: The matrix with raw data
    """

    __slots__ = [ '_matrix', '_pmatrix', '_countries', '_countries_iso3', '_features', '_nt', '_year_index' ]

    def __init__(self):
        super(WB_LG, self).__init__('%s/data/landportal-FAO-LG.csv' % dir_path, sep=';')
    #edef
#eclass

class LMM_LSIC(LandPortal):
    """
    LMM - Indicators of the Legal Security of Indigenous and Community Lands

    Provides the following properties:
        features: A matrix of features
        M: The matrix with raw data
    """

    __slots__ = [ '_matrix', '_pmatrix', '_countries', '_countries_iso3', '_features', '_nt', '_year_index' ]

    def __init__(self):
        super(LMM_LSIC, self).__init__('%s/data/landportal-LMM-LSIC.csv' % dir_path, sep=';')
    #edef
#eclass

class LMM_PICL(LandPortal):
    """
    LMM - Percent of Indigenous and Community Lands

    Provides the following properties:
        features: A matrix of features
        M: The matrix with raw data
    """

    __slots__ = [ '_matrix', '_pmatrix', '_countries', '_countries_iso3', '_features', '_nt', '_year_index' ]

    def __init__(self):
        super(LMM_PICL, self).__init__('%s/data/landportal-LMM-PICL.csv' % dir_path, sep=';')
    #edef
#eclass

class WB_SE(LandPortal):
    """
    Socio-Economic Indicators

    Provides the following properties:
        features: A matrix of features
        M: The matrix with raw data
    """

    def __init__(self):
        super(WB_SE, self).__init__('%s/data/landportal-WB-SE.csv' % dir_path, sep=';')
    #edef
#eclass

class WB_LGAF(LandPortal):
    """
    Land and Gender distribution per country

    Provides the following properties:
        features: A matrix of features
        M: The matrix with raw data
    """

    def __init__(self):
        super(WB_LGAF, self).__init__('%s/data/landportal-WB-LGAF2016.csv' % dir_path, sep=';')
    #edef
#eclass
