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

# Table 2a: Academies (1,2): pupils with special educational needs by type of academy

from gssutils import *
scraper = Scraper('https://www.gov.uk/government/statistics/special-educational-needs-in-england-january-2019')
tabs = { tab.name: tab for tab in scraper.distributions[1].as_databaker() }
tab = tabs['Table 2']
cell = tab.filter('England')
academy = cell.fill(DOWN).is_not_blank().is_not_whitespace()
support = cell.shift(0,2).fill(RIGHT).is_not_blank().is_not_whitespace()
observations1 = support.fill(DOWN).is_number().is_not_blank().is_not_whitespace() - tab.excel_ref('J6').expand(DOWN).expand(RIGHT)
Dimensions1 = [
            HDimConst('Geography', 'E92000001'),
            HDimConst('Period','2019'),
            HDim(academy,'Education provider',DIRECTLY, LEFT),
            HDimConst('Unit','children'),  
            HDimConst('Measure Type','Count'),
            HDim(support, 'Special need type', DIRECTLY, ABOVE)
] 
c1 = ConversionSegment(observations1, Dimensions1, processTIMEUNIT=True)
new_table = c1.topandas()
import numpy as np
new_table.rename(columns={'OBS': 'Value'}, inplace=True)
new_table['Value'] = new_table['Value'].astype(int)
new_table['Special support type'] = 'Academy'
new_table['Age']  = 'All'
new_table['Sex']  = 'All'
new_table = new_table [['Geography','Period','Education provider','Special support type', 'Special need type','Age','Sex','Unit','Value','Measure Type']]
