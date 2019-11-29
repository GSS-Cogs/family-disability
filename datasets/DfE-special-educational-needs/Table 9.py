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

# Special schools (1,2): types of provision for which schools have been approved (3)

from gssutils import *
scraper = Scraper('https://www.gov.uk/government/collections/statistics-special-educational-needs-sen')
scraper.select_dataset(title=lambda x: x.startswith('Special educational needs in England'), latest=True)
tabs = { tab.name: tab for tab in scraper.distributions[1].as_databaker() }
tab = tabs['Table 9']
cell = tab.filter('England')
schoolprovision = cell.fill(DOWN).is_not_blank().is_not_whitespace()
schooltype = cell.shift(0,2).fill(RIGHT).is_not_blank().is_not_whitespace()
observations1 = schooltype.fill(DOWN).is_number().is_not_blank().is_not_whitespace() 
Dimensions1 = [
            HDimConst('Geography', 'E92000001'),
            HDimConst('Period','2019'),
            HDim(schoolprovision,'Special need type',DIRECTLY, LEFT),
            HDimConst('Unit','children'),  
            HDimConst('Measure Type','Count'),
            HDim(schooltype, 'Education provider', DIRECTLY, ABOVE)
] 
c1 = ConversionSegment(observations1, Dimensions1, processTIMEUNIT=True)
new_table = c1.topandas()
import numpy as np
new_table.rename(columns={'OBS': 'Value'}, inplace=True)
new_table['Value'] = new_table['Value'].astype(int)
new_table['Age']  = 'All'
new_table['Sex']  = 'All'
new_table['Special support type'] = 'School provision'
new_table = new_table [['Geography','Period','Education provider','Special support type', 'Special need type','Age','Sex','Unit','Value','Measure Type']]
