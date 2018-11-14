import pandas as pd
import numpy as np
import os
dir_path = os.path.dirname(os.path.realpath(__file__))

from .. import GIS

class GRAIN(object):
    """
    The GRAIN Dataset.

    Objects:
        M : Pandas DataFrame of land deals
    Properties:
        countries: A list of countries present in the dataset
        shape: Size of the dataset
    Functions:
        dealsFrom: Filters the deals based on the investor origin.
        dealsTo: Filters the deals based on the target of the investment
    """
    __slots__ = [ '_matrix', '_countries', '_countries_iso3' ]
    def __init__(self, matrix=None):
        """
        matrix: if None, the dataset is loaded from file. Otherwise, matrix is used as the dataset.
        """
        print('\rLoading GRAIN%s' % (' '*100), end='' )

        if matrix is not None and isinstance(matrix, pd.DataFrame):
            self._matrix = matrix
        else:
            m = pd.read_csv('%s/grain_dataset_2016.csv' % dir_path, sep=';')

            m.Hectares = m.Hectares.apply(lambda x: str(x).replace(' ','').replace('.', '').replace(',', '.'))
            m['Projected investment'] = m['Projected investment'].apply(lambda x: str(x).replace(' ','').replace('.', '').replace(',', '.') if isinstance(x, str) else None)
            self._matrix = self.__prepareMatrix(m)

        #fi
        self._countries = None
    #edef

    def __prepareMatrix(self, M):
        """
        Clean the matrix.
        """

        M['Hectares'] = M.Hectares.apply(lambda x: float(x.replace(',', '')) if isinstance(x, str) else None)
        M = M.rename(columns={'Landgrabbed': 'target_country',
                              'Landgrabber': 'investor_name',
                              'Base': 'investor_country',
                              'Production': 'crop',
                              'Sector' : 'intention',
                              'Hectares' : 'intended_size',
                              'Status of deal': 'negotiation_status'})

        CC = GIS.CountryCode()
        M['investor_country'] = M['investor_country'].apply(lambda x: x.split(',') if isinstance(x, str) else [])
        M['target_country_iso3'] = M.target_country.apply(lambda c: CC[c].iso3)
        M['investor_country_iso3'] = M.investor_country.apply(lambda L: [ cc.iso3 for cc in CC[L]] )

        return M
    #edef

    @property
    def M(self):
        return self._matrix
    #edef


    @property
    def countries(self):
        if self._countries is None:
            in_countries  = self.M.target_country.values
            out_countries = [out.split(',') for out in self.M.investor_country.values if isinstance(out, str) ]
            out_countries = [ c.strip() for out in out_countries for c in out  ]
            self._countries = sorted(set(in_countries) | set(out_countries))
        #fi
        return self._countries
    #edef

    @property
    def countries_iso3(self):
        if self._countries is None:
            in_countries  = self.M.target_country_iso3.values
            out_countries = [ out for out in self.M.investor_country_iso3.values if isinstance(out, str) ]
            out_countries = [ c.strip() for out in out_countries for c in out  ]
            self._countries_iso3 = sorted(set(in_countries) | set(out_countries))
        #fi
        return self._countries_iso3
    #edef


    def dealsFrom(self, countries, iso3=True):
        """
        Return all deals in which the investor is in the list of countries provided
        Input:
            countries: String of single country, of list of strings of countries
            iso3 : Boolean. Lookup iso3 identifiers
        Output:
            pandas data frame
        """
        if isinstance(countries, str):
            countries = [ countries ]
        #fi
        col = self.M.investor_country_iso3 if iso3 else self.M.investor_country
        mat = self.M[col.apply(lambda c: hasattr(c, '__iter__') and any([(country in c) for country in countries]))]
        return GRAIN(matrix=mat)
    #edef

    def dealsTo(self, countries, iso3=True):
        """
        Return all deals in which the target country is in the list of countries provided
        Input:
            countries: String of single country, of list of strings of countries
            iso3 : Boolean. Lookup iso3 identifiers
        Output:
            pandas data frame
        """
        if isinstance(countries, str):
            countries = [ countries ]
        #fi
        col = self.M.target_country_iso3 if iso3 else self.M.target_country
        mat = self.M[col.isin(countries)]
        return GRAIN(matrix=mat)
    #edef

    def _repr_html_(self):
        return self._matrix._repr_html_()
    #edef
#eclass
