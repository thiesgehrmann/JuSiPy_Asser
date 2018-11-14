import difflib
from collections import namedtuple
import pandas as pd
import os
dir_path = os.path.dirname(os.path.realpath(__file__))

class CountryCode(object):
    """
    Translate between country codes
    Usage:
        CC = CountryCode()
        CC['Germany'] # Returns: countrycode(country='Germany', iso2='DE', iso3='DEU', number=276)
    """

    __slots__ = [ '_matrix', '_index', '_tups', '_special_cases' ]

    def __init__(self):
        self._matrix = pd.read_csv('%s/data/country_iso3.csv' % dir_path, sep=';')
        tup = namedtuple('countrycode', ['country', 'iso2', 'iso3', 'number'])
        self._tups = list(map(lambda x: tup(*x), self._matrix.values))
        self._index = { str(k).lower() : i for i,t in enumerate(self._tups) for k in t }

        self._special_cases = { 'democratic republic of the congo': 'congo, (kinshasa)',
                                "democratic people's republic of korea": 'korea (south)',
                                'republic of korea': 'korea (south)',
                                'the former yugoslav republic of macedonia': 'macedonia, republic of',
                                'east timor': 'timor-leste',
                                'burma': 'myanmar',
                                'dutch': 'netherlands',
                                'tanzania': 'tanzania, united republic of',
                                'russia': 'russian federation',
                                'uae': 'united arab emirates',
                                'south korea': 'korea (south)',
                                'north korea': 'korea (north)',
                                'taiwan': 'taiwan, republic of china',
                                'venezuela': 'venezuela (bolivarian republic)'}

        for s,c in self._special_cases.items():
            self._index[s.lower()] = self._index[c.lower()]
        #efor
        self._tups.append(tup(None, None, None, None))
    #edef

    @property
    def country(self):
        """
        A list of all countries represented in this index
        """
        return [ cc.country for cc in self._tups]
    #edef

    @property
    def iso2(self):
        """
        A list of all ISO2 represented in this index
        """
        return [ cc.iso2 for cc in self._tups]
    #edef

    @property
    def iso3(self):
        return [ cc.iso2 for cc in self._tups]
    #edef

    @property
    def number(self):
        return [ cc.number for cc in self._tups]
    #edef

    def _lookup(self, key):
        k = str(key).lower()

        if k in self._index:
            return self._tups[self._index[k]]
        #fi

        matches = difflib.get_close_matches(k, self._index.keys())
        if len(matches) > 0:
            km = matches[0]
            return self._tups[self._index[km]]
        else:
            sk = ' '.join(k.split()[:-1])
            if len(sk) == 0:
                return self._tups[-1]
            #fi
            rec = self._lookup(sk)
            if rec.country is None:
                print('Did not find "%s". Consider adding special case' % key)
            #fi
            return rec
        #fi
    #edef

    def __getitem__(self, keys):
        if isinstance(keys, str) or isinstance(keys, int):
            return self._lookup(keys)
        else:
            return [ self._lookup(k) for k in keys ]
        #fi
    #edef
#edef
