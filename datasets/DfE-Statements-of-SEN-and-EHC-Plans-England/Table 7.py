# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:light
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.3.3
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

from gssutils import *
scraper = Scraper('https://www.gov.uk/government/collections/statistics-special-educational-needs-sen')

scraper

scraper.select_dataset(title=lambda x: x.startswith('Statements of SEN and EHC Plans'), latest=True)

scraper

tabs = { tab.name: tab for tab in scraper.distributions[2].as_databaker() }

tab = tabs['Table 7']

# +
cell = tab.filter('LA code')
cell.assert_one()
geo = cell.fill(DOWN).is_not_blank().is_not_whitespace()
Year = tab.filter(contains_string('Year'))
plantype = tab.filter(contains_string('Number of children'))
age = cell.shift(0,1).fill(RIGHT).is_not_blank().is_not_whitespace()
observations = geo.shift(2,0).fill(RIGHT).is_not_blank().is_not_whitespace()
Dimensions = [
            HDim(geo,'Geography',DIRECTLY,LEFT),
            HDim(Year,'Year', CLOSEST,LEFT),
            HDim(age,'DfE Age Groups',DIRECTLY,ABOVE),
            HDim(plantype,'Statements or EHC Plan Type',CLOSEST, ABOVE),
            HDimConst('Unit','children'),  
            HDimConst('Measure Type','Count'),
            HDimConst('Statements of SEN or EHC Plan Description', 'Children and young people with an EHC plan by local authority and age group')
    
]  
c1 = ConversionSegment(observations, Dimensions, processTIMEUNIT=True)
new_table = c1.topandas()
import numpy as np
new_table.rename(columns={'OBS': 'Value','DATAMARKER': 'NHS Marker'}, inplace=True)
new_table['Year'] = 'Year/' + new_table['Year'].astype(str).str[-4:]
new_table['DfE Age Groups'] = new_table['DfE Age Groups'].map(
    lambda x: {
        'Total' : 'all ages'}.get(x, x))
new_table['Statements of SEN or EHC Plan Provider'] = 'all'
