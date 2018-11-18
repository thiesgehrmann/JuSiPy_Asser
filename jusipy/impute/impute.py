import numpy as np
import sklearn
from sklearn.impute import SimpleImputer
import pandas as pd

class Impute(object):
    """

    """
    def __init__(self, features_df, **kwargs):
        self._features, self._types = set_column_types(features_df)
        self._features = self._features.select_dtypes([np.number])

        self._features = self._features.drop_duplicates()
        self._kwargs   = kwargs

        self._means = None
        self._stds  = None
        self._normalized = None

        self._normalize()
        self._fit(**kwargs)
    #edef

    def _normalize(self):
        self._means = self._features.mean()
        self._stds  = self._features.std()
        self._normalized = (self._features - self._means) / self._stds
    #edef

    def _fit(self, **kwargs):
        self._fit = SimpleImputer(missing_values=np.nan, **self._kwargs).fit(X=self._normalized)
    #edef

    def predict(self, new_df):
        new_df_types = new_df.copy()
        for col in new_df.columns:
            new_df_types[col] = pd.to_numeric(new_df_types[col], errors='coerce') if self._types[col] == 'numeric' else new_df_types[col].astype('category')
        #efor

        new_df_types = (new_df_types[self._features.columns] - self._means) / self._stds

        return pd.DataFrame(self._fit.transform(new_df_types), columns=new_df_types.columns, index=new_df_types.index)
    #edef
#edef


def set_column_types(df):

    new_df = df.copy()

    types = {}

    for col in df.columns:
        series = df[col]
        if hasattr(series, 'str'):
            not_na = series.str.isnumeric()[~pd.isna(series)]
            if all(not_na):
                #print('%s numeric' % col)
                new_df[col] = pd.to_numeric(series, errors='coerce')
                types[col] = 'numeric'
            else:
                #print('%s categorical' % col)
                new_df[col].astype('category')
                types[col] = 'category'
                # make it categorical
            #fi
        else:
            #print('%s numeric' % col)
            new_df[col] = pd.to_numeric(series, errors='coerce')
            types[col] = 'numeric'
        #edef
    #efor

    return new_df, types
#efor
