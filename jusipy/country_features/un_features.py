import pandas as pd
import numpy as np
from collections import namedtuple

import os

dir_path = os.path.dirname(os.path.realpath(__file__))

from .. import GIS

class UN_HDI(object):
    """
    UN Human Development Index features
    Provides:
    properties: features, countries_iso3 and description
    function: get
    """
    def __init__(self):
        cc = GIS.CountryCode()

        unhdi = pd.read_csv('%s/data/UN_HDI.tsv' % dir_path, sep='\t')
        unhdi['country_iso3'] = unhdi.Country.apply(lambda c: cc[c].iso3)
        unhdi = unhdi.rename(columns={'Human Development Index (HDI)': 'Human_Development_Index',
                                      'Inequality-adjusted HDI (IHDI)': 'Inequality_adjusted_HDI',
                                      'Coefficient of human inequality': 'Coefficient_of_human_inequality',
                                      'Inequality in life expectancy': 'Inequality_in_life_expectancy',
                                      'Inequality-adjusted life expectancy index': 'Inequality_adjusted_life_expectancy_index',
                                      'Inequality in education': 'Inequality_in_education',
                                      'Inequality-adjusted education index': 'Inequality_adjusted_education_index',
                                      'Inequality in income': 'Inequality_in_income',
                                      'Inequality-adjusted income index': 'Inequality_adjusted_income_index',
                                      'Income_Quintile ratio': 'Income_Quintile_ratio',
                                      'Income_Palma ratio ': 'Income_Palma_ratio',
                                      'Gini coefficient': 'Gini_coefficient'})
        unhdi = unhdi.drop(columns=['Country'])
        unhdi = unhdi.set_index('country_iso3')
        for col in unhdi.columns:
            unhdi[col] = unhdi[col].astype(float)
        #efor
        self._features = unhdi
        self._nt = namedtuple('UN_HDI_features', self._features.columns)
        self._countries_iso3 = sorted(set(self._features.index.values))
        self._index = { iso3.lower() : r.values for  (iso3, r) in self._features.iterrows() }
        self._labels = self._features.columns
        self._empty = [ None for v in self._index[list(self._index.keys())[0]] ]

    @property
    def features(self):
        return self._features
    #edef

    @property
    def countries_iso3(self):
        return self._countries_iso3
    #edef

    @property
    def description(self):
        return { 'Human_Development_Index'                  : "A composite index measuring average achievement in three basic dimensions of human development—a long and healthy life, knowledge and a decent standard of living. See Technical note 1 at http://hdr.undp.org for details on how the HDI is calculated.",
                 'Inequality-adjusted_HDI'                  : "HDI value adjusted for inequalities in the three basic dimensions of human development. See Technical note 2 at http://hdr.undp.org for details on how the IHDI is calculated.",
                 "Overall loss"                             : "Percentage difference between the IHDI and the HDI.",
                 'Coefficient_of_human_inequality'          : "Average inequality in three basic dimensions of human development. See Technical note 2 at http://hdr.undp.org.",
                 'Inequality_in_life_expectancy'            : "Inequality in distribution of expected length of life based on data from life tables estimated using the Atkinson inequality index. ",
                 'Inequality-adjusted_life_expectancy_index': "The HDI life expectancy index adjusted for inequality in distribution of expected length of life based on data from life tables listed in Main data sources.",
                 'Inequality_in_education'                  : "Inequality in distribution of years of schooling based on data from household surveys estimated using the Atkinson inequality index.",
                 'Inequality-adjusted_education_index'      : "The HDI education index adjusted for inequality in distribution of years of schooling based on data from household surveys listed in Main data sources.",
                 'Inequality_in_income'                     : "Inequality in income distribution based on data from household surveys estimated using the Atkinson inequality index.",
                 'Inequality-adjusted_income_index'         : "The HDI income index adjusted for inequality in income distribution based on data from household surveys listed in Main data sources.",
                 'Income_Quintile_ratio'                    : "Ratio of the average income of the richest 20% of the population to the average income of the poorest 20% of the population.",
                 'Income_Palma_ratio'                       : "Ratio of the richest 10% of the population's share of gross national income (GNI) divided by the poorest 40%'s share. It is based on the work of Palma (2011), who found that middle class incomes almost always account for about half of GNI and that the other half is split between the richest 10% and poorest 40%, though their shares vary considerably across countries.",
                 'Gini_coefficient'                         : "Measure of the deviation of the distribution of income among individuals or households within a country from a perfectly equal distribution. A value of 0 represents absolute equality, a value of 100 absolute inequality."}
    #edef


    def getMany(self, countries, df=False, *pargs, **kwargs):
        """
        Get UN HDI features
        Input:
            countries: a list of ISO3 countries
            pargs, kwargs: Ignored inputs
        Output:
            A dataframe of HDI features, per country in input
        """
        if isinstance(countries,str):
            countries = [countries]
        R = [ self._nt(*self._index[c.lower()] if (c.lower() in self._index) else self._empty) for c in countries ]
        print(R)
        if df:
            return pd.DataFrame(R, columns = self._labels)
        else:
            return R
        #fi
    #edef

    def get(self, country, *pargs, **kwargs):
        """
        Get UN HDI features
        Input:
            countries: a list of ISO3 countries
            pargs, kwargs: Ignored inputs
        Output:
            A dataframe of HDI features, per country in input
        """
        c = country
        return self._nt(*self._index[c.lower()]) if (c.lower() in self._index) else self._empty

        #fi
    #edef

#eclass
