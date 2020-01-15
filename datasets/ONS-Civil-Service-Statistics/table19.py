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


# Table 19 : Civil Service employment by region and age

tabs = {tab.name: tab for tab in scraper.distribution(latest=True).as_databaker()}
tab = tabs['Table 19']

area_code = tab.excel_ref('A8').expand(DOWN).is_not_blank() - tab.excel_ref('A28').expand(DOWN)
region = tab.excel_ref('B8').expand(DOWN).is_not_blank() - tab.excel_ref('B28').expand(DOWN)
age_group = tab.excel_ref('D5').expand(RIGHT).is_not_blank() - tab.excel_ref('L5').expand(RIGHT)
observations = age_group.fill(DOWN).is_not_blank() - tab.excel_ref('B28').expand(RIGHT).expand(DOWN)
#savepreviewhtml(area_code)

dimensions = [
    HDimConst('Measure Type', 'headcount'),
    HDimConst('Year', '2018'),
    HDimConst('Sex', 'all'),
    HDimConst('Ethnicity', 'all'),
    HDimConst('Nationality', 'all'),
    HDimConst('Salary Band', 'all'),
    HDimConst('Profession of Post', 'not-applicable'),
    HDimConst('Entrants or Leavers', 'not-applicable'),
    HDimConst('Department', 'not-applicable'),
    HDimConst('Type of Employment', 'all-employees'),
    HDimConst('Status of Employment', 'not-applicable'),
    HDimConst('NUTS Area Code', 'not-applicable'),
    HDimConst('Responsibility Level', 'all'),
    HDimConst('Disability Status', 'not-applicable'),
    HDim(age_group, 'ONS Age Range', DIRECTLY, ABOVE),
    HDim(area_code, 'ONS area code', CLOSEST, ABOVE), 
    HDim(region, 'Region name', CLOSEST, ABOVE),
]
c1 = ConversionSegment(observations, dimensions, processTIMEUNIT=True)
new_table = c1.topandas()
savepreviewhtml(c1)

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

new_table['ONS Age Range'] = new_table['ONS Age Range'].map(lambda x: pathify(x))
new_table['Region name'] = new_table['Region name'].map(lambda x: pathify(x))
new_table
