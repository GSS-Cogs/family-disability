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

# Civil Service Statistics (unvalidated)

# +
import json
import pandas as pd
import numpy as np
from gssutils import *

scraper = Scraper('https://www.ons.gov.uk/employmentandlabourmarket/peopleinwork/publicsectorpersonnel/datasets/civilservicestatistics')
scraper
# -


# Table 15 :Civil Service employment; regional (NUTS3) distribution1 2

tabs = {tab.name: tab for tab in scraper.distribution(latest=True).as_databaker()}
tab = tabs['Table 15']

# +
cells_to_remove = ['B12', 'B17', 'B26', 'B32', 'B39', 'B43', 'B50', 'B54', 'B57', 'B60', 'B67', 'B74',
                   'B79', 'B83', 'B87','B92', 'B102', 'B109', 'B114', 'B123', 'B128', 'B134','B139', 'B143', 
                   'B151', 'B156', 'B163', 'B177', 'B178', 'B184', 'B188', 'B190','B196', 'B205', 'B212', 
                   'B221', 'B230', 'B232']
cells_to_remove2 = ['B11', 'B22', 'B49', 'B66', 'B82', 'B101', 'B122', 'B150', 'B177', 'B195', 'B211', 'B240', ]

nuts_region = tab.excel_ref('B10').expand(DOWN).is_not_blank() - tab.excel_ref('B252').expand(DOWN)
for cell in cells_to_remove:
    nuts_region = nuts_region - tab.excel_ref(cell)
for cell in cells_to_remove2:
    nuts_region = nuts_region - tab.excel_ref(cell)

region = tab.excel_ref('B10').expand(DOWN).is_not_blank() - nuts_region - tab.excel_ref('B252').expand(DOWN)
for cell in cells_to_remove:
    region = region - tab.excel_ref(cell)
# -

gender = tab.excel_ref('B6').expand(RIGHT).is_not_blank()
employment_status = tab.excel_ref('B5').expand(RIGHT).is_not_blank()
employment_type = tab.excel_ref('B7').expand(RIGHT).is_not_blank()
NUTS_code = tab.excel_ref('A12').expand(DOWN) - tab.excel_ref('A252').expand(DOWN)
observations = employment_type.fill(DOWN).is_not_blank() - tab.excel_ref('B252').expand(DOWN).expand(RIGHT)
#savepreviewhtml(observations)

dimensions = [
    HDimConst('Measure Type', 'headcount'),
    HDimConst('Year', '2018'),
    HDimConst('Ethnicity', 'all'),
    HDimConst('Disability Status', 'not-applicable'),
    HDimConst('ONS Age Range', 'all'),
    HDimConst('Nationality', 'all'),
    HDimConst('Responsibility Level', 'all'),
    HDimConst('Salary Band', 'all'),
    HDimConst('Profession of Post', 'not-applicable'),
    HDimConst('Entrants or Leavers', 'not-applicable'),
    HDimConst('Department', 'not-applicable'),
    HDimConst('ONS area code', 'not-applicable'),
    HDim(employment_type, 'Type of Employment', DIRECTLY, ABOVE),
    HDim(gender, 'Sex', CLOSEST, LEFT),
    HDim(employment_status, 'Status of Employment', CLOSEST, LEFT),
    HDim(region, 'Region name', CLOSEST, ABOVE),
    HDim(nuts_region, 'NUTS Region name',DIRECTLY, LEFT ),
    HDim(NUTS_code, 'NUTS Area Code', DIRECTLY, LEFT),
]
c1 = ConversionSegment(observations, dimensions, processTIMEUNIT=True)
new_table = c1.topandas()
savepreviewhtml(c1)


# +
not_reported = new_table['NUTS Region name'] == 'Not reported'
all_employees = new_table['NUTS Region name'] == 'All employees'
overseas = new_table['NUTS Region name'] == 'Overseas'
new_table.loc[not_reported, 'Region name'] = 'not-applicable'
new_table.loc[all_employees, 'Region name'] = 'not-applicable'
new_table.loc[overseas, 'Region name'] = 'not-applicable'

new_table.rename(columns={'OBS': 'Value'}, inplace=True)
if 'DATAMARKER' in new_table.columns:
    print('marker found in columns')
    new_table['DATAMARKER'].replace('..', 'between-one-and-five', inplace=True)
    new_table['DATAMARKER'].replace('-', 'not-applicable', inplace=True)
    new_table = new_table.rename(columns={'DATAMARKER':'Marker'})
    new_table = new_table.fillna('not-applicable') 
else:
    print('marker not found in colmns making it')
    new_table['DATAMARKER'] = 'not-applicable'
    new_table = new_table.rename(columns={'DATAMARKER':'Marker'})
# -

new_table['Type of Employment'] = new_table['Type of Employment'].map(lambda x: pathify(x))
new_table['Status of Employment'] = new_table['Status of Employment'].map(lambda x: pathify(x))
new_table['Region name'] = new_table['Region name'].map(lambda x: pathify(x))
new_table['NUTS Region name'] = new_table['NUTS Region name'].map(lambda x: pathify(x))
new_table['Sex'] = new_table['Sex'].map(lambda x: pathify(x))
new_table = new_table.replace({'Sex' : {'male' : 'M','female' : 'F','total' : 'T' }})
new_table = new_table.replace({'NUTS Area Code' : {'' : 'not-applicable' }})
new_table = new_table.fillna('not-applicable')
new_table
