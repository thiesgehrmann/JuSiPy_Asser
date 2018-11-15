import geopandas as gpd
import shapely as sp
from scipy.spatial import cKDTree
import numpy as np
import pandas as pd

import os
dir_path = os.path.dirname(os.path.realpath(__file__))

from .. import GIS

class NaturalEarth_single(object):
    """
    Downside... Distance is euclidean... Not geodesic...
    This exaggerates distances at the poles... How to fix?
    NOTE: NaturalEarth points are given in (long,lat)... Need to reverse points!!
    """
    def __init__(self, file):
        print('\rLoading NaturalEarth(%s)%s' % (file, ' '*100), end='')
        self._DF = gpd.read_file(file)
        self._indexes = self._index()
    #edef

    def _index(self):
        indexes = {}
        index_types = set(self._DF.geometry.apply(lambda x: x.type).values)
        for itype in index_types:
            indexes[itype] = {'Point' : self._index_point,
                              'Polygon' : self._index_polygon,
                              'LineString' : self._index_linestring,
                              'MultiLineString' : self._index_multilinestring}[itype]()
        #fi
        return indexes
    #edef

    def _index_point(self):
        points = self._DF[self._DF.geometry.apply(lambda x: x.type == 'Point')].geometry

        btree  = cKDTree(np.array(list(zip(points.x, points.y))))
        df_idx = np.array(range(len(points.values)))
        return lambda p : btree.query([(pt.x, pt.y) for pt in p], k=1)
    #edef

    def _index_polygon(self):
        """
        Querying polygons can a long time. Therefore, we perform a heuristic here.
        We query the individual points in the convex hull of the polygon, and find the polygon that
        has a closest boundary point to our query point. This narrows down the search considerably
        Then we calculate the distance to the counary shape.
        """

        polygons = self._DF[self._DF.geometry.apply(lambda x: x.type == 'Polygon')].geometry.values
        plist = np.array(list(enumerate(polygons)))
        polygon_points = np.array([ p for poly_i, poly in plist for p in poly.convex_hull.boundary.coords ])
        btree = cKDTree(polygon_points)
        btree_idx = np.array([ poly_i for poly_i, poly in plist for p in poly.convex_hull.boundary.coords ])
        def func(plist, btree, btree_idx, points):
            _dist, closest_polygon_points = btree.query(np.array([ (p.x, p.y) for p in points]), k=1)
            closest_polygons = btree_idx[closest_polygon_points]
            distances_indexes = [ (plist[poly_i][1].distance(p), poly_i)
                                  for ((poly_i, poly), p) in zip(plist[closest_polygons], points) ]

            distances, indexes = zip(*distances_indexes)
            return np.array(distances), np.array(indexes)
        #edef

        return lambda p: func(plist, btree, btree_idx, p)
    #edef

    def _index_linestring(self):
        LS = self._DF[self._DF.geometry.apply(lambda x: x.type == 'LineString')].geometry.values

        line_points = np.array([ p for ls in LS for p in ls.coords ])
        df_idx      = np.array([ i for i, ls in enumerate(LS) for p in ls.coords ])
        btree       = cKDTree(line_points)

        def func(lines, btree, btree_idx, points):
            _dist, closest_line_points = btree.query(np.array([ (p.x, p.y) for p in points]), k=1)
            closest_lines = btree_idx[closest_line_points]
            distances_indexes = [ (lines[line_idx].distance(p), line_idx)
                                  for (line_idx, p) in zip(closest_lines, points) ]
            distances, indexes = zip(*distances_indexes)
            return np.array(distances), np.array(indexes)
        #edef

        return lambda p : func(LS, btree, df_idx, p)
    #edef

    def _index_multilinestring(self):
        MLS = self._DF[self._DF.geometry.apply(lambda x: x.type == 'MultiLineString')].geometry.values

        line_points = np.array([ p for mls in MLS for ls in mls for p in ls.coords ])
        df_idx = np.array([ i for i, mls in enumerate(MLS) for ls in mls for p in ls.coords ])

        btree = cKDTree(line_points)
        def func(lines, btree, btree_idx, points):
            _dist, closest_line_points = btree.query(np.array([ (p.x, p.y) for p in points]), k=1)
            closest_lines = btree_idx[closest_line_points]
            distances_indexes = [ (lines[line_idx].distance(p), line_idx)
                                  for (line_idx, p) in zip(closest_lines, points) ]
            distances, indexes = zip(*distances_indexes)
            return np.array(distances), np.array(indexes)
        #edef

        return lambda p : func(MLS, btree, df_idx, p)
    #edef

    def query_nearest(self, points):
        """
        For each point in point, return the distance to the nearest element in the dataset, and the index of that point
        Downside... Distance is euclidean... Not geodesic...
        This exaggerates distances at the poles... How to fix?
        Input:
            points: a list of tuples, or shapely.geometry.Point objects, in (lat, long) format
        Output:
            distances: an np.array of length len(points) describing the EUCLIDEAN DISTANCE in the lat/long projection
            indexes: an np.array of length len(points) describing the index in the self._DF dataframe
        """
        points = [ sp.geometry.Point(p[1], p[0]) if not isinstance(p, sp.geometry.Point) else sp.geometry.Point(p.y, p.x) for p in points ]
        min_dist        = np.ones(len(points)) * 1e100
        min_dist_df_idx = np.ones(len(points)) * 1e100

        point_corr = np.array([ GIS.projection.lat_distance_correction(p.y) for p in points ])
        for itype in self._indexes:
            func      = self._indexes[itype]
            dist, idx = func(points)
            dist = dist * point_corr

            min_dist_df_idx[dist < min_dist] = idx[dist < min_dist]
            min_dist[dist < min_dist] = dist[dist < min_dist]
        #efor

        return min_dist, min_dist_df_idx
    #edef

class NaturalEarth(object):
    def __init__(self):
        datasets = { 'airport'    : '%s/data/natural_earth/ne_10m_airports' % dir_path,
                     'port'       : '%s/data/natural_earth/ne_10m_ports' % dir_path,
                     'roads'      : '%s/data/natural_earth/ne_10m_roads' % dir_path,
                     'railroad'   : '%s/data/natural_earth/ne_10m_railroads' % dir_path,
                     'urban_area' : '%s/data/natural_earth/ne_10m_urban_areas' % dir_path }

        self._loaded = { name : NaturalEarth_single(datasets[name]) for name in datasets }
    def get(self, points, **kwargs):
        """
        For each point in point, return the distance to the nearest element in each dataset
        Downside... Distance is euclidean... Not geodesic...
        This exaggerates distances at the poles... How to fix?
        Input:
            points: a list of tuples, or shapely.geometry.Point objects
            kwargs: Ignored inputs
        Output:
            distances: a DataFrame of EUCLIDEAN distances for each point (rows) to the
                       closest element in each dataset (columns)
        """
        fields = {}
        for name in self._loaded:
            fields['nearest_%s' % name], _idx = self._loaded[name].query_nearest(points)
        #efor
        return pd.DataFrame.from_dict(fields)
    #edef
#eclass
