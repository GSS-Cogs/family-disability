# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:light
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.4'
#       jupytext_version: 1.1.1
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

# Special schools (1,2): Number and percentage of pupils with special educational needs by primary type of need (3)

from gssutils import *
scraper = Scraper('https://www.gov.uk/government/collections/statistics-special-educational-needs-sen')
scraper.select_dataset(title=lambda x: x.startswith('Special educational needs in England'), latest=True)
tabs = { tab.name: tab for tab in scraper.distributions[2].as_databaker() }
tab = tabs['Table 18']
cell = tab.filter('LA Code')
cell.assert_one()
geography = cell.fill(DOWN).is_not_blank().is_not_whitespace()              
typeofprovision = cell.shift(0,1).fill(RIGHT).is_not_blank().is_not_whitespace() 
Percentages = tab.filter(contains_string('%')).fill(DOWN)
observations = geography.shift(2,0).fill(RIGHT).is_not_blank().is_not_whitespace() - Percentages
Dimensions = [
            HDim(geography,'Geography', DIRECTLY, LEFT),
            HDimConst('Period', '2019'),
            HDimConst('Education provider','special-schools'),
            HDimConst('Unit','children'),  
            HDimConst('Measure Type','Count'),
            HDim(typeofprovision, 'Special need type', DIRECTLY, ABOVE)
]  
c1 = ConversionSegment(observations, Dimensions, processTIMEUNIT=True)
new_table = c1.topandas()
import numpy as np
new_table.rename(columns={'OBS': 'Value'}, inplace=True)
new_table = new_table[new_table['Value'] !=  '' ]
new_table['Value'] = new_table['Value'].astype(int)
new_table['Special support type'] = 'primary-need'
new_table['Age']  = 'All'
new_table['Sex']  = 'All'
new_table = new_table [['Geography','Period','Education provider','Special support type', 'Special need type','Age','Sex','Unit','Value','Measure Type']]


