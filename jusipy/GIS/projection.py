import matplotlib.pylab as plt
import numpy as np

def project(matrix, lat, long):
    """
    Project lat/long pair onto a matrix.
    ASSUMES matrix has ratio of 180/360! and upper corner is 90,-180!!!
    Inputs:
        lat, long: Floats
    Outputs:
        index_lat, index_long : Integers
    """
    mult = float(matrix.shape[1]/360.0)

    assert abs(lat) <= 90
    assert abs(long) <= 180

    lat  = mult * (180 - (lat + 90))
    long = mult * (long + 180)

    lat  = int(lat)
    long = int(long)

    return lat, long
#edef

def latlong_lookup(matrix, lat, long, pixel_window=0):
    """
    Lookup the land cover classification at this location
    Inputs:
        lat, long: Floats. Latitude and Longitude
        pixel_window: Integer. Return the average counts per pixel in an PxP square around the location given.

    Output:
        numpy array of features

    Depending upon the resolution, we multiply the latitude and longitude by a constant to index the data matrix.
    """

    lat, long = project(matrix, lat, long)

    # | a b |
    # | c d |

    a = max(lat-pixel_window, 0)
    b = min(lat+pixel_window+1, matrix.shape[0])
    c = max(long-pixel_window, 0)
    d = min(long+pixel_window+1, matrix.shape[1])

    res = matrix[a:b,c:d]
    return res
#edef

def draw(matrix, lat=0, long=0, ax=None):
    if ax is None:
        fig, axes = plt.subplots(ncols=1, nrows=1, figsize=(10,5))
        ax = axes
    #fi

    ax.imshow(matrix)

    lat, long = project(matrix, lat, long)
    size_y, size_x = matrix.shape
    ax.plot([0, size_x], [lat, lat], c='r')
    ax.plot([long, long], [0, size_y], c='r')

    return ax
#edef

def lat_distance_correction(lat):
    """
    When calculating distances between geodesic coordinates in the euclidean space,
    distances at the poles (-90, 90) tend to become exaggerated.
    This function provides a heuristic correction factor for distances calculated
    in a euclidean space based on the latitude of the query point.

    Input:
        lat: Float [-90,90] The latitude
    Output:
        Correction factor (multiply the distance with this value) [0,1]
        Is near 1 near equator, and near 0 near the pole.
    """
    return ((np.cos(np.pi*(lat/90))+1)/2)**(1/1.5)
#edef


def haversine(coord1, coord2):
    """
    Calculate the great-circle distance between two coordinates.
    Inputs:
        coord1: coordinate one (lat, long)
        coord2: coordinate two (lat, long)
    Output:
        Distance in meters along the globe.
    """
    R = 6372800  # Earth radius in meters
    lat1, lon1 = coord1
    lat2, lon2 = coord2

    phi1, phi2 = np.radians(lat1), np.radians(lat2)
    dphi       = np.radians(lat2 - lat1)
    dlambda    = np.radians(lon2 - lon1)

    a = np.sin(dphi/2)**2 + \
        np.cos(phi1)*np.cos(phi2)*np.sin(dlambda/2)**2

    return 2*R*np.atan2(np.sqrt(a), np.sqrt(1 - a))
#edef
