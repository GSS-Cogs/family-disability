#!/usr/bin/env python
# coding: utf-8
# %%
from gssutils import *

scraper = Scraper('https://digital.nhs.uk/data-and-information/publications/statistical/adult-social-care-activity-and-finance-report')
scraper.select_dataset(latest=True)
tab = next(t for t in scraper.distributions[0].as_databaker() if t.name == 'T9')

# %%
cell = tab.filter('Age band')
cell.assert_one()
support = cell.shift(1,0).fill(DOWN).is_not_blank().is_not_whitespace() 
activity = cell.shift(1,0).fill(RIGHT).is_not_blank().is_not_whitespace()
age = cell.fill(DOWN).is_not_blank().is_not_whitespace()
code = cell.shift(1,0).fill(DOWN).is_not_blank().is_not_whitespace()
observations = activity.fill(DOWN).is_not_blank().is_not_whitespace()

Dimensions1 = [
            HDimConst('NHS Geography', 'all'),
            HDim(support,'Adult Social Care group',DIRECTLY,LEFT),
            HDim(age,'group',CLOSEST,ABOVE),
            HDimConst('Period', 'gregorian-interval/2018-04-01T00:00:00/P1Y'),
            HDimConst('Unit','GBP'),  
            HDimConst('Measure Type','Count'),
            HDim(activity,'Adult Social Care activity',DIRECTLY,ABOVE)
]  
c1 = ConversionSegment(observations, Dimensions1, processTIMEUNIT=True)
new_table = c1.topandas()
import numpy as np
new_table.rename(columns={'OBS': 'Value'}, inplace=True)
new_table['Adult Social Care group'] = new_table['Adult Social Care group'] + ' - ' + new_table['group']
new_table = new_table [['NHS Geography','Period','Adult Social Care group','Adult Social Care activity','Unit','Value','Measure Type']]
