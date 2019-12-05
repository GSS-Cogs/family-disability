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

# State-funded primary and secondary schools (1,2): number of schools with SEN units and resourced provisions(3)

from gssutils import *
scraper = Scraper('https://www.gov.uk/government/collections/statistics-special-educational-needs-sen')
scraper.select_dataset(title=lambda x: x.startswith('Special educational needs in England'), latest=True)
tabs = { tab.name: tab for tab in scraper.distributions[1].as_databaker() }
tab = tabs['Table 11']
cell = tab.filter('England')
typeofschool = cell.shift(0,2).expand(RIGHT).is_not_blank().is_not_whitespace()
resources = typeofschool.shift(-1,1).fill(RIGHT).is_not_blank().is_not_whitespace() \
            .filter(lambda x: type(x.value) != '%' not in x.value)
year = cell.fill(DOWN).is_not_blank().is_not_whitespace()
observations1 = resources.fill(DOWN).is_number().is_not_blank().is_not_whitespace()
Dimensions1 = [
            HDimConst('Geography', 'E92000001'),
            HDim(year,'Period',DIRECTLY,LEFT),
            HDim(typeofschool,'Education provider',CLOSEST, LEFT),
            HDim(resources, 'Special need type',DIRECTLY, ABOVE ),
            HDimConst('Unit','children'),  
            HDimConst('Measure Type','Count')            
            ]
c1 = ConversionSegment(observations1, Dimensions1, processTIMEUNIT=True)
new_table = c1.topandas()
import numpy as np
new_table.rename(columns={'OBS': 'Value'}, inplace=True)
new_table['Value'] = new_table['Value'].astype(int)
new_table['Period'] = pd.to_numeric(new_table['Period'], errors='coerce').fillna(0)
new_table['Period'] = new_table['Period'].astype('Int64')
new_table['Age']  = 'All'
new_table['Sex']  = 'All'
new_table['Special support type'] = 'Resources'
new_table = new_table [['Geography','Period','Education provider','Special support type', 'Special need type','Age','Sex','Unit','Value','Measure Type']]
