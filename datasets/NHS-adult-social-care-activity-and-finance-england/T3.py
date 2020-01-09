#!/usr/bin/env python
# coding: utf-8
# %%
from gssutils import *

scraper = Scraper('https://digital.nhs.uk/data-and-information/publications/statistical/adult-social-care-activity-and-finance-report')
scraper.select_dataset(latest=True)
tab = next(t for t in scraper.distributions[0].as_databaker() if t.name == 'T3')


# %%
cell = tab.filter('Geography code')
cell.assert_one()
activity = cell.shift(4,0).fill(RIGHT).is_not_blank().is_not_whitespace()
Type = cell.shift(0,1).fill(RIGHT).is_not_blank().is_not_whitespace() \
        .filter(lambda x: type(x.value) != 'Percentage' not in x.value) 
code = cell.shift(1,0).fill(DOWN).is_not_blank().is_not_whitespace()
observations = code.shift(3,0).fill(RIGHT).is_not_blank().is_not_whitespace()
Dimensions = [
            HDim(code, 'NHS Geography', DIRECTLY, LEFT),
            HDim(Type,'Adult Social Care group',CLOSEST, LEFT),
            HDimConst('Unit','gbp-thousands'),  
            HDimConst('Measure Type','GBP Total'),
            HDim(activity, 'Adult Social Care activity', CLOSEST, LEFT)
]  
c1 = ConversionSegment(observations, Dimensions, processTIMEUNIT=True)
new_table = c1.topandas()
import numpy as np
new_table.rename(columns={'OBS': 'Value'}, inplace=True)
def user_perc(x):
    
    if ((str(x) == '2017-18')) | ((str(x) == '2018-19')): 
        
        return str(x)
    else:
        return '2018-19'    
new_table['Period'] = new_table.apply(lambda row: user_perc(row['Adult Social Care group']), axis = 1)
new_table['Period'] = new_table['Period'].map(
    lambda x: f'gregorian-interval/{str(x)[:4]}-03-31T00:00:00/P1Y')
def user_perc2(x):
    
    if ((str(x) == '2017-18')) | ((str(x) == '2018-19')): 
        
        return str('all')
    else:
        return str(x)    
new_table['Adult Social Care group'] = new_table.apply(lambda row: user_perc2(row['Adult Social Care group']), axis = 1)
new_table = new_table [['NHS Geography','Period','Adult Social Care group','Adult Social Care activity','Unit','Value','Measure Type']]
