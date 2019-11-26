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

# State-funded primary, secondary and special schools (1,2): Number of pupils with special educational needs by national curriculum year group

from gssutils import *
scraper = Scraper('https://www.gov.uk/government/statistics/special-educational-needs-in-england-january-2019')
tabs = { tab.name: tab for tab in scraper.distributions[1].as_databaker() }
tab = tabs['Table 4']
cell = tab.filter('England')
academy = tab.excel_ref('B').expand(DOWN).by_index([10,24,38,57])
pupils = cell.shift(0,3).fill(RIGHT).is_not_blank().is_not_whitespace()
ncgroup = tab.excel_ref('C').expand(DOWN).is_not_blank().is_not_whitespace()
observations1 = pupils.fill(DOWN).is_number().is_not_blank().is_not_whitespace() - tab.excel_ref('C74').expand(RIGHT)
Dimensions1 = [
            HDimConst('Geography', 'E92000001'),
            HDimConst('Period','2019'),
            HDim(academy,'Education provider',CLOSEST,ABOVE),
            HDimConst('Unit','children'),  
            HDimConst('Measure Type','Count'),
            HDim(pupils, 'Special need type', DIRECTLY, ABOVE),
            HDim(ncgroup,'Special support type',DIRECTLY,LEFT)
            ] 
c1 = ConversionSegment(observations1, Dimensions1, processTIMEUNIT=True)
new_table = c1.topandas()
import numpy as np
new_table.rename(columns={'OBS': 'Value'}, inplace=True)
new_table['Value'] = new_table['Value'].astype(int)
new_table['Age']  = 'All'
new_table['Sex']  = 'All'
new_table['Special support type'] = new_table['Special support type'].str.rstrip('(3)')
new_table = new_table [['Geography','Period','Education provider','Special support type', 'Special need type','Age','Sex','Unit','Value','Measure Type']]
