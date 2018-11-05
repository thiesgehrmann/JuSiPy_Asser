import pandas as pd
import os
dir_path = os.path.dirname(os.path.realpath(__file__))

class LG(object):
    """
    Land and Gender distribution per country

    Provides the following properties:
        features: A matrix of features
        M: The matrix with raw data
    """

    __slots__ = [ '_matrix', '_countries', '_countries_iso3', '_features' ]

    def __init__(self):
        m = pd.read_csv('%s/landportal-WB-SE.csv' % dir_path, sep=';')
        self._matrix = m
        m.indicatorID = m.
        features = dict(m[['indicatorID', 'indicatorLabel']].drop_duplicates().values)
        newpd = m[['country_iso3']].drop_duplicates().set_index('country_iso3')
        for f in features:
            newpd = newpd.join(m[m.indicatorID == f][['country_iso3', 'value']].rename(columns={'value':f}).set_index('country_iso3'))
        #edef
        self._features = newpd
        self._countries_iso3 = sorted(set(m.country_iso3.values))
        self._countries = sorted(set(m.countryLabel.values))
    #edef

    @property
    def features(self):
        """
        Return a dataframe of the features, indexed by iso3 country ID
        FAO-LG.1FA : Agricultural holders by sex (female - total n)
        FAO-LG.1FB : Distribution of agricultural holders by sex (female - Share %)
        FAO-LG.1MA : Agricultural holders by sex (male - total n)
        FAO-LG.1MB : Distribution of agricultural holders by sex (male - Share %)
        FAO-LG.1T  : Total number of agricultural holders
        FAO-LG.2F  : Distribution of agricultural landowners by sex (female - share %)
        FAO-LG.2M  : Distribution of agricultural landowners by sex (male - share %)
        FAO-LG.3FA : Incidence of agricultural landowners (female only - share%)
        FAO-LG.3FB : Incidence of agricultural landowners (female sole & joint - share%)
        FAO-LG.3MA : Incidence of agricultural landowners (male only - share%)
        FAO-LG.3MB : Incidence of agricultural landowners (male sole & joint - share%)
        FAO-LG.4F  : Distribution of agricultural land area owned by sex (female - share%)
        FAO-LG.4M  : Distribution of agricultural land area owned by sex (male - share%)
        FAO-LG.5F  : Distribution of agricultural land value owned by sex (female - share%)
        FAO-LG.5M  : Distribution of agricultural land value owned by sex (male - share%)
        """
        return self._features
    #edef

    @property
    def countries_iso3(self):
        """
        Return a list of countries represented in this dataset in iso3 format
        """
        return self._countries_iso3
    #edef

    @property
    def countries(self):
        """
        Return a list of countries represented in this dataset.
        """
        return self._countries
    #edef
#eclass
