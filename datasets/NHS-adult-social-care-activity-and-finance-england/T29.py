#!/usr/bin/env python
# coding: utf-8
# %%
from gssutils import *

scraper = Scraper('https://digital.nhs.uk/data-and-information/publications/statistical/adult-social-care-activity-and-finance-report')
scraper.select_dataset(latest=True)
tab = next(t for t in scraper.distributions[0].as_databaker() if t.name == 'T29')


# %%
cell = tab.filter('Age band')
cell.assert_one()
activity = cell.shift(2,0).fill(RIGHT).is_not_blank().is_not_whitespace() \
            .filter(lambda x: type(x.value) != 'per' not in x.value)
age = cell.expand(DOWN).is_not_blank().is_not_whitespace()
group = cell.shift(1,0).fill(DOWN).is_not_blank().is_not_whitespace()
observations = activity.fill(DOWN).is_not_blank().is_not_whitespace()
Dimensions = [
            HDimConst('NHS Geography', 'all'),
            HDim(group,'Adult Social Care group', DIRECTLY, LEFT),
            HDim(age,'group',CLOSEST,ABOVE),
            HDimConst('Period', 'gregorian-interval/2018-04-01T00:00:00/P1Y'),
            HDimConst('Unit','GBP'),  
            HDimConst('Measure Type','thousands'),
            HDim(activity, 'Adult Social Care activity',DIRECTLY,ABOVE)
]  
c1 = ConversionSegment(observations, Dimensions, processTIMEUNIT=True)
new_table = c1.topandas()
import numpy as np
new_table.rename(columns={'OBS': 'Value','DATAMARKER': 'NHS Marker'}, inplace=True)
def user_perc(x):
    
    if ((str(x) == '18 to 64')) | ((str(x) == '65 and Over')): 
        
        return str(x)
    else:
        return 'all ages'    
new_table['group'] = new_table.apply(lambda row: user_perc(row['group']), axis = 1)
new_table['group'] = new_table['group'].map(
    lambda x: {
        '18 to 64' : 'age 18 to 64 ', 
        '65 and over' : 'age 65 and over'}.get(x, x))
new_table['Adult Social Care group'] = new_table['Adult Social Care group'] + ' - ' + new_table['group']
new_table['NHS Marker'] = ''
new_table = new_table [['NHS Geography','Period','Adult Social Care group','Adult Social Care activity','Unit','Value','Measure Type','NHS Marker']]
