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

# All Schools (1): Number of pupils with a statement or EHC plan, based on where the child attends school

from gssutils import *
scraper = Scraper('https://www.gov.uk/government/collections/statistics-special-educational-needs-sen')
scraper.select_dataset(title=lambda x: x.startswith('Special educational needs in England'), latest=True)
tabs = { tab.name: tab for tab in scraper.distributions[2].as_databaker() }
tab = tabs['Table 12']
cell = tab.filter('LA Code')
cell.assert_one()
Year = cell.fill(RIGHT).is_not_blank().is_not_whitespace()
geography = cell.fill(DOWN).is_not_blank().is_not_whitespace()              
typeofprovision = cell.shift(0,1).fill(RIGHT).is_not_blank().is_not_whitespace() \
                    .filter(lambda x: type(x.value) != '%' not in x.value)
Percentages = tab.filter(contains_string('%')).fill(DOWN)
observations = geography.shift(3,0).fill(RIGHT).is_not_blank().is_not_whitespace() - Percentages
Dimensions = [
            HDim(geography,'Geography', CLOSEST,ABOVE),
            HDim(Year,'Period', CLOSEST,LEFT),
            HDimConst('Education provider','Local Authority all schools'),
            HDimConst('Unit','children'),  
            HDimConst('Measure Type','Count'),
            HDim(typeofprovision, 'Special need type', DIRECTLY, ABOVE)
]  
c1 = ConversionSegment(observations, Dimensions, processTIMEUNIT=True)
new_table = c1.topandas()
import numpy as np
new_table.rename(columns={'OBS': 'Value'}, inplace=True)
new_table = new_table[new_table['Value'] !=  '' ]
new_table['Value'] = new_table['Value'].astype(int)
new_table['Period'] = pd.to_numeric(new_table['Period'], errors='coerce').fillna(0)
new_table['Period'] = new_table['Period'].astype('Int64')
new_table['Special support type'] = 'statement-or-ehc-plan'
new_table['Age']  = 'All'
new_table['Sex']  = 'All'
new_table = new_table [['Geography','Period','Education provider','Special support type', 'Special need type','Age','Sex','Unit','Value','Measure Type']]


