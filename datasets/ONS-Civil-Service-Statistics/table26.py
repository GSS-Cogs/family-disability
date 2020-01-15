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


#  Table: 26   Civil Service employment; median earnings by region and responsibility level
# - All Employees 
# - Earnings

tabs = {tab.name: tab for tab in scraper.distribution(latest=True).as_databaker()}
tab = tabs['Table 26']

responsibility_level = tab.excel_ref('C5').expand(RIGHT).is_not_blank()
area_code = tab.excel_ref('A8').fill(DOWN) - tab.excel_ref('A25').expand(DOWN)
region = tab.excel_ref('B8').fill(DOWN).is_not_blank() - tab.excel_ref('B25').expand(DOWN)
observations = responsibility_level.fill(DOWN).is_not_blank() - tab.excel_ref('B25').expand(DOWN).expand(RIGHT)
#savepreviewhtml(observations)

dimensions = [
    HDimConst('Measure Type', 'median-earnings'),
    HDimConst('Year', '2018'),
    HDimConst('ONS Age Range', 'all'),
    HDimConst('Ethnicity', 'all'),
    HDimConst('Nationality', 'all'),
    HDimConst('Salary Band', 'all'),
    HDimConst('Sex', 'all'),
    HDimConst('Profession of Post', 'not-applicable'),
    HDimConst('Entrants or Leavers', 'not-applicable'),
    HDimConst('Type of Employment', 'full-time-employees'),
    HDimConst('Status of Employment', 'not-applicable'),
    HDimConst('NUTS Area Code', 'not-applicable'),
    HDimConst('Department', 'all'),
    HDimConst('Disability Status', 'not-applicable'),
    HDim(area_code, 'ONS area code', DIRECTLY, LEFT), 
    HDim(region, 'Region name', DIRECTLY, LEFT),
    HDim(responsibility_level, 'Responsibility Level', DIRECTLY, ABOVE), 
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

new_table['Region name'] = new_table['Region name'].map(lambda x: pathify(x))
new_table['Responsibility Level'] = new_table['Responsibility Level'].map(lambda x: pathify(x))
new_table
