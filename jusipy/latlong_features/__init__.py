from .naturalearth import NaturalEarth
from .glcf_avhrr import GLCF
from .usgs import USGS
from .mrds import MRDS
from .cru import CRU

def All(datasets=None):
    from .all_datasets import All_latlong

    if datasets is None:
        datasets = [ NaturalEarth(),
                     GLCF(resolution='1deg'),
                     GLCF(resolution='8km'),
                     MRDS(),
                     CRU() ]
    #fi

    return All_latlong(datasets)
#edef

def get(df, feature, pixel_window=0, lat_col='lat', long_col='long'):
    """
    A function to retrieve lat/long-level features
        df:           A DataFrame with relevant columns
        feature:      A latlong-feature object (e.g. GLCF, All_latlong)
        pixel_window: If relevant, the number of pixels to look into in the lookup
        lat_col:      The name of the column that has the latitude.
        long_col:     The name of the column that has the longitude.
    Output:
        A dataframe with rows the same order as countries columns, are features. Index is identical to df
    """
    lat  = df[lat_col].values
    long = df[long_col].values
    F = feature.get(list(zip(lat, long)), pixel_window=pixel_window)
    F['index'] = df.index
    return F.set_index('index')
#edef
