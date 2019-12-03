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

# State-funded primary, secondary and special schools (1,2): Pupils with special educational needs by age (3) and gender (4,5)

from gssutils import *
scraper = Scraper('https://www.gov.uk/government/collections/statistics-special-educational-needs-sen')
scraper.select_dataset(title=lambda x: x.startswith('Special educational needs in England'), latest=True)
tabs = { tab.name: tab for tab in scraper.distributions[3].as_databaker() }
tab = tabs['Table F']
cell = tab.filter('England')
pupils = cell.fill(DOWN).is_not_blank().is_not_whitespace()
sen = cell.shift(0,3).fill(RIGHT).is_not_blank().is_not_whitespace() \
        .filter(lambda x: type(x.value) != '%' not in x.value)
support = cell.shift(0,2).fill(RIGHT).is_not_blank().is_not_whitespace() 
observations1 = sen.fill(DOWN).is_number().is_not_blank().is_not_whitespace() 
Dimensions1 = [
            HDimConst('Geography', 'E92000001'),
            HDimConst('Period','2019'),
            HDimConst('Education provider','state-funded-primary-secondary-and-special-schools'),
            HDimConst('Unit','children'),  
            HDimConst('Measure Type','Count'),
            HDim(pupils, 'Special need type', DIRECTLY, LEFT),
            HDim(support,'Special support type', CLOSEST,LEFT),
            HDim(sen,'sen', DIRECTLY,ABOVE),
            HDimConst('Sex','all'),
            HDimConst('Age','all')            
]
c1 = ConversionSegment(observations1, Dimensions1, processTIMEUNIT=True)
new_table = c1.topandas()
import numpy as np
new_table.rename(columns={'OBS': 'Value'}, inplace=True)
new_table['Value'] = new_table['Value'].astype(int)
new_table['Special support type'] = new_table['sen'] + '-' + new_table['Special support type']
new_table['Special support type'] = new_table['Special support type'].str.lower()
new_table = new_table [['Geography','Period','Education provider','Special support type', 'Special need type','Age','Sex','Unit','Value','Measure Type']]
