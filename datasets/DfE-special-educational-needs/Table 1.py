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

# All Schools (1) : Pupils with special educational needs by Education provider and type of provision (2)(3)

from gssutils import *
scraper = Scraper('https://www.gov.uk/government/statistics/special-educational-needs-in-england-january-2019')
tabs = { tab.name: tab for tab in scraper.distributions[1].as_databaker() }
tab = tabs['Table 1']
cell = tab.filter('England')
cell.assert_one()
Year = cell.shift(0,2).fill(RIGHT).is_not_blank().is_not_whitespace()
schooltype = cell.fill(DOWN).is_not_blank().is_not_whitespace() |\
             cell.shift(1,0).fill(DOWN).is_not_blank().is_not_whitespace()
typeofprovision = cell.shift(2,0).fill(DOWN).is_not_blank().is_not_whitespace()
observations = typeofprovision.fill(RIGHT).is_not_blank().is_not_whitespace()
Dimensions = [
            HDimConst('Geography', 'E92000001'),
            HDim(Year,'Period', DIRECTLY,ABOVE),
            HDim(schooltype,'Education provider',CLOSEST, ABOVE),
            HDimConst('Unit','children'),  
            HDimConst('Measure Type','Count'),
            HDim(typeofprovision, 'Special need type', DIRECTLY, LEFT)
]  
c1 = ConversionSegment(observations, Dimensions, processTIMEUNIT=True)
new_table = c1.topandas()
import numpy as np
new_table.rename(columns={'OBS': 'Value'}, inplace=True)
new_table['Value'] = new_table['Value'].astype(int)
new_table['Period'] = pd.to_numeric(new_table['Period'], errors='coerce').fillna(0)
new_table['Period'] = new_table['Period'].astype('Int64')
new_table['Special support type'] = 'Provision'
new_table['Age']  = 'All'
new_table['Sex']  = 'All'
new_table['Education provider'] = new_table['Education provider'].str.rstrip('(4)')
new_table['Education provider'] = new_table['Education provider'].str.lower()
new_table = new_table [['Geography','Period','Education provider','Special support type', 'Special need type','Age','Sex','Unit','Value','Measure Type']]
