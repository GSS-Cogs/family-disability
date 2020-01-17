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


# Table 16 :Civil Service employment; by region, responsibility level and sex

tabs = {tab.name: tab for tab in scraper.distribution(latest=True).as_databaker()}
tab = tabs['Table 16']

area_code = tab.excel_ref('A9').expand(DOWN).is_not_blank() - tab.excel_ref('A130').expand(DOWN)
region = tab.excel_ref('B9').expand(DOWN).is_not_blank() - tab.excel_ref('B130').expand(DOWN)
responsibility_level = tab.excel_ref('C9').fill(DOWN).is_not_blank() - tab.excel_ref('c130').expand(DOWN)
gender = tab.excel_ref('D5').expand(RIGHT).is_not_blank() - tab.excel_ref('G5').expand(RIGHT)
observations = gender.fill(DOWN).is_not_blank() - tab.excel_ref('C130').expand(DOWN).expand(RIGHT)
#savepreviewhtml(area_code)

dimensions = [
    HDimConst('Measure Type', 'headcount'),
    HDimConst('Year', '2018'),
    HDimConst('Ethnicity', 'all'),
    HDimConst('Disability Status', 'not-applicable'),
    HDimConst('ONS Age Range', 'all'),
    HDimConst('Nationality', 'all'),
    HDimConst('Salary Band', 'all'),
    HDimConst('Profession of Post', 'all'),
    HDimConst('Entrants or Leavers', 'not-applicable'),
    HDimConst('Department', 'all'),
    HDimConst('Type of Employment', 'all-employees'),
    HDimConst('Status of Employment', 'not-applicable'),
    HDimConst('NUTS Area Code', 'not-applicable'),
    HDim(area_code, 'ONS area code', CLOSEST, ABOVE), 
    HDim(responsibility_level, 'Responsibility Level', DIRECTLY, LEFT),
    HDim(region, 'Region name', CLOSEST, ABOVE),
    HDim(gender, 'Sex', DIRECTLY, ABOVE),
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

new_table['Responsibility Level'] = new_table['Responsibility Level'].map(lambda x: pathify(x))
new_table['Sex'] = new_table['Sex'].map(lambda x: pathify(x))
new_table = new_table.replace({'Sex' : {'male' : 'M','female' : 'F','total' : 'T' }})
new_table['Region name'] = new_table['Region name'].map(lambda x: pathify(x))
new_table
