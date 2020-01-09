#!/usr/bin/env python
# coding: utf-8
# %%
from gssutils import *

scraper = Scraper('https://digital.nhs.uk/data-and-information/publications/statistical/adult-social-care-activity-and-finance-report')
scraper.select_dataset(latest=True)
tab = next(t for t in scraper.distributions[0].as_databaker() if t.name == 'T16')


# %%
cell = tab.filter('Geography code')
cell.assert_one()
activity = cell.shift(4,1).fill(RIGHT).is_not_blank().is_not_whitespace() \
            .filter(lambda x: type(x.value) != 'per' not in x.value)
year = cell.fill(RIGHT).is_not_blank().is_not_whitespace()
code = cell.shift(1,0).fill(DOWN).is_not_blank().is_not_whitespace()
observations = activity.shift(0,13).fill(DOWN).is_not_blank().is_not_whitespace()
Dimensions = [
            HDim(code, 'NHS Geography', DIRECTLY, LEFT),
            HDim(year,'Period',CLOSEST, LEFT),
            HDimConst('Adult Social Care activity','Gross Current Expenditure'),
            HDimConst('Unit','gbp-thousands'),  
            HDimConst('Measure Type','GBP Total'),
            HDim(activity, 'Adult Social Care group',DIRECTLY,ABOVE)
]  
c1 = ConversionSegment(observations, Dimensions, processTIMEUNIT=True)
new_table = c1.topandas()
import numpy as np
new_table.rename(columns={'OBS': 'Value'}, inplace=True)
new_table['Period'] = new_table['Period'].map(
    lambda x: f'gregorian-interval/{str(x)[:4]}-03-31T00:00:00/P1Y')
def user_perc2(x,y):
    
    if (str(x) ==  'Population') : 
        
        return 'clients'
    else:
        return y
    
new_table['Unit'] = new_table.apply(lambda row: user_perc2(row['Adult Social Care group'], row['Unit']), axis = 1)
def user_perc3(x,y):
    
    if (str(x) ==  'Population'): 
        
        return 'Count'
    else:
        return y
    
new_table['Measure Type'] = new_table.apply(lambda row: user_perc3(row['Adult Social Care group'], row['Measure Type']), axis = 1)

new_table = new_table [['NHS Geography','Period','Adult Social Care group','Adult Social Care activity','Unit','Value','Measure Type']]
