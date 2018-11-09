import numpy as np
from .. import landcover

def _random_unit_sphere():
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
    """
    points = None
    if land:
        if glcf is None:
            glcf = landcover.GLCF(resolution='1deg')
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
