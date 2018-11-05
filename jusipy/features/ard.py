#"""
#API_1_DS2_en_csv_v2_10181830.csv
#https://data.worldbank.org/topic/agriculture-and-rural-development?view=chart
#"""

import pandas as pd
import os
dir_path = os.path.dirname(os.path.realpath(__file__))

class ARD(object):
    """
    Agriculture and Rural Development indicators

    Provides the following properties:
        features: A matrix of features
        M: The matrix with raw data
    """

    __slots__ = [ '_matrix', '_countries', '_countries_iso3', '_features' ]

    def __init__(self):
        def select_newest(row):
            """ Select the most recent data for each indicator per country """
            for i in range(4, len(row.index)-1)[::-1]:
                if not pd.isna(row[i]):
                    return (row.index[i], row[i])
                #fi
            #efor
            return (None, None)
        #edef

        m = pd.read_csv('jusipy/features/ARD_API_1_DS2_en_csv_v2_10181830.csv', skiprows=3)
        m['year'], m['value'] = list(zip(*list(m.apply(select_newest, axis=1))))
        m = m[['Country Code', 'Country Name', 'Indicator Name', 'Indicator Code', 'year', 'value']]
        m = m.rename(columns={"Country Code": "country_iso3", "Indicator Code" : "indicatorID",
                                "Indicator Name": "indicatorLabel", 'Country Name' : 'country' })

        self._matrix = m

        features = dict(m[['indicatorID', 'indicatorLabel']].drop_duplicates().values)
        newpd = m[['country_iso3']].drop_duplicates().set_index('country_iso3')
        for f in features:
            newpd = newpd.join(m[m.indicatorID == f][['country_iso3', 'value']].rename(columns={'value':f}).set_index('country_iso3'))
        #edef
        self._features = newpd
        self._countries_iso3 = sorted(set(m.country_iso3.values))
        self._countries = sorted(set(m.country.values))
    #edef

    @property
    def features(self):
        """
        Return a dataframe of the features, indexed by iso3 country ID
        TX.VAL.AGRI.ZS.UN : Agricultural raw materials exports (% of merchandise exports)
        TM.VAL.AGRI.ZS.UN : Agricultural raw materials imports (% of merchandise imports)
        SP.RUR.TOTL.ZS  : Rural population (% of total population)
        SP.RUR.TOTL.ZG  : Rural population growth (annual %)
        SP.RUR.TOTL     : Rural population
        SL.AGR.EMPL.ZS  : Employment in agriculture (% of total employment) (modeled ILO estimate)
        SL.AGR.EMPL.MA.ZS : Employment in agriculture, male (% of male employment) (modeled ILO estimate)
        SL.AGR.EMPL.FE.ZS : Employment in agriculture, female (% of female employment) (modeled ILO estimate)
        SI.POV.RUHC     : Rural poverty headcount ratio at national poverty lines (% of rural population)
        SI.POV.RUGP     : Rural poverty gap at national poverty lines (%)
        NV.AGR.TOTL.ZS  : Agriculture, forestry, and fishing, value added (% of GDP)
        NV.AGR.TOTL.CD  : Agriculture, forestry, and fishing, value added (current US$)
        ER.H2O.FWAG.ZS  : Annual freshwater withdrawals, agriculture (% of total freshwater withdrawal)
        EN.POP.EL5M.RU.ZS : Rural population living in areas where elevation is below 5 meters (% of total population)
        EN.ATM.NOXE.AG.ZS : Agricultural nitrous oxide emissions (% of total)
        EN.ATM.NOXE.AG.KT.CE : Agricultural nitrous oxide emissions (thousand metric tons of CO2 equivalent)
        EN.ATM.METH.AG.ZS : Agricultural methane emissions (% of total)
        EN.ATM.METH.AG.KT.CE : Agricultural methane emissions (thousand metric tons of CO2 equivalent)
        EG.ELC.ACCS.RU.ZS : Access to electricity, rural (% of rural population)
        AG.YLD.CREL.KG  : Cereal yield (kg per hectare)
        AG.SRF.TOTL.K2  : Surface area (sq. km)
        AG.PRD.LVSK.XD  : Livestock production index (2004-2006 = 100)
        AG.PRD.FOOD.XD  : Food production index (2004-2006 = 100)
        AG.PRD.CROP.XD  : Crop production index (2004-2006 = 100)
        AG.PRD.CREL.MT  : Cereal production (metric tons)
        AG.LND.TRAC.ZS  : Agricultural machinery, tractors per 100 sq. km of arable land
        AG.LND.TOTL.RU.K2 : Rural land area (sq. km)
        AG.LND.TOTL.K2  : Land area (sq. km)
        AG.LND.PRCP.MM  : Average precipitation in depth (mm per year)
        AG.LND.IRIG.AG.ZS : Agricultural irrigated land (% of total agricultural land)
        AG.LND.FRST.ZS  : Forest area (% of land area)
        AG.LND.FRST.K2  : Forest area (sq. km)
        AG.LND.EL5M.RU.ZS : Rural land area where elevation is below 5 meters (% of total land area)
        AG.LND.EL5M.RU.K2 : Rural land area where elevation is below 5 meters (sq. km)
        AG.LND.CROP.ZS  : Permanent cropland (% of land area)
        AG.LND.CREL.HA  : Land under cereal production (hectares)
        AG.LND.ARBL.ZS  : Arable land (% of land area)
        AG.LND.ARBL.HA.PC : Arable land (hectares per person)
        AG.LND.ARBL.HA  : Arable land (hectares)
        AG.LND.AGRI.ZS  : Agricultural land (% of land area)
        AG.LND.AGRI.K2  : Agricultural land (sq. km)
        AG.CON.FERT.ZS  : Fertilizer consumption (kilograms per hectare of arable land)
        AG.CON.FERT.PT.ZS : Fertilizer consumption (% of fertilizer production)
        AG.AGR.TRAC.NO  : Agricultural machinery, tractors

        """
        return self._features
    #edef

    @property
    def countries_iso3(self):
        """
        Return a list of countries represented in this dataset in iso3 format
        """
        return self._countries_iso3
    #edef

    @property
    def countries(self):
        """
        Return a list of countries represented in this dataset.
        """
        return self._countries
    #edef
#eclass
