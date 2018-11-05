from .cpi import CPI # Corruption perception index
from .lg import LG   # Land and Gender
from .ard import ARD # WB Agricultural and Rural development
from .spl import SPL # WB Social Protection and Labor
from .sd import SD   # WB Social Development

_datasets = [ CPI, LG, ARD, SPL, SD ]

def all(countries=None):
    import pandas as pd
    loadedSets = [ d() for d in _datasets ]
    all_countries = sorted(set([ c for d in loadedSets for c in d.countries_iso3]))
    if countries is None:
        countries = all_countries
    else:
        countries = [ c for c in countries if c in all_countries]
    #fi

    all_df = pd.DataFrame({'country_iso3' : countries}).set_index('country_iso3')
    for d in loadedSets:
        all_df = all_df.join(d.features[[c for c in d.features.columns if c not in all_df.columns]], how='left')
    #efor
    return all_df
#edef
