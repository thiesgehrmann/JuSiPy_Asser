from .lp import WB_LGAF, WB_SE, LMM_PICL, LMM_LSIC, WB_LG, TI_CPI
from .wb import WB_ARD, WB_SPL, WB_SD
from .un_features import UN_HDI
from .wb_ldi import WB_LDI

_datasets = [ WB_LGAF, WB_SE, LMM_PICL, LMM_LSIC, WB_LG, TI_CPI, WB_ARD, WB_SPL, WB_SD, UN_HDI, WB_LDI ]

def All(datasets=None):
    from .all_datasets import All_country as _all_datasets

    if datasets is None:
        datasets = [ d() for d in _datasets ]
    #fi

    return _all_datasets(datasets)
#edef

def get(df, feature, fuzzy=None, country_col='country', year_col='year'):
    """
    A function to retrieve country-level features per country/per year.
    Input:
        df:          A DataFrame with relevant columns
        feature:     A countyfeature object (e.g. TM_CPI, All_country)
        fuzzy:       The number of years to look around if we don't find a record for the country/year
        country_col: The name of the column in df which has the ISO3 country code
        year_col:    The name of the column in df which has the year
    Output:
        A dataframe with rows the same order as countries columns, are features. Index is identical to df
    """

    import pandas as pd

    countries = df[country_col].values
    if year_col in df.columns:
        def detect_year(year):
            if pd.isna(year):
                return 'newest'
            elif isinstance(year, str) and (year.lower().strip() == 'newest'):
                return 'newest'
            #fi
            try:
                return str(int(year))
            except Exception as e:
                return 'newest'
            #etry
        #edef
        years     = [ detect_year(y) for y in df[year_col].values ]
    else:
        years = ['newest' for c in countries]
    #fi
    F = feature.get(countries, years, fuzzy=fuzzy, df=True)
    F['index'] = df.index
    return F.set_index('index')
#edef
