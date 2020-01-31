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

tab = tabs['Table 8']

cell = tab.filter('LA code')
cell.assert_one()
geo = cell.fill(DOWN).is_not_blank().is_not_whitespace()
Year = tab.filter(contains_string('Year'))
description = cell.shift(2,0).fill(RIGHT).is_not_blank().is_not_whitespace()
plantype = cell.shift(2,1).fill(RIGHT).is_not_blank().is_not_whitespace() | tab.excel_ref('E6')
per = tab.filter(contains_string('Percentage'))
observations = geo.shift(2,0).fill(RIGHT).is_not_blank().is_not_whitespace() - per.fill(DOWN)
Dimensions = [
            HDim(geo,'Geography',DIRECTLY,LEFT),
            HDim(Year,'Year', CLOSEST,LEFT),
            HDim(description,'Statements of SEN or EHC Plan Description',CLOSEST,LEFT),
            HDimConst('Unit','children'),  
            HDimConst('Measure Type','Count'),
            HDim(plantype,'Statements or EHC Plan Type', CLOSEST,LEFT)
]  
c1 = ConversionSegment(observations, Dimensions, processTIMEUNIT=True)
new_table = c1.topandas()
import numpy as np
new_table.rename(columns={'OBS': 'Value','DATAMARKER': 'Marker'}, inplace=True)
new_table['Year'] = 'Year/' + new_table['Year'].astype(str).str[-4:]
new_table['DfE Age Groups'] = 'all ages'
new_table['Statements of SEN or EHC Plan Provider'] = 'all'

new_table['Statements or EHC Plan Type'] = new_table['Statements or EHC Plan Type'].map(
    lambda x: {
        'Number of initial requests that were made for assessment for an EHC plan during the 2018 calendar year' : 'New EHC Plans', 
        'Number' : 'New EHC Plans',
        'Percentage1': 'New EHC Plans' ,
        'Percentage2': 'New EHC Plans',
        'Total' : 'All Plans',
        'Other' : 'EHC Plans Other'       
        }.get(x, x))
