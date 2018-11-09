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

    res = matrix[lat-pixel_window:lat+pixel_window+1,long-pixel_window:long+pixel_window+1]
    return res
#edef

def draw(matrix, lat=0, long=0):
    fig, ax = plt.subplots(1)
    ax.imshow(matrix)
    lat, long = project(matrix, lat, long)
    size_y, size_x = matrix.shape
    ax.plot([0, size_x], [lat, lat], c='r')
    ax.plot([long, long], [0, size_y], c='r')

    return ax
#edef
