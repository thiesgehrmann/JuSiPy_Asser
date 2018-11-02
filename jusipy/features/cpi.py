import pandas as pd
import os
dir_path = os.path.dirname(os.path.realpath(__file__))

class CPI(object):
    """
    Corruption perceived index
    Provides the following methods:
        score: Return the CPI scores
        rank: Return the CPI ranks
    Provides the following property:
        M: The matrix with raw data
    """

    __slots__ = [ '_matrix', '_countries', '_countries_iso3', '_rank_index', '_score_index' ]

    def __init__(self):
        self._matrix = pd.read_csv('%s/landportal-TI-CPI.csv' % dir_path, sep=';')
        df = self._matrix[self._matrix.indicatorLabel.apply(lambda x: 'Score' in x)]
        df = df[df.year == df.groupby('country_iso3').transform(max).year]
        df.value = df.value.map(float)
        df.year = df.year.map(int)
        self._countries_iso3 = sorted(set(df.country_iso3.values))
        self._countries = sorted(set(df.countryLabel.values))
        self._score_index = dict(df[['country_iso3', 'value']].values)
        self._rank_index = { c:i  for i,c in enumerate(sorted(self._score_index, key=lambda x: self._score_index[x])) }
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

    @property
    def M(self):
        """
        Access the raw matrix data
        """
        return self._matrix
    #edef

    def score(self, countries):
        """
        Return the CPI score of a list of countries (based on the most up-to-date information for that country)
        Input:
            countries: String of ISO3 country identifier, or else a list of strings
        Output:
            Integer or list of integers. Missing values encode by None
        """
        if isinstance(countries, str):
            return self._score_index[countries] if countries in self._score_index else None
        else:
            return [ (self._score_index[c] if c in self._score_index else None) for c in countries ]
        #fi
    #edef

    def rank(self, countries):
        """
        Return the CPI rank of a list of countries (based on the most up-to-date information for that country)
        Input:
            countries: String of ISO3 country identifier, or else a list of strings
        Output:
            Integer or list of integers. Missing values encode by None
        """
        if isinstance(countries, str):
            return self._rank_index[countries] if countries in self._rank_index else None
        else:
            return [ (self._rank_index[c] if c in self._rank_index else None) for c in countries ]
        #fi
    #edef
