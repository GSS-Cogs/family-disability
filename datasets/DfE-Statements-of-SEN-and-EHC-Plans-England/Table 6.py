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

tab = tabs['Table 6a']

cell = tab.filter('LA code')
cell.assert_one()
geo = cell.fill(DOWN).is_not_blank().is_not_whitespace()
Year = tab.filter(contains_string('Year'))
provider = cell.fill(RIGHT).is_not_blank().is_not_whitespace() | \
            cell.shift(0,1).fill(RIGHT).is_not_blank().is_not_whitespace()
observations = geo.shift(2,0).fill(RIGHT).is_not_blank().is_not_whitespace()
description = cell.shift(1,0).fill(RIGHT).is_not_blank().is_not_whitespace()
Dimensions = [
            HDim(geo,'Geography',DIRECTLY,LEFT),
            HDim(Year,'Year', CLOSEST,LEFT),
            HDim(provider,'Statements of SEN or EHC Plan Provider',DIRECTLY, ABOVE),
            HDimConst('Unit','children'),  
            HDimConst('Measure Type','Count'),
            HDim(description,'Statements of SEN or EHC Plan Description',CLOSEST,LEFT)
]  
c1 = ConversionSegment(observations, Dimensions, processTIMEUNIT=True)
new_table = c1.topandas()
import numpy as np
new_table.rename(columns={'OBS': 'Value','DATAMARKER': 'Marker'}, inplace=True)
new_table['Year'] = 'Year/' + new_table['Year'].astype(str).str[-4:]
new_table['DfE Age Groups'] = 'all ages'
new_table['Statements or EHC Plan Type'] = 'New EHC Plans'

new_table['Statements of SEN or EHC Plan Provider'] = new_table['Statements of SEN or EHC Plan Provider'].map(
    lambda x: {
        'Number of children and young people for whom EHC plans were made for the first time during the 2018 calendar year' : 'all', 
        'Number of children and young people for whom EHC plans were newly made in 2018 calendar year educated elsewhere' : 'all',
        'Other1': 'all' ,
        'Number of children and young people for whom EHC plans were newly made in the 2018 calendar year who are not in education, employment or training': 'all'
        }.get(x, x)) 
