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


gender_type = ['Male', 'Female', 'Total']
tabs = {tab.name: tab for tab in scraper.distribution(latest=True).as_databaker()}
tab = tabs['Table 9'] #Entrants and leavers to the Civil Service by sex and responsibility level 

entrants_leavers = tab.excel_ref('B5').expand(RIGHT).is_not_blank()
gender = tab.excel_ref('C6').expand(RIGHT).is_not_blank()
responsibility_level = tab.excel_ref('B9').fill(DOWN).is_not_blank() - tab.excel_ref('B9') - tab.excel_ref('B21').expand(DOWN)
observations = gender.fill(DOWN).is_not_blank() - tab.excel_ref('B21').expand(RIGHT).expand(DOWN)
savepreviewhtml(entrants_leavers)

# +

dimensions = [
    HDimConst('Measure Type', 'headcount'),
    HDimConst('Year', '2018'),
    HDimConst('Ethnicity', 'all'),
    HDimConst('Disability Status', 'not-applicable'),
    HDimConst('ONS Age Range', 'all'),
    HDimConst('Nationality', 'all'),
    HDimConst('Region name', 'all'),
    HDimConst('NUTS Area Code', 'not-applicable'),
    HDimConst('ONS area code', 'not-applicable'),
    HDimConst('Status of Employment', 'not-applicable'),
    HDimConst('Type of Employment', 'all-employees'),
    HDimConst('Salary Band', 'all'),
    HDimConst('Department', 'all'),
    HDimConst('Profession of Post', 'all'),
    HDim(gender, 'Sex', DIRECTLY, ABOVE),
    HDim(responsibility_level, 'Responsibility Level', DIRECTLY, LEFT),
    HDim(entrants_leavers, 'Entrants or Leavers', CLOSEST, LEFT),
]
c1 = ConversionSegment(observations, dimensions, processTIMEUNIT=True)
savepreviewhtml(c1)
new_table = c1.topandas()
# -

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

new_table['Sex'] = new_table['Sex'].map(lambda x: pathify(x))
new_table = new_table.replace({'Sex' : {'male' : 'M','female' : 'F','total' : 'T' }})
new_table['Entrants or Leavers'] = new_table['Entrants or Leavers'].map(lambda x: pathify(x))
new_table['Responsibility Level'] = new_table['Responsibility Level'].map(lambda x: pathify(x))
new_table = new_table.fillna('not-applicable')
new_table
