import pandas as pd

from collections import namedtuple

from .. import GIS

class All_country(object):
    """
    Get all features simultaneously
    """

    __slots__ = [ '_countries_iso3', '_countries', '_datasets', '_description', '_nt', '_features']

    def __init__(self, datasets):

        cc = GIS.CountryCode()

        self._datasets = datasets
        self._countries_iso3 = sorted(set([ c for d in datasets for c in d.countries_iso3]))
        self._countries = [ cc[c].country for c in self._countries_iso3]
        self._description = { '%s__%s' % (d.__class__.__name__, f): desc for d in datasets for (f,desc) in d.description.items() }
        self._nt = [ '%s__%s' % (d.__class__.__name__, f) for d in datasets for f in d._nt._fields ]

        self._features = pd.DataFrame({'country_iso3' : self._countries_iso3}).set_index('country_iso3')
        for d in self._datasets:
            self._features = self._features.join(d.features.rename(columns={f : '%s__%s' % (d.__class__.__name__, f) for f in d.features.columns}))
        #efor



    #edef

    def _get(self, country, year='newest', fuzzy=None):
        return [ f for d in self._datasets for f in d.get(country, year, fuzzy) ]
    #edef

    def get(self, countries, years='newest', fuzzy=None, df=None):
        """
        Retrieve features for a country (or list of countries)
        Inputs:
            Countries: A single country (ISO3 identifier) or a list of countries
            years: A year (or 'newest' to revrieve the ), or a list of years (in equal length of the countries)
            fuzzy: None or integer of the number of years up or down to look around the provided year for a suitable replacement
            df: Ignored, added only for compatabiity to the CountryFeatures class
        Output:
            A dataframe (in the case of df=True)
        """
        inputList = True
        if isinstance(countries,str):
            inputList = False
            countries = [countries]
        #fi

        if (isinstance(years, str) or isinstance(years, int)):
            years = [ years ] * len(countries)
        #fi

        if isinstance(fuzzy, int) or (fuzzy is None):
            fuzzy = [ fuzzy ] * len(countries)
        #fi

        if (len(countries) != len(fuzzy)) or (len(countries) != len(years)):
            raise InputError
        #fi

        res = [ self._get(c, y, f) for (c,y,f) in zip(countries, years, fuzzy) ]

        res = pd.DataFrame(res, columns=self._nt)

        return res
    #edef


    @property
    def features(self):
        """
        Return a dataframe of the features, indexed by iso3 country ID
        """
        return self._features
    #edef

    @property
    def  description(self):
        """
            A dictionary with a description of the features in this dataset.
        """
        return self._description
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
