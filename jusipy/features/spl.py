#"""
#API_1_DS2_en_csv_v2_10181830.csv
#https://data.worldbank.org/topic/agriculture-and-rural-development?view=chart
#"""

import pandas as pd
import os
dir_path = os.path.dirname(os.path.realpath(__file__))

class SPL(object):
    """
    Social Protection & Labor

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

        m = pd.read_csv('jusipy/features/SPL_API_10_DS2_en_csv_v2_10189431.csv', skiprows=3)
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
        SL.WAG.0714.ZS  : Children in employment, wage workers (% of children in employment, ages 7-14)
        SL.WAG.0714.MA.ZS : Children in employment, wage workers, male (% of male children in employment, ages 7-14)
        SL.WAG.0714.FE.ZS : Children in employment, wage workers, female (% of female children in employment, ages 7-14)
        SL.UEM.TOTL.ZS  : Unemployment, total (% of total labor force) (modeled ILO estimate)
        SL.UEM.TOTL.NE.ZS : Unemployment, total (% of total labor force) (national estimate)
        SL.UEM.TOTL.MA.ZS : Unemployment, male (% of male labor force) (modeled ILO estimate)
        SL.UEM.TOTL.MA.NE.ZS : Unemployment, male (% of male labor force) (national estimate)
        SL.UEM.TOTL.FE.ZS : Unemployment, female (% of female labor force) (modeled ILO estimate)
        SL.UEM.TOTL.FE.NE.ZS : Unemployment, female (% of female labor force) (national estimate)
        SL.UEM.NEET.ZS  : Share of youth not in education, employment or training, total (% of youth population)
        SL.UEM.NEET.MA.ZS : Share of youth not in education, employment or training, male (% of male youth population)
        SL.UEM.NEET.FE.ZS : Share of youth not in education, employment or training, female (% of female youth population)
        SL.UEM.INTM.ZS  : Unemployment with intermediate education (% of total labor force with intermediate education)
        SL.UEM.INTM.MA.ZS : Unemployment with intermediate education, male (% of male labor force with intermediate education)
        SL.UEM.INTM.FE.ZS : Unemployment with intermediate education, female (% of female labor force with intermediate education)
        SL.UEM.BASC.ZS  : Unemployment with basic education (% of total labor force with basic education)
        SL.UEM.BASC.MA.ZS : Unemployment with basic education, male (% of male labor force with basic education)
        SL.UEM.BASC.FE.ZS : Unemployment with basic education, female (% of female labor force with basic education)
        SL.UEM.ADVN.ZS  : Unemployment with advanced education (% of total labor force with advanced education)
        SL.UEM.ADVN.MA.ZS : Unemployment with advanced education, male (% of male labor force with advanced education)
        SL.UEM.ADVN.FE.ZS : Unemployment with advanced education, female (% of female labor force with advanced education)
        SL.UEM.1524.ZS  : Unemployment, youth total (% of total labor force ages 15-24) (modeled ILO estimate)
        SL.UEM.1524.NE.ZS : Unemployment, youth total (% of total labor force ages 15-24) (national estimate)
        SL.UEM.1524.MA.ZS : Unemployment, youth male (% of male labor force ages 15-24) (modeled ILO estimate)
        SL.UEM.1524.MA.NE.ZS : Unemployment, youth male (% of male labor force ages 15-24) (national estimate)
        SL.UEM.1524.FE.ZS : Unemployment, youth female (% of female labor force ages 15-24) (modeled ILO estimate)
        SL.UEM.1524.FE.NE.ZS : Unemployment, youth female (% of female labor force ages 15-24) (national estimate)
        SL.TLF.TOTL.IN  : Labor force, total
        SL.TLF.TOTL.FE.ZS : Labor force, female (% of total labor force)
        SL.TLF.PART.ZS  : Part time employment, total (% of total employment)
        SL.TLF.PART.MA.ZS : Part time employment, male (% of total male employment)
        SL.TLF.PART.FE.ZS : Part time employment, female (% of total female employment)
        SL.TLF.INTM.ZS  : Labor force with intermediate education (% of total working-age population with intermediate education)
        SL.TLF.INTM.MA.ZS : Labor force with intermediate education, male (% of male working-age population with intermediate education)
        SL.TLF.INTM.FE.ZS : Labor force with intermediate education, female (% of female working-age population with intermediate education)
        SL.TLF.CACT.ZS  : Labor force participation rate, total (% of total population ages 15+) (modeled ILO estimate)
        SL.TLF.CACT.NE.ZS : Labor force participation rate, total (% of total population ages 15+) (national estimate)
        SL.TLF.CACT.MA.ZS : Labor force participation rate, male (% of male population ages 15+) (modeled ILO estimate)
        SL.TLF.CACT.MA.NE.ZS : Labor force participation rate, male (% of male population ages 15+) (national estimate)
        SL.TLF.CACT.FM.ZS : Ratio of female to male labor force participation rate (%) (modeled ILO estimate)
        SL.TLF.CACT.FM.NE.ZS : Ratio of female to male labor force participation rate (%) (national estimate)
        SL.TLF.CACT.FE.ZS : Labor force participation rate, female (% of female population ages 15+) (modeled ILO estimate)
        SL.TLF.CACT.FE.NE.ZS : Labor force participation rate, female (% of female population ages 15+) (national estimate)
        SL.TLF.BASC.ZS  : Labor force with basic education (% of total working-age population with basic education)
        SL.TLF.BASC.MA.ZS : Labor force with basic education, male (% of male working-age population with basic education)
        SL.TLF.BASC.FE.ZS : Labor force with basic education, female (% of female working-age population with basic education)
        SL.TLF.ADVN.ZS  : Labor force with advanced education (% of total working-age population with advanced education)
        SL.TLF.ADVN.MA.ZS : Labor force with advanced education, male (% of male working-age population with advanced education)
        SL.TLF.ADVN.FE.ZS : Labor force with advanced education, female (% of female working-age population with advanced education)
        SL.TLF.ACTI.ZS  : Labor force participation rate, total (% of total population ages 15-64) (modeled ILO estimate)
        SL.TLF.ACTI.MA.ZS : Labor force participation rate, male (% of male population ages 15-64) (modeled ILO estimate)
        SL.TLF.ACTI.FE.ZS : Labor force participation rate, female (% of female population ages 15-64) (modeled ILO estimate)
        SL.TLF.ACTI.1524.ZS : Labor force participation rate for ages 15-24, total (%) (modeled ILO estimate)
        SL.TLF.ACTI.1524.NE.ZS : Labor force participation rate for ages 15-24, total (%) (national estimate)
        SL.TLF.ACTI.1524.MA.ZS : Labor force participation rate for ages 15-24, male (%) (modeled ILO estimate)
        SL.TLF.ACTI.1524.MA.NE.ZS : Labor force participation rate for ages 15-24, male (%) (national estimate)
        SL.TLF.ACTI.1524.FE.ZS : Labor force participation rate for ages 15-24, female (%) (modeled ILO estimate)
        SL.TLF.ACTI.1524.FE.NE.ZS : Labor force participation rate for ages 15-24, female (%) (national estimate)
        SL.TLF.0714.ZS  : Children in employment, total (% of children ages 7-14)
        SL.TLF.0714.WK.ZS : Children in employment, work only (% of children in employment, ages 7-14)
        SL.TLF.0714.WK.TM : Average working hours of children, working only, ages 7-14 (hours per week)
        SL.TLF.0714.WK.MA.ZS : Children in employment, work only, male (% of male children in employment, ages 7-14)
        SL.TLF.0714.WK.MA.TM : Average working hours of children, working only, male, ages 7-14 (hours per week)
        SL.TLF.0714.WK.FE.ZS : Children in employment, work only, female (% of female children in employment, ages 7-14)
        SL.TLF.0714.WK.FE.TM : Average working hours of children, working only, female, ages 7-14 (hours per week)
        SL.TLF.0714.SW.ZS : Children in employment, study and work (% of children in employment, ages 7-14)
        SL.TLF.0714.SW.TM : Average working hours of children, study and work, ages 7-14 (hours per week)
        SL.TLF.0714.SW.MA.ZS : Children in employment, study and work, male (% of male children in employment, ages 7-14)
        SL.TLF.0714.SW.MA.TM : Average working hours of children, study and work, male, ages 7-14 (hours per week)
        SL.TLF.0714.SW.FE.ZS : Children in employment, study and work, female (% of female children in employment, ages 7-14)
        SL.TLF.0714.SW.FE.TM : Average working hours of children, study and work, female, ages 7-14 (hours per week)
        SL.TLF.0714.MA.ZS : Children in employment, male (% of male children ages 7-14)
        SL.TLF.0714.FE.ZS : Children in employment, female (% of female children ages 7-14)
        SL.SRV.EMPL.ZS  : Employment in services (% of total employment) (modeled ILO estimate)
        SL.SRV.EMPL.MA.ZS : Employment in services, male (% of male employment) (modeled ILO estimate)
        SL.SRV.EMPL.FE.ZS : Employment in services, female (% of female employment) (modeled ILO estimate)
        SL.SRV.0714.ZS  : Child employment in services (% of economically active children ages 7-14)
        SL.SRV.0714.MA.ZS : Child employment in services, male (% of male economically active children ages 7-14)
        SL.SRV.0714.FE.ZS : Child employment in services, female (% of female economically active children ages 7-14)
        SL.SLF.0714.ZS  : Children in employment, self-employed (% of children in employment, ages 7-14)
        SL.SLF.0714.MA.ZS : Children in employment, self-employed, male (% of male children in employment, ages 7-14)
        SL.SLF.0714.FE.ZS : Children in employment, self-employed, female (% of female children in employment, ages 7-14)
        SL.MNF.0714.ZS  : Child employment in manufacturing (% of economically active children ages 7-14)
        SL.MNF.0714.MA.ZS : Child employment in manufacturing, male (% of male economically active children ages 7-14)
        SL.MNF.0714.FE.ZS : Child employment in manufacturing, female (% of female economically active children ages 7-14)
        SL.ISV.IFRM.ZS  : Informal employment (% of total non-agricultural employment)
        SL.ISV.IFRM.MA.ZS : Informal employment, male (% of total non-agricultural employment)
        SL.ISV.IFRM.FE.ZS : Informal employment, female (% of total non-agricultural employment)
        SL.IND.EMPL.ZS  : Employment in industry (% of total employment) (modeled ILO estimate)
        SL.IND.EMPL.MA.ZS : Employment in industry, male (% of male employment) (modeled ILO estimate)
        SL.IND.EMPL.FE.ZS : Employment in industry, female (% of female employment) (modeled ILO estimate)
        SL.GDP.PCAP.EM.KD : GDP per person employed (constant 2011 PPP $)
        SL.FAM.WORK.ZS  : Contributing family workers, total (% of total employment) (modeled ILO estimate)
        SL.FAM.WORK.MA.ZS : Contributing family workers, male (% of male employment) (modeled ILO estimate)
        SL.FAM.WORK.FE.ZS : Contributing family workers, female (% of female employment) (modeled ILO estimate)
        SL.FAM.0714.ZS  : Children in employment, unpaid family workers (% of children in employment, ages 7-14)
        SL.FAM.0714.MA.ZS : Children in employment, unpaid family workers, male (% of male children in employment, ages 7-14)
        SL.FAM.0714.FE.ZS : Children in employment, unpaid family workers, female (% of female children in employment, ages 7-14)
        SL.EMP.WORK.ZS  : Wage and salaried workers, total (% of total employment) (modeled ILO estimate)
        SL.EMP.WORK.MA.ZS : Wage and salaried workers, male (% of male employment) (modeled ILO estimate)
        SL.EMP.WORK.FE.ZS : Wage and salaried workers, female (% of female employment) (modeled ILO estimate)
        SL.EMP.VULN.ZS  : Vulnerable employment, total (% of total employment) (modeled ILO estimate)
        SL.EMP.VULN.MA.ZS : Vulnerable employment, male (% of male employment) (modeled ILO estimate)
        SL.EMP.VULN.FE.ZS : Vulnerable employment, female (% of female employment) (modeled ILO estimate)
        SL.EMP.TOTL.SP.ZS : Employment to population ratio, 15+, total (%) (modeled ILO estimate)
        SL.EMP.TOTL.SP.NE.ZS : Employment to population ratio, 15+, total (%) (national estimate)
        SL.EMP.TOTL.SP.MA.ZS : Employment to population ratio, 15+, male (%) (modeled ILO estimate)
        SL.EMP.TOTL.SP.MA.NE.ZS : Employment to population ratio, 15+, male (%) (national estimate)
        SL.EMP.TOTL.SP.FE.ZS : Employment to population ratio, 15+, female (%) (modeled ILO estimate)
        SL.EMP.TOTL.SP.FE.NE.ZS : Employment to population ratio, 15+, female (%) (national estimate)
        SL.EMP.SMGT.FE.ZS : Female share of employment in senior and middle management (%)
        SL.EMP.SELF.ZS  : Self-employed, total (% of total employment) (modeled ILO estimate)
        SL.EMP.SELF.MA.ZS : Self-employed, male (% of male employment) (modeled ILO estimate)
        SL.EMP.SELF.FE.ZS : Self-employed, female (% of female employment) (modeled ILO estimate)
        SL.EMP.MPYR.ZS  : Employers, total (% of total employment) (modeled ILO estimate)
        SL.EMP.MPYR.MA.ZS : Employers, male (% of male employment) (modeled ILO estimate)
        SL.EMP.MPYR.FE.ZS : Employers, female (% of female employment) (modeled ILO estimate)
        SL.EMP.1524.SP.ZS : Employment to population ratio, ages 15-24, total (%) (modeled ILO estimate)
        SL.EMP.1524.SP.NE.ZS : Employment to population ratio, ages 15-24, total (%) (national estimate)
        SL.EMP.1524.SP.MA.ZS : Employment to population ratio, ages 15-24, male (%) (modeled ILO estimate)
        SL.EMP.1524.SP.MA.NE.ZS : Employment to population ratio, ages 15-24, male (%) (national estimate)
        SL.EMP.1524.SP.FE.ZS : Employment to population ratio, ages 15-24, female (%) (modeled ILO estimate)
        SL.EMP.1524.SP.FE.NE.ZS : Employment to population ratio, ages 15-24, female (%) (national estimate)
        SL.AGR.EMPL.ZS  : Employment in agriculture (% of total employment) (modeled ILO estimate)
        SL.AGR.EMPL.MA.ZS : Employment in agriculture, male (% of male employment) (modeled ILO estimate)
        SL.AGR.EMPL.FE.ZS : Employment in agriculture, female (% of female employment) (modeled ILO estimate)
        SL.AGR.0714.ZS  : Child employment in agriculture (% of economically active children ages 7-14)
        SL.AGR.0714.MA.ZS : Child employment in agriculture, male (% of male economically active children ages 7-14)
        SL.AGR.0714.FE.ZS : Child employment in agriculture, female (% of female economically active children ages 7-14)
        per_si_allsi.cov_q5_tot : Coverage of social insurance programs in richest quintile (% of population)
        per_si_allsi.cov_q4_tot : Coverage of social insurance programs in 4th quintile (% of population)
        per_si_allsi.cov_q3_tot : Coverage of social insurance programs in 3rd quintile (% of population)
        per_si_allsi.cov_q2_tot : Coverage of social insurance programs in 2nd quintile (% of population)
        per_si_allsi.cov_q1_tot : Coverage of social insurance programs in poorest quintile (% of population)
        per_si_allsi.cov_pop_tot : Coverage of social insurance programs (% of population)
        per_si_allsi.ben_q1_tot : Benefit incidence of social insurance programs to poorest quintile (% of total social insurance benefits)
        per_si_allsi.adq_pop_tot : Adequacy of social insurance programs (% of total welfare of beneficiary households)
        per_sa_allsa.cov_q5_tot : Coverage of social safety net programs in richest quintile (% of population)
        per_sa_allsa.cov_q4_tot : Coverage of social safety net programs in 4th quintile (% of population)
        per_sa_allsa.cov_q3_tot : Coverage of social safety net programs in 3rd quintile (% of population)
        per_sa_allsa.cov_q2_tot : Coverage of social safety net programs in 2nd quintile (% of population)
        per_sa_allsa.cov_q1_tot : Coverage of social safety net programs in poorest quintile (% of population)
        per_sa_allsa.cov_pop_tot : Coverage of social safety net programs (% of population)
        per_sa_allsa.ben_q1_tot : Benefit incidence of social safety net programs to poorest quintile (% of total safety net benefits)
        per_sa_allsa.adq_pop_tot : Adequacy of social safety net programs (% of total welfare of beneficiary households)
        per_lm_alllm.cov_q5_tot : Coverage of unemployment benefits and ALMP in richest quintile (% of population)
        per_lm_alllm.cov_q4_tot : Coverage of unemployment benefits and ALMP in 4th quintile (% of population)
        per_lm_alllm.cov_q3_tot : Coverage of unemployment benefits and ALMP in 3rd quintile (% of population)
        per_lm_alllm.cov_q2_tot : Coverage of unemployment benefits and ALMP in 2nd quintile (% of population)
        per_lm_alllm.cov_q1_tot : Coverage of unemployment benefits and ALMP in poorest quintile (% of population)
        per_lm_alllm.cov_pop_tot : Coverage of unemployment benefits and ALMP (% of population)
        per_lm_alllm.ben_q1_tot : Benefit incidence of unemployment benefits and ALMP to poorest quintile (% of total U/ALMP benefits)
        per_lm_alllm.adq_pop_tot : Adequacy of unemployment benefits and ALMP (% of total welfare of beneficiary households)
        per_allsp.cov_pop_tot : Coverage of social protection and labor programs (% of population)
        per_allsp.ben_q1_tot : Benefit incidence of social protection and labor programs to poorest quintile (% of total SPL benefits)
        per_allsp.adq_pop_tot : Adequacy of social protection and labor programs (% of total welfare of beneficiary households)

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
