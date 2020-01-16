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


# table 39: Civil Service employment by government department and age1

tabs = {tab.name: tab for tab in scraper.distribution(latest=True).as_databaker()}
tab = tabs['Table 39']

department = tab.excel_ref('B9').expand(DOWN).is_not_blank() - tab.excel_ref('B193').expand(DOWN)
age_group = tab.excel_ref('B5').expand(RIGHT).is_not_blank()
observations = age_group.fill(DOWN).is_not_blank() - tab.excel_ref('B193').expand(DOWN).expand(RIGHT) 
#savepreviewhtml(observations)


dimensions = [
    HDimConst('Year', '2018'),
    HDimConst('Measure Type', 'heacount'),
    HDimConst('Region name', 'all'),
    HDimConst('Nationality', 'all'),
    HDimConst('Salary Band', 'all'),
    HDimConst('Sex', 'all'),
    HDimConst('Ethnicity', 'all'),
    HDimConst('Profession of Post', 'not-applicable'),
    HDimConst('Entrants or Leavers', 'not-applicable'),
    HDimConst('Disability Status', 'not-applicable'),
    HDimConst('Status of Employment', 'not-applicable'),
    HDimConst('Type of Employment', 'all-employees'),
    HDimConst('NUTS Area Code', 'not-applicable'),
    HDimConst('ONS area code', 'not-applicable'),
    HDimConst('Responsibility Level', 'all'),
    HDim(department, 'Department', DIRECTLY, LEFT), 
    HDim(age_group, 'ONS Age Range', DIRECTLY, ABOVE), 
]
c1 = ConversionSegment(observations, dimensions, processTIMEUNIT=True)
new_table = c1.topandas() 

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

new_table['Department'] = new_table['Department'].map(lambda x: pathify(x))
new_table


