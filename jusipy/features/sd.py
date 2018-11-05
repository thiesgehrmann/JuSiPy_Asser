#"""
#API_1_DS2_en_csv_v2_10181830.csv
#https://data.worldbank.org/topic/agriculture-and-rural-development?view=chart
#"""

import pandas as pd
import os
dir_path = os.path.dirname(os.path.realpath(__file__))

class SD(object):
    """
    Social Development indicators

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

        m = pd.read_csv('jusipy/features/SD_API_15_DS2_en_csv_v2_10186395.csv', skiprows=3)
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
        SP.DYN.LE00.MA.IN : Life expectancy at birth, male (years)
        SP.DYN.LE00.FE.IN : Life expectancy at birth, female (years)
        SP.ADO.TFRT     : Adolescent fertility rate (births per 1,000 women ages 15-19)
        SM.POP.REFG.OR  : Refugee population by country or territory of origin
        SM.POP.REFG     : Refugee population by country or territory of asylum
        SL.UEM.TOTL.MA.ZS : Unemployment, male (% of male labor force) (modeled ILO estimate)
        SL.UEM.TOTL.FE.ZS : Unemployment, female (% of female labor force) (modeled ILO estimate)
        SL.TLF.CACT.MA.ZS : Labor force participation rate, male (% of male population ages 15+) (modeled ILO estimate)
        SL.TLF.CACT.FE.ZS : Labor force participation rate, female (% of female population ages 15+) (modeled ILO estimate)
        SL.TLF.ACTI.ZS  : Labor force participation rate, total (% of total population ages 15-64) (modeled ILO estimate)
        SL.TLF.ACTI.MA.ZS : Labor force participation rate, male (% of male population ages 15-64) (modeled ILO estimate)
        SL.TLF.ACTI.FE.ZS : Labor force participation rate, female (% of female population ages 15-64) (modeled ILO estimate)
        SL.TLF.ACTI.1524.ZS : Labor force participation rate for ages 15-24, total (%) (modeled ILO estimate)
        SL.TLF.ACTI.1524.MA.ZS : Labor force participation rate for ages 15-24, male (%) (modeled ILO estimate)
        SL.TLF.ACTI.1524.FE.ZS : Labor force participation rate for ages 15-24, female (%) (modeled ILO estimate)
        SL.TLF.0714.ZS  : Children in employment, total (% of children ages 7-14)
        SL.TLF.0714.WK.ZS : Children in employment, work only (% of children in employment, ages 7-14)
        SL.TLF.0714.WK.MA.ZS : Children in employment, work only, male (% of male children in employment, ages 7-14)
        SL.TLF.0714.WK.FE.ZS : Children in employment, work only, female (% of female children in employment, ages 7-14)
        SL.TLF.0714.SW.ZS : Children in employment, study and work (% of children in employment, ages 7-14)
        SL.TLF.0714.SW.MA.ZS : Children in employment, study and work, male (% of male children in employment, ages 7-14)
        SL.TLF.0714.SW.FE.ZS : Children in employment, study and work, female (% of female children in employment, ages 7-14)
        SL.TLF.0714.MA.ZS : Children in employment, male (% of male children ages 7-14)
        SL.TLF.0714.FE.ZS : Children in employment, female (% of female children ages 7-14)
        SL.EMP.VULN.MA.ZS : Vulnerable employment, male (% of male employment) (modeled ILO estimate)
        SL.EMP.VULN.FE.ZS : Vulnerable employment, female (% of female employment) (modeled ILO estimate)
        SH.HIV.1524.MA.ZS : Prevalence of HIV, male (% ages 15-24)
        SH.HIV.1524.FE.ZS : Prevalence of HIV, female (% ages 15-24)
        SG.GEN.PARL.ZS  : Proportion of seats held by women in national parliaments (%)
        SE.ENR.TERT.FM.ZS : School enrollment, tertiary (gross), gender parity index (GPI)
        SE.ENR.SECO.FM.ZS : School enrollment, secondary (gross), gender parity index (GPI)
        SE.ENR.PRSC.FM.ZS : School enrollment, primary and secondary (gross), gender parity index (GPI)
        SE.ENR.PRIM.FM.ZS : School enrollment, primary (gross), gender parity index (GPI)
        SE.ADT.1524.LT.FM.ZS : Literacy rate, youth (ages 15-24), gender parity index (GPI)

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
