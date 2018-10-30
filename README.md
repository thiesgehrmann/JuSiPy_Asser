# ASSer challenge

Todos
================

- Read the documents given here
  - Proposed:
    - [https://www.hackathonforgood.org/asser-institute/](https://www.hackathonforgood.org/asser-institute/)
    - [https://www.tni.org/files/download/landgrabbingprimer-feb2013.pdf](https://www.tni.org/files/download/landgrabbingprimer-feb2013.pdf)
    - [http://www.srfood.org/images/stories/pdf/officialreports/20140310\_finalreport\_en.pdf](http://www.srfood.org/images/stories/pdf/officialreports/20140310_finalreport_en.pdf)
  - Suggested in [Readings](#readings)
- Datasets:
  - Past land deals and acquisitions -\&gt; Adonis
  - Investment contracts for land -\&gt; Manos
  - Media notifications of land acquisitions -\&gt; Marios
  - Land registries around the world -\&gt; Mixalis
  - Government corruption perceptions -\&gt; Stelios
  - Land cover classifications -\&gt; Thies
  - Elevation and population data sets -\&gt; Adonis

**NOTE: Most of these datasets seem to be listed also here:** [**https://landportal.org/book/datasets**](https://landportal.org/book/datasets) **It might be that they aggregate data from those sources, and give them to us…**

**Adding to that:** [**https://datahub.io/search**](https://datahub.io/search)

Google Jupyter Notebook
================
[https://colab.research.google.com/drive/1Bdz4OaSsLHPxHA3RTtaLwwRcH\_\_45AFa](https://colab.research.google.com/drive/1Bdz4OaSsLHPxHA3RTtaLwwRcH__45AFa)

Types of data
================

**Past land deals and acquisitions**

LandMatrix has basically everything about previous land acquisitions (.csv, .xml , .xls)

[https://landmatrix.org/en/get-the-detail/database.csv/?download\_format=csv](https://landmatrix.org/en/get-the-detail/database.csv/?download_format=csv)

Give information about target country and specifically targeted region and investor country and the reason of the grabbing ( farming, crops, mining etc etc)

Comments from:

&quot;Large scale foreign acquisitions of land in developing countries. Risks, opportunities and new actors&quot;

- Land grabbing is concentrated into specific target and origin countries
- In mainly for agriculture (67%  \&lt;- mostly for biofuels) and forests (20%)
- Developing countries are most commonly involved in land grabbing
- The number of deals that are needed for a specific region varies per origin country (Figure 2,3)
- South-South deals becoming increasingly common
- private-public partnerships has increased
- In host countries, governments are often engaged in negotiating investment deals
-  there is an increase in the share of production of basic foods

**Geocoding**

Retrieve a lat/long from an address. Or reverse, retrieve an address from a lat/long pair.

\*in python: [https://www.datacamp.com/community/tutorials/geospatial-data-python](https://www.datacamp.com/community/tutorials/geospatial-data-python)

**Land Cover Classifications**

Used to describe land use. Is a specific location water/dry land/forest/agricultural land/urban land etc. Also can be used to describe how this land changes in recent years.

[https://lpdaac.usgs.gov/dataset\_discovery](https://lpdaac.usgs.gov/dataset_discovery)

[http://glcf.umd.edu/data/landcover/data.shtml](http://glcf.umd.edu/data/landcover/data.shtml)

**Elevation and population**

Population density (people per sq. km of land area): [https://datahub.io/world-bank/en.pop.dnst](https://datahub.io/world-bank/en.pop.dnst)

[https://freegisdata.rtwilson.com/](https://freegisdata.rtwilson.com/)

[https://www2.jpl.nasa.gov/srtm/](https://www2.jpl.nasa.gov/srtm/)

[https://www.ngdc.noaa.gov/ngdcinfo/onlineaccess.html](https://www.ngdc.noaa.gov/ngdcinfo/onlineaccess.html) (this is perhaps not for us exactly, but to have for now)

[https://www.lib.ncsu.edu/gis/esridm/2004/help/images/world/gtopo\_1km.htm](https://www.lib.ncsu.edu/gis/esridm/2004/help/images/world/gtopo_1km.htm)

**Land registries around the world**

Indication of datasets and their properties for some countries:[https://index.okfn.org/dataset/land/](https://index.okfn.org/dataset/land/)

What to expect in terms of features(check the land registry section): [https://cadasta.org/open-data/overview-of-property-rights-data/](https://cadasta.org/open-data/overview-of-property-rights-data/)

Datasets from the UK(most diverse country for this kind of data so far, some are under an Open Government Registry, other are free, one is under restricted license): [https://www.gov.uk/topic/land-registration/data](https://www.gov.uk/topic/land-registration/data)

Example of parsing and analysis of one of the UK datasets(.csv):

[https://www.kaggle.com/stephaniejones/land-registry-data/kernels](https://www.kaggle.com/stephaniejones/land-registry-data/kernels)

Converting .SUP/.CXF files to shapefiles for GIS: [https://github.com/bopen/bgeo.catasto](https://github.com/bopen/bgeo.catasto)

**Government corruption perceptions**

DATA-type: Simple tabular data with an index (score) of corruption assigned per country per year since 1995 by transparency.org

Reading: [https://ourworldindata.org/corruption](https://ourworldindata.org/corruption)

DATAsets:

- [https://www.transparency.org/research/cpi](https://www.transparency.org/research/cpi)
- [https://datahub.io/core/corruption-perceptions-index](https://datahub.io/core/corruption-perceptions-index)

**Investment contracts for land**
- [http://pubs.iied.org/pdfs/12578IIED.pdf](http://pubs.iied.org/pdfs/12578IIED.pdf)
- [https://openlandcontracts.org/contract/ocds-591adf-0122591393/view#/](https://openlandcontracts.org/contract/ocds-591adf-0122591393/view#/)
- [http://pubs.iied.org/pdfs/12568IIED.pdf](http://pubs.iied.org/pdfs/12568IIED.pdf)

Readings
================
- The debate over big land data (article)
[https://www.ft.com/content/df31f666-0a43-3a0e-a747-ec72f2efb40c](https://www.ft.com/content/df31f666-0a43-3a0e-a747-ec72f2efb40c)
- Methodological reflections on &#39;land grab&#39;databases and the &#39;land grab&#39;literature &#39;rush&#39; (paper)
[https://eprints.soas.ac.uk/16795/](https://eprints.soas.ac.uk/16795/)
- Land grab/data grab: precision agriculture and its new horizons (paper)
[https://www.tandfonline.com/doi/full/10.1080/03066150.2017.1415887?scroll=top&amp;needAccess=true](https://www.tandfonline.com/doi/full/10.1080/03066150.2017.1415887?scroll=top&amp;needAccess=true)
- Global Map of &quot;Land Grabs&quot; By Country and By Sector

[http://www.circleofblue.org/LAND.html](http://www.circleofblue.org/LAND.html)

Existing Data
================
- The Online Public Database on Land Deals
[https://landmatrix.org/en/](https://landmatrix.org/en/)
- GRAIN releases data set with over 400 global land grabs [https://www.grain.org/article/entries/4479-grain-releases-data-set-with-over-400-global-land-grabs](https://www.grain.org/article/entries/4479-grain-releases-data-set-with-over-400-global-land-grabs)

Existing Methods
================
[https://github.com/edwardsfriedman/land-grab](https://github.com/edwardsfriedman/land-grab)

Dashboard creation
================
- [https://blog.sicara.com/bokeh-dash-best-dashboard-framework-python-shiny-alternative-c5b576375f7f](https://blog.sicara.com/bokeh-dash-best-dashboard-framework-python-shiny-alternative-c5b576375f7f)
- [https://dash.plot.ly/getting-started-part-2#interactivity](https://dash.plot.ly/getting-started-part-2#interactivity)
