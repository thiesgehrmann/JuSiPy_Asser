from .cpi import CPI # Corruption perception index
from .lg import LG   # Land and Gender
from .ard import ARD # WB Agricultural and Rural development
from .spl import SPL # WB Social Protection and Labor
from .sd import SD   # WB Social Development
from .se import SE  #

_datasets = [ CPI, LG, SE, ARD, SPL, SD ]

def All(datasets=None):
    from .all_datasets import All as _all_datasets

    if datasets is None:
        datasets = [ d() for d in _datasets ]
    #fi

    return _all_datasets(datasets)
#edef
