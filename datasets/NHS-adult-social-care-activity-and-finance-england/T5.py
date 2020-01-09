#!/usr/bin/env python
# coding: utf-8
# %%
from gssutils import *

scraper = Scraper('https://digital.nhs.uk/data-and-information/publications/statistical/adult-social-care-activity-and-finance-report')
scraper.select_dataset(latest=True)
tab = next(t for t in scraper.distributions[0].as_databaker() if t.name == 'T5')


# %%
cell = tab.filter('Geography code')
cell.assert_one()
Type = cell.fill(RIGHT).is_not_blank().is_not_whitespace() 
year = cell.shift(0,1).fill(RIGHT).is_not_blank().is_not_whitespace()
code = cell.shift(1,0).fill(DOWN).is_not_blank().is_not_whitespace()
observations = code.shift(3,0).fill(RIGHT).is_not_blank().is_not_whitespace()
Dimensions = [
            HDim(code, 'NHS Geography', DIRECTLY, LEFT),
            HDim(Type,'Adult Social Care group',CLOSEST, LEFT),
            HDim(year,'Period',DIRECTLY,ABOVE),
            HDimConst('Unit','gbp-thousands'),  
            HDimConst('Measure Type','GBP Total'),
            HDimConst('Adult Social Care activity', 'Expenditure')
]  
c1 = ConversionSegment(observations, Dimensions, processTIMEUNIT=True)
new_table = c1.topandas()
import numpy as np
new_table.rename(columns={'OBS': 'Value'}, inplace=True)
new_table['Period'] = new_table['Period'].map(
    lambda x: f'gregorian-interval/{str(x)[:4]}-03-31T00:00:00/P1Y')
new_table = new_table [['NHS Geography','Period','Adult Social Care group','Adult Social Care activity','Unit','Value','Measure Type']]
