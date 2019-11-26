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

# Table 2b: Academies (1,2): Pupils with special educational needs time series

from gssutils import *
scraper = Scraper('https://www.gov.uk/government/statistics/special-educational-needs-in-england-january-2019')
tabs = { tab.name: tab for tab in scraper.distributions[1].as_databaker() }
tab = tabs['Table 2']
cell = tab.filter('England')
academy1 = tab.excel_ref('L').expand(DOWN).by_index([8,14,20,26])
academy2 = tab.excel_ref('L6').fill(DOWN).is_not_blank().is_not_whitespace() \
            .filter(lambda x: type(x.value) != 'Percentage' not in x.value) \
            - academy1
year = cell.shift(0,2).fill(RIGHT).is_not_blank().is_not_whitespace()
observations1 = academy2.fill(RIGHT).is_number().is_not_blank().is_not_whitespace() 
Dimensions1 = [
            HDimConst('Geography', 'E92000001'),
            HDim(year,'Period',DIRECTLY,ABOVE),
            HDim(academy1,'Education provider',CLOSEST, ABOVE),
            HDim(academy2, 'Special need type',DIRECTLY, LEFT ),
            HDimConst('Unit','children'),  
            HDimConst('Measure Type','Count'),
            ] 
c1 = ConversionSegment(observations1, Dimensions1, processTIMEUNIT=True)
new_table = c1.topandas()
import numpy as np
new_table.rename(columns={'OBS': 'Value'}, inplace=True)
new_table['Value'] = new_table['Value'].astype(int)
new_table['Period'] = pd.to_numeric(new_table['Period'], errors='coerce').fillna(0)
new_table['Period'] = new_table['Period'].astype('Int64')
new_table['Special support type'] = 'Academy'
new_table['Age']  = 'All'
new_table['Sex']  = 'All'
new_table = new_table [['Geography','Period','Education provider','Special support type', 'Special need type','Age','Sex','Unit','Value','Measure Type']]       
