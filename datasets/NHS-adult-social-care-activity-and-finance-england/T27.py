#!/usr/bin/env python
# coding: utf-8
# %%
from gssutils import *

scraper = Scraper('https://digital.nhs.uk/data-and-information/publications/statistical/adult-social-care-activity-and-finance-report')
scraper.select_dataset(latest=True)
tab = next(t for t in scraper.distributions[0].as_databaker() if t.name == 'T27')


# %%
cell = tab.filter('Age band')
cell.assert_one()
activity = cell.shift(3,0).fill(RIGHT).is_not_blank().is_not_whitespace() \
            .filter(lambda x: type(x.value) != 'per' not in x.value)
group = cell.shift(1,0).fill(DOWN).is_not_blank().is_not_whitespace()
age = cell.fill(DOWN).is_not_blank().is_not_whitespace()
code = cell.shift(1,0).fill(DOWN).is_not_blank().is_not_whitespace()
observations = activity.fill(DOWN).is_not_blank().is_not_whitespace()
Dimensions = [
            HDim(code,'NHS Geography',DIRECTLY,LEFT),
            HDimConst('Period', 'gregorian-interval/2018-04-01T00:00:00/P1Y'),
            HDim(activity,'Adult Social Care activity',DIRECTLY, ABOVE),
            HDimConst('Unit','GBP'),  
            HDimConst('Measure Type','number'),
            HDim(age, 'Adult Social Care group',CLOSEST,LEFT)
]  
c1 = ConversionSegment(observations, Dimensions, processTIMEUNIT=True)
new_table = c1.topandas()
import numpy as np
new_table.rename(columns={'OBS': 'Value','DATAMARKER': 'NHS Marker'}, inplace=True)
new_table['Adult Social Care group'] = new_table['Adult Social Care group'].map(
    lambda x: {
        '18 to 64' : 'age 18 to 64 ', 
        '65 and over' : 'age 65 and over'}.get(x, x))
new_table['Adult Social Care group'] = new_table['group'] + ' - ' + new_table['Adult Social Care group']
new_table = new_table [['NHS Geography','Period','Adult Social Care group','Adult Social Care activity','Unit','Value','Measure Type','NHS Marker']]

# %%
