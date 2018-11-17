import pandas as pd
import numpy as np
from collections import namedtuple

import os

dir_path = os.path.dirname(os.path.realpath(__file__))

from .. import GIS

class WB_LDI(object):
    """
    World Bank land dispute index
    Provides:
    properties: features, countries_iso3 and description
    function: get
    """
    def __init__(self):
        cc = GIS.CountryCode()

        ldi = pd.read_csv('%s/data/WB_LDI.csv' % dir_path, sep=',')
        ldi['country_iso3'] = ldi.A.apply(lambda c: cc[c].iso3)
        ldi = ldi[~pd.isna(ldi.country_iso3)]
        print(ldi[pd.isna(ldi.country_iso3)].A)
        ldi = ldi.rename(columns={ 'B':'Land_dispute_resolution_index',
                                       'C':'Law_required_registration',
                                       'D':'State_or_private_guarantee',
                                       'E':'Compensation_for_scaming',
                                       'F':'Check_for_document_legality',
                                       'H':'Verification_of_parties_in_property_transaction',
                                       'J':'Is_there_a_national_database_to_verify_the_accuracy_of_identity_documents',
                                       'M':'land_dispute_statistics',
                                      })
        ldi = ldi.drop(columns=['A'])
        ldi = ldi.set_index('country_iso3')
        for col in ldi.columns:
            ldi[col] = ldi[col].astype(float)
        #efor
        self._features = ldi
        self._nt = namedtuple('WB_LDI_features', self._features.columns)
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
                 'Law_required_registration'                  : "Does the law require that all property sale transactions be registered at the immovable property registry to make them opposable to third parties?",
                 "State_or_private_guarantee"  : "Is the system of immovable property registration subject to a state or private guarantee?",
                 'Compensation_for_scaming'          : "Is there a specific compensation mechanism to cover for losses incurred by parties who engaged in good faith in a property transaction based on erroneous information certified by the immovable property registry?",
                 'Check_for_document_legality' : "Does the legal system require a control of legality of the documents necessary for a property transaction (e.g., checking the compliance of contracts with requirements of the law)? ",
                 'Verification_of_parties_in_property_transaction': "Does the legal system require verification of the identity of the parties to a property transaction?",
                 'Is_there_a_national_database_to_verify_the_accuracy_of_identity_documents' : "Is there a national a to verify the accuracy of identity documents?.",
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
