import numpy as np
import sklearn
from sklearn.impute import SimpleImputer
import pandas as pd

from .impute import Impute


class SimpleImpute(Impute):
    """
    A mean/median Simple imputer.
    """
    def __init__(self, features_df, **kwargs):
        super(SimpleImpute, self).__init__(features_df, **kwargs)
    #edef
    def _fit(self, **kwargs):
        self._fit = SimpleImputer(missing_values=np.nan, **self._kwargs).fit(X=self._features)
    #edef
#eclass
