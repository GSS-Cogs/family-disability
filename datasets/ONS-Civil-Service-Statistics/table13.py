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


# Table 13 : Civil Service employment; regional distribution12

tabs = {tab.name: tab for tab in scraper.distribution(latest=True).as_databaker()}
tab = tabs['Table 13']

#gender_type = ['Male', 'Female', 'Total']
employment_status = tab.excel_ref('B5').expand(RIGHT).is_not_blank()
gender = tab.excel_ref('B6').expand(RIGHT).is_not_blank()
employment_type = tab.excel_ref('B7').expand(RIGHT).is_not_blank()
region = tab.excel_ref('B10').expand(DOWN).is_not_blank() - tab.excel_ref('B30').expand(DOWN)
area_code = tab.excel_ref('A10').expand(DOWN) - tab.excel_ref('A30').expand(DOWN)
observations = employment_type.fill(DOWN).is_not_blank() - tab.excel_ref('B30').expand(DOWN).expand(RIGHT)
#savepreviewhtml(area_code)

# +
dimensions = [
    HDimConst('Measure Type', 'headcount'),
    HDimConst('Year', '2018'),
    HDimConst('Ethnicity', 'all'),
    HDimConst('Disability Status', 'not-applicable'),
    HDimConst('ONS Age Range', 'All'),
    HDimConst('Nationality', 'All'),
    HDimConst('Responsibility Level', 'All'),
    HDimConst('Salary Band', 'All'),
    HDimConst('Profession of Post', 'not-applicable'),
    HDimConst('Entrants or Leavers', 'not-applicable'),
    HDimConst('Department', 'not-applicable'),
    HDimConst('NUTS Area Code', 'not-applicable'),
    HDim(employment_type, 'Type of Employment', DIRECTLY, ABOVE),
    HDim(gender, 'Sex', CLOSEST, LEFT),
    HDim(employment_status, 'Status of Employment', CLOSEST, LEFT),
    HDim(region, 'Region name', DIRECTLY, LEFT),
    HDim(area_code, 'ONS area code', DIRECTLY, LEFT),  
    
]
c1 = ConversionSegment(observations, dimensions, processTIMEUNIT=True)
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
new_table['Region name'] = new_table['Region name'].map(lambda x: pathify(x))
new_table['Sex'] = new_table['Sex'].map(lambda x: pathify(x))
new_table = new_table.replace({'Sex' : {'male' : 'M','female' : 'F','total' : 'T' }})
new_table = new_table.replace({'Type of Employment' : {'Full Time' : 'Full Time Employees','Part Time' : 'Part Time Employees','Total' : 'All Employees' }})
new_table['Type of Employment'] = new_table['Type of Employment'].map(lambda x: pathify(x))
new_table['Status of Employment'] = new_table['Status of Employment'].map(lambda x: pathify(x))

new_table


