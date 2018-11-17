class All_latlong(object):
    def __init__(self, datasets):
        self._datasets = datasets
    #edef

    def get(self, points, *pargs, **kwargs):
        """
        Perform a lookup for many points
        Inputs:
            points: A list of tuples or lat/long locations
            **kwargs: specific arguments for the datasets
        Outputs:
            DataFrame of feature percentages
        """
        dfs = [ d.get(points, **kwargs) for d in self._datasets ]
        joined_d = dfs[0]
        for i, d in enumerate(dfs[1:]):
            joined_d = joined_d.join(d, rsuffix='%d' % (i+1))
        #efor

        return joined_d
    #edef

    @property
    def datasets(self):
        return self._datasets
#edef
