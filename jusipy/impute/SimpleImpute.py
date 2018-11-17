import numpy as np
import sklearn
from sklearn.impute import SimpleImputer
import pandas as pd

class SimpleImpute(object):
    """

    """
    def __init__(self, features_df, **kwargs):
        self._features = features_df.drop_duplicates()
        self._kwargs   = kwargs

        self._fit(**kwargs)
    #edef
    def _fit(self, **kwargs):
        self._fit = SimpleImputer(missing_values=np.nan, **self._kwargs).fit(X=self._features)
    #edef

    def predict(self, new_df):
        return pd.DataFrame(self._fit.transform(new_df), columns=new_df.columns, index=new_df.index)
    #edef
#edef
