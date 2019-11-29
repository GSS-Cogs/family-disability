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

# State-funded primary, secondary and special schools (1,2): number of pupils with special educational needs by ethnic group

from gssutils import *
scraper = Scraper('https://www.gov.uk/government/collections/statistics-special-educational-needs-sen')
scraper.select_dataset(title=lambda x: x.startswith('Special educational needs in England'), latest=True)
tabs = { tab.name: tab for tab in scraper.distributions[1].as_databaker() }
tab = tabs['Table 8']
cell = tab.filter('England')
typeofschool = cell.shift(0,2).expand(RIGHT).is_not_blank().is_not_whitespace()
primaryneed = cell.fill(DOWN).is_not_blank().is_not_whitespace()
pupil = typeofschool.shift(0,1).expand(RIGHT).is_not_blank().is_not_whitespace()
observations1 = pupil.fill(DOWN).is_number().is_not_blank().is_not_whitespace()
Dimensions1 = [
            HDimConst('Geography', 'E92000001'),
            HDimConst('Period','2019'),
            HDim(typeofschool,'Education provider',CLOSEST, LEFT),
            HDim(primaryneed, 'Special support type',DIRECTLY, LEFT ),
            HDimConst('Unit','children'),  
            HDimConst('Measure Type','Count'),
            HDim(pupil, 'Special need type', DIRECTLY,ABOVE)
            ]   
c1 = ConversionSegment(observations1, Dimensions1, processTIMEUNIT=True)
new_table = c1.topandas()
import numpy as np
new_table.rename(columns={'OBS': 'Value'}, inplace=True)
new_table['Value'] = new_table['Value'].astype(int)
new_table['Age']  = 'All'
new_table['Sex']  = 'All'
new_table['Special support type'] = new_table['Special support type'].str.rstrip('4()')
new_table['Special need type'] = new_table['Special need type'].str.rstrip('5()')
new_table = new_table [['Geography','Period','Education provider','Special support type', 'Special need type','Age','Sex','Unit','Value','Measure Type']]
