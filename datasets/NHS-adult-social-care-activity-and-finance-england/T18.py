#!/usr/bin/env python
# coding: utf-8
# %%
from gssutils import *

scraper = Scraper('https://digital.nhs.uk/data-and-information/publications/statistical/adult-social-care-activity-and-finance-report')
scraper.select_dataset(latest=True)
tab = next(t for t in scraper.distributions[0].as_databaker() if t.name == 'T18')


# %%
cell = tab.filter('Geography code')
cell.assert_one()
activity = cell.shift(0,1).fill(RIGHT).is_not_blank().is_not_whitespace() \
            .filter(lambda x: type(x.value) != 'per' not in x.value)
age = cell.fill(RIGHT).is_not_blank().is_not_whitespace()
code = cell.shift(1,0).fill(DOWN).is_not_blank().is_not_whitespace()
observations = activity.shift(0,13).fill(DOWN).is_not_blank().is_not_whitespace()
Dimensions = [
            HDim(code, 'NHS Geography', DIRECTLY, LEFT),
            HDim(age,'group', CLOSEST, LEFT),
            HDimConst('Period', 'gregorian-interval/2018-04-01T00:00:00/P1Y'),
            HDimConst('Adult Social Care activity','Gross Current Expenditure on long and short term care combined'),
            HDimConst('Unit','gbp-thousands'),  
            HDimConst('Measure Type','GBP Total'),
            HDim(activity, 'Adult Social Care group',CLOSEST, LEFT)
]  
c1 = ConversionSegment(observations, Dimensions, processTIMEUNIT=True)
new_table = c1.topandas()
import numpy as np
new_table.rename(columns={'OBS': 'Value'}, inplace=True)
def user_perc(x):
    
    if ((str(x) == '18 to 64')) | ((str(x) == '65 and over')): 
        
        return str(x)
    else:
        return 'all ages'    
new_table['group'] = new_table.apply(lambda row: user_perc(row['group']), axis = 1)
new_table['group'] = new_table['group'].map(
    lambda x: {
        '18 to 64' : 'age 18 to 64 ', 
        '65 and over' : 'age 65 and over'}.get(x, x))
new_table['Adult Social Care group'] = new_table['Adult Social Care group'] + ' - ' + new_table['group']
new_table = new_table [['NHS Geography','Period','Adult Social Care group','Adult Social Care activity','Unit','Value','Measure Type']]

# %%
savepreviewhtml(c1)

# %%
