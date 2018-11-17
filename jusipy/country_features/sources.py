import pandas as pd
from collections import namedtuple

from .. import GIS

class CountryFeatures(object):

    def __init__(self, m, pm):
        self._matrix  = m
        self._pmatrix = pm

        nt = namedtuple('CountryFeatures', [ f.replace('.', '_').replace('-', '_') for f in pm.columns.levels[1] ])

        self._nt = nt

        year_index = { country_iso3.lower() : {} for country_iso3 in pm.index }

        for country_iso3, row in pm.iterrows():
            country_iso3 = country_iso3.lower()
            year_index[country_iso3]['newest'] = [ None for f in nt._fields ]
            for year in row.index.levels[0]:
                values = [ x if not pd.isna(x) else None for x in row[year].values ]
                year_index[country_iso3][str(year)] = values
                newest = [ n if (n is not None) else o for (o,n) in zip(year_index[country_iso3]['newest'], values) ]
                year_index[country_iso3]['newest'] = newest
            #efor
        #efor

        self._year_index = year_index

        cc = GIS.CountryCode()
        countries_iso3 = [ c for c in m.country_iso3.drop_duplicates().values if not pd.isna(c) ]
        countries = [ cc[c].country for c in countries_iso3 ]

        self._countries      = countries
        self._countries_iso3 = countries_iso3

        features = pd.DataFrame([ self._get(country) for country in self._countries_iso3 ],
                                        index=self._countries_iso3,
                                        columns=self._nt._fields)


        self._features = features
    #edef

    def _get(self, country, year='newest', fuzzy=None):
        country = country.lower()
        year = str(year)

        if (country not in self._year_index) or (year not in self._year_index[country]):
            return self._nt(*[None for f in self._nt._fields])
        #fi

        if (fuzzy == None) or year == 'newest':
            return self._nt(*self._year_index[country.lower()][year])
        else:
            fields = self._year_index[country.lower()][year]
            fuzzy_years = [ (self._get(country, str(int(year)-i), fuzzy=None),
                             self._get(country, str(int(year)+i), fuzzy=None)) for i in range(fuzzy) ]
            fuzzy_years = [ fy for fys in fuzzy_years for fy in fys ]
            for i, f in enumerate(fields):
                if f is None:
                    for alt in fuzzy_years:
                        if alt[i] is not None:
                            fields[i] = alt[i]
                            break
                        #fi
                    #efor
                #fi
            #efor
            return self._nt(*fields)
        #fi
    #edef

    def get(self, countries, years='newest', fuzzy=None, df=False, *pargs, **kwargs):
        """
        Retrieve features for a country (or list of countries)
        Inputs:
            Countries: A single country (ISO3 identifier) or a list of countries
            years: A year (or 'newest' to revrieve the ), or a list of years (in equal length of the countries)
            fuzzy: None or integer of the number of years up or down to look around the provided year for a suitable replacement
            df: Boolean. Return a dataframe
        Output:
            A named tuple (in the case of a non-list input)
            A list of named tuples (in the case of list input)
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

        if df:
            res = pd.DataFrame(res, columns=self._nt._fields)
            #res['country'] = [ c.upper() for c in countries ]
            #res['year'] = years
            return res
        #fi

        if not inputList:
            return res[0]
        #fi

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
        return { k.replace('.', '_').replace('-', '_') : v
                 for (k,v) in dict(self._matrix[['indicatorID','indicatorLabel']].drop_duplicates().values).items()
                 if not pd.isna(k) }
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

class LandPortal(CountryFeatures):
    def __init__(self, filename, **kwargs):
        print('\rLoading LandPortal(%s)%s' % (filename, ' '*100), end='' )
        m = pd.read_csv(filename, **kwargs)
        pm = m.drop_duplicates(['country_iso3', 'indicatorID', 'year']).set_index(['country_iso3', 'indicatorID', 'year']).value
        pm = pm.unstack().unstack()

        super(LandPortal, self).__init__(m, pm)
    #edef
#eclass



class WorldBank(CountryFeatures):
    def __init__(self, filename, **kwargs):
        print('\rLoading WorldBank(%s)%s' % (filename, ' '*100), end='' )
        m = pd.read_csv(filename, **kwargs)
        m = m.rename(columns={"Country Code": "country_iso3", "Indicator Code" : "indicatorID",
                                        "Indicator Name": "indicatorLabel", 'Country Name' : 'countryLabel' })
        pm = m.pivot(index='country_iso3', columns='indicatorID', values=m.columns[4:-1])

        super(WorldBank, self).__init__(m, pm)
    #edef

#eclass
