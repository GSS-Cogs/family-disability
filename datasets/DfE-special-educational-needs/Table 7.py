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

# State-funded primary, secondary and special schools (1,2): number and percentage of pupils with special educational needs by first language (3)

from gssutils import *
scraper = Scraper('https://www.gov.uk/government/collections/statistics-special-educational-needs-sen')
scraper.select_dataset(title=lambda x: x.startswith('Special educational needs in England'), latest=True)
tabs = { tab.name: tab for tab in scraper.distributions[1].as_databaker() }
tab = tabs['Table 7']
cell = tab.filter('England')
academy = cell.fill(DOWN).is_not_blank().is_not_whitespace()
pupils = cell.shift(0,3).fill(RIGHT).is_not_blank().is_not_whitespace()
language = tab.excel_ref('C').expand(DOWN).is_not_blank().is_not_whitespace() 
observations1 = pupils.fill(DOWN).is_number().is_not_blank().is_not_whitespace() 
Dimensions1 = [
            HDimConst('Geography', 'E92000001'),
            HDimConst('Period','2019'),
            HDim(academy,'Education provider',CLOSEST,ABOVE),
            HDimConst('Unit','children'),  
            HDimConst('Measure Type','Count'),
            HDim(pupils, 'Special need type', DIRECTLY, ABOVE),
            HDim(language,'Special support type',DIRECTLY,LEFT)
            ]
c1 = ConversionSegment(observations1, Dimensions1, processTIMEUNIT=True)
new_table = c1.topandas()
import numpy as np
new_table.rename(columns={'OBS': 'Value'}, inplace=True)
new_table['Value'] = new_table['Value'].astype(int)
new_table['Age']  = 'All'
new_table['Sex']  = 'All'
new_table['Special support type'] = new_table['Special support type'].str.rstrip('(4)')
new_table['Special support type'] = new_table['Special support type'].str.rstrip('(4)')
new_table = new_table [['Geography','Period','Education provider','Special support type', 'Special need type','Age','Sex','Unit','Value','Measure Type']]
