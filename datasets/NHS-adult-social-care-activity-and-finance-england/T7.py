#!/usr/bin/env python
# coding: utf-8
# %%
from gssutils import *

scraper = Scraper('https://digital.nhs.uk/data-and-information/publications/statistical/adult-social-care-activity-and-finance-report')
scraper.select_dataset(latest=True)
tab = next(t for t in scraper.distributions[0].as_databaker() if t.name == 'T7')

# %%
cell = tab.filter('Geography code')
cell.assert_one()
income = cell.fill(RIGHT).is_not_blank().is_not_whitespace() \
        .filter(lambda x: type(x.value) != 'Percentage' not in x.value)
activity = cell.shift(0,1).fill(RIGHT).is_not_blank().is_not_whitespace()
age = cell.shift(0,2).fill(RIGHT)
code = cell.shift(1,0).fill(DOWN).is_not_blank().is_not_whitespace()
observations = code.shift(3,0).fill(RIGHT).is_not_blank().is_not_whitespace()
obs1 = age.shift(0,13).fill(DOWN).is_not_blank().is_not_whitespace()
obs2 = observations - obs1
Dimensions1 = [
            HDim(code, 'NHS Geography', DIRECTLY, LEFT),
            HDim(activity,'Adult Social Care group',CLOSEST,LEFT),
            HDim(age,'group',DIRECTLY,ABOVE),
            HDimConst('Period', 'gregorian-interval/2018-04-01T00:00:00/P1Y'),
            HDimConst('Unit','GBP'),  
            HDimConst('Measure Type','Thousands'),
            HDim(income,'Adult Social Care activity', CLOSEST,LEFT)
]  
c1 = ConversionSegment(observations, Dimensions1, processTIMEUNIT=True)
new_table = c1.topandas()
import numpy as np
new_table.rename(columns={'OBS': 'Value'}, inplace=True)


# %% [markdown]
# There are missing labels in this section of total of all finances, need to verify from source owner

# %%
def user_perc2(x,y):
    
    if ((str(x) ==  'Long Term Care') |  (str(x) ==  'Short Term Care') |(str(x) ==  'Other') & (str(y) == '18 to 64')) | ((str(y) == '65 and Over')): 
        
        return str(y)
    else:
        return 'all ages'
    
new_table['group'] = new_table.apply(lambda row: user_perc2(row['Adult Social Care group'], row['group']), axis = 1)
def user_perc1(x,y):
    
    if ((str(x) ==  'Long Term Care') |  (str(x) ==  'Short Term Care') |(str(x) ==  'Other') & (str(y) == '18 to 64')) | ((str(y) == '65 and Over')): 
        
        return str(x)
    else:
        return 'total'
    
new_table['Adult Social Care group'] = new_table.apply(lambda row: user_perc1(row['Adult Social Care group'], row['group']), axis = 1)
new_table['Adult Social Care group'] = new_table['Adult Social Care group'] + ' - ' + new_table['group']
new_table = new_table [['NHS Geography','Period','Adult Social Care group','Adult Social Care activity','Unit','Value','Measure Type']]
