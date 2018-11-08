import json
import requests

class FireDict(object):
    """
    A Firebase-based dictionary. Allows you to store data across multiple devices
    """
    __slots__ = [ '_url', '_auth', '_sub', '_cache' ]
    def __init__(self, url='https://jusipy-1541084665170.firebaseio.com/', auth=None, sub=None, cache=True):
        """
        url: Which database to use
        auth: Authentication. Currently unimplemented
        sub: Access a sub-structure of the database, rather than using the root.
        cache: Cache the queries (saves bandwidth). Note: A query is only made once!
            If your data changes in the database then caching may not be appropriate

        Behaves like a dictionary other than this.
        """
        self._url = url + ('/%s' % sub if sub else '')
        self._auth = auth
        self._sub = sub
        self._cache = {} if cache else None
    #edef

    def _keyify(self, key):
        ret = None
        if isinstance(key, str):
            ret = key
        elif hasattr(key, '__iter__'):
            ret = '_'.join([str(c) for c in key])
        else:
            ret = str(key)
        #fi

        return ret.translate(str.maketrans({c : '_' for c in ' !.@#?$%^&*()-+={}[];/\|'}))
    #edef

    def get(self, key, default=None):
        key = self._keyify(key)
        if (self._cache is not None) and (key in self._cache):
            return self._cache[key]
        #fi
        req = '%s/%s.json' % (self._url, key)

        res = requests.get(req).json()

        if self._cache is not None:
            self._cache[key] = res
        #fi

        if res is None:
            return default
        #fi

        return res
    #edef

    def put(self, key, data):
        key = self._keyify(key)

        if (self._cache is not None):
            self._cache[key] = data
        #fi
        req = '%s/%s.json' % (self._url, key)

        data = json.dumps(data)
        res = requests.put(req, data=data)

        return res
    #edef

    def __getitem__(self, key):
        return self.get(key)
    #edef

    def __setitem__(self, key, data):
        return self.put(key, data)
    #edef

    def __contains__(self, key):
        return self.get(key) is not None
    #edef

    def keys(self):
        return requests.get('%s.json?shallow=true' % self._url).json().keys()
    #edef
#eclass
