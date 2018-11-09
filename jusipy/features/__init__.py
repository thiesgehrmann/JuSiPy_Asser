from .lp import WB_LGAF, WB_SE, LMM_PICL, LMM_LSIC, WB_LG, TI_CPI
from .wb import WB_ARD, WB_SPL, WB_SD

_datasets = [ WB_LGAF, WB_SE, LMM_PICL, LMM_LSIC, WB_LG, TI_CPI, WB_ARD, WB_SPL, WB_SD ]

def All(datasets=None):
    from .all_datasets import All as _all_datasets

    if datasets is None:
        datasets = [ d() for d in _datasets ]
    #fi

    return _all_datasets(datasets)
#edef
