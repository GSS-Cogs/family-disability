#!/usr/bin/env python
# coding: utf-8
# %%
from gssutils import *

scraper = Scraper('https://digital.nhs.uk/data-and-information/publications/statistical/adult-social-care-activity-and-finance-report')
scraper.select_dataset(latest=True)
tab = next(t for t in scraper.distributions[0].as_databaker() if t.name == 'T1')


# %% [markdown]
# In source data Age row has empty cells to define all ages, age definitions share activity cells to map observations
# Regions data not included in tidy data due to missing geography codes

# %%
cell = tab.filter('Geography code')
cell.assert_one()
activity = cell.shift(4,0).fill(RIGHT).is_not_blank().is_not_whitespace()
age = cell.fill(RIGHT).is_not_blank().is_not_whitespace() |\
             cell.shift(0,1).fill(RIGHT).is_not_blank().is_not_whitespace()
code = cell.shift(1,0).fill(DOWN).is_not_blank().is_not_whitespace()
observations = code.shift(3,0).fill(RIGHT).is_not_blank().is_not_whitespace()
Dimensions = [
            HDim(code, 'NHS Geography', DIRECTLY, LEFT),
            HDimConst('Period', 'gregorian-interval/2018-04-01T00:00:00/P1Y'),
            HDim(age,'Adult Social Care group',DIRECTLY, ABOVE),
            HDimConst('Unit','gbp-thousands'),  
            HDimConst('Measure Type','GBP Total'),
            HDim(activity, 'Adult Social Care activity', CLOSEST, LEFT)
]  
c1 = ConversionSegment(observations, Dimensions, processTIMEUNIT=True)
new_table = c1.topandas()
import numpy as np
new_table.rename(columns={'OBS': 'Value','DATAMARKER': 'NHS Marker'}, inplace=True)
def user_perc(x):
    
    if ((str(x) == '18 to 64')) | ((str(x) == '65 and over')): 
        
        return str(x)
    else:
        return 'all ages'    
new_table['Adult Social Care group'] = new_table.apply(lambda row: user_perc(row['Adult Social Care group']), axis = 1)
new_table['Adult Social Care group'] = new_table['Adult Social Care group'].map(
    lambda x: {
        '18 to 64' : 'age 18 to 64 ', 
        '65 and over' : 'age 65 and over'}.get(x, x))
def user_perc2(x,y):
    
    if ((str(x) ==  'Net Total Expenditure') | (str(x) ==  'Gross Total Expenditure') | (str(x) ==  'Net Total Expenditure')) : 
        
        return y
    else:
        return 'clients'
    
new_table['Unit'] = new_table.apply(lambda row: user_perc2(row['Adult Social Care activity'], row['Unit']), axis = 1)
def user_perc3(x,y):
    
    if ((str(x) ==  'Net Total Expenditure') | (str(x) ==  'Gross Total Expenditure') | (str(x) ==  'Net Total Expenditure')): 
        
        return y
    else:
        return 'Count'
    
new_table['Measure Type'] = new_table.apply(lambda row: user_perc3(row['Adult Social Care activity'], row['Measure Type']), axis = 1)
new_table = new_table [['NHS Geography','Period','Adult Social Care group','Adult Social Care activity','Unit','Value','Measure Type']]
