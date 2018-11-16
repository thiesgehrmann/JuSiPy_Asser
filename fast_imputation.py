import numpy as np
import sklearn
from sklearn.impute import SimpleImputer
import pandas as pd

def fast_imputation(df):
    name = df.name
    mean = np.mean(df)
    median = np.median(df[~df.isna()])
    df_temp = np.array(df).reshape(-1,1)
    
    imp = SimpleImputer(missing_values=np.nan, strategy='median')
    if mean!=median:
        imp = SimpleImputer(missing_values=np.nan, strategy='median')
    else:
        imp = SimpleImputer(missing_values=np.nan, strategy='mean')


    imp.fit(df_temp)  
    df_imp=imp.transform(df_temp)
    df_imp = df_imp.reshape(len(df_imp),)
    df_imp = pd.Series(df_imp)
    df_imp.name = name
    return df_imp