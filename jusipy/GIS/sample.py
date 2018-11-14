import numpy as np
from ..latlong_features import GLCF

def _random_unit_sphere():
    """
    Randomly sample a point from the unit sphere
    http://mathworld.wolfram.com/SpherePointPicking.html
    """
    u, v = np.random.uniform(size=2)
    long = 2 * np.pi * u
    lat = np.arccos(2*v - 1)
    return lat, long
#edef

def _random_latlong():
    unit_lat, unit_long = _random_unit_sphere()

    lat = ((unit_lat - (np.pi/2)) / (np.pi/2)) * 90
    long = (unit_long - np.pi) / np.pi * 180

    return (lat, long)
#edef

def _random_latlong_land(glcf):
    """
    Return a random
    """

    while True:
        lat, long = _random_latlong()
        res = glcf.lookup(lat, long)
        if res[0] != 1:
            break
        #fi
    #ewhile
    return lat, long
#edef

def random_latlong(land=False, glcf=None, size=1):
    """
    Return lat/longitude coordinates
    Inputs:
        land: Boolean. Only return points on land
        glcf: a GLCF object. (Default the lowest resolution (1deg) is used)
        size: The number of coordinates to return
    Output:
        A list of (x,y) coordinates randomly scattered across the earth
    """
    points = None
    if land:
        if glcf is None:
            glcf = GLCF(resolution='1deg')
        #fi
        points = [ _random_latlong_land(glcf) for i in range(size) ]
    else:
        points = [ _random_latlong() for i in range(size) ]
    #fi

    if size == 1:
        return points[0]
    #fi
    return points
#edef

def grid_latlong(land=False, glcf=None, lat_points=1000, long_points=None):
    """
    Return lat/longitude coordinates uniformly sampled across the globe (not enriched at the poles)
    Inputs:
        land: Boolean. Only return points on land
        glcf: a GLCF object. (Default the lowest resolution (1deg) is used)
        lat_points: The number of points to sample in the latitude
        long_points: The number of points to sample on the equator
    Output:
        A list of (x,y) coordinates uniformly scattered across the earth
    """

    long_points = 2*lat_points
    coords = []

    for lat in np.arange(-np.pi,np.pi, (2*np.pi)/lat_points)[1:-1]:
        step_size = ((2*np.pi)/long_points)/((np.abs(np.cos(lat/2))))
        steps = np.arange(-np.pi,np.pi, step_size)[1:-1]
        for long in steps:
            coords.append(((lat/np.pi)*90, (long/np.pi)*180))
        #efr
    #efor

    if land:
        if glcf is None:
            glcf = jusipy.latlong_features.GLCF(resolution='1deg')
        #fi
        coords = [ (lat, long) for (lat, long) in coords if glcf.lookup(lat, long)[0] != 1 ]
    #fi

    return coords
#edef
