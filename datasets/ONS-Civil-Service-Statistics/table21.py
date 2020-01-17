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


# Table 21 :Civil Service employment; responsibility level by government department Full-Time Equivalent

tabs = {tab.name: tab for tab in scraper.distribution(latest=True).as_databaker()}
tab = tabs['Table 21']

department = tab.excel_ref('B9').fill(DOWN).is_not_blank() - tab.excel_ref('B193').expand(DOWN)
responsibility_level = tab.excel_ref('C5').expand(RIGHT).is_not_blank()
observations = responsibility_level.fill(DOWN).is_not_blank() - tab.excel_ref('B194').expand(DOWN).expand(RIGHT)
#savepreviewhtml(department)

dimensions = [
    HDimConst('Measure Type', 'headcount'),
    HDimConst('Year', '2018'),
    HDimConst('Sex', 'U'),
    HDimConst('ONS Age Range', 'all'),
    HDimConst('Ethnicity', 'all'),
    HDimConst('Nationality', 'all'),
    HDimConst('Salary Band', 'all'),
    HDimConst('Profession of Post', 'all'),
    HDimConst('Entrants or Leavers', 'not-applicable'),
    HDimConst('Type of Employment', 'full-time-equivalent'),
    HDimConst('Status of Employment', 'not-applicable'),
    HDimConst('NUTS Area Code', 'not-applicable'),
    HDimConst('ONS area code', 'not-applicable'),
    HDimConst('Region name', 'not-applicable'), 
    HDimConst('Disability Status', 'not-applicable'),
    HDim(department, 'Department', DIRECTLY, LEFT), 
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

new_table['Department'] = new_table['Department'].map(lambda x: pathify(x))
new_table['Responsibility Level'] = new_table['Responsibility Level'].map(lambda x: pathify(x))
new_table
