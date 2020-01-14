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


# Table 14 :Civil Service employment; regional (NUTS2) distribution1 2

tabs = {tab.name: tab for tab in scraper.distribution(latest=True).as_databaker()}
tab = tabs['Table 14']

#gender_type = ['Male', 'Female', 'Total']
gender = tab.excel_ref('B6').expand(RIGHT).is_not_blank()
employment_type = tab.excel_ref('B7').expand(RIGHT).is_not_blank()
employment_status = tab.excel_ref('B5').expand(RIGHT).is_not_blank()
region = tab.excel_ref('B12').expand(DOWN).is_not_blank() - tab.excel_ref('B11') - tab.excel_ref('B15') - tab.excel_ref('B22') - tab.excel_ref('B28') - tab.excel_ref('B33') - tab.excel_ref('B38') - tab.excel_ref('B43') - tab.excel_ref('B50') - tab.excel_ref('B56') - tab.excel_ref('B62') - tab.excel_ref('B66') - tab.excel_ref('B80').expand(DOWN)
NUTS2_code = tab.excel_ref('A12').expand(DOWN) - tab.excel_ref('A80').expand(DOWN)
observations = employment_type.fill(DOWN).is_not_blank() - tab.excel_ref('B80').expand(DOWN).expand(RIGHT)
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
    HDim(employment_type, 'Employment Type', DIRECTLY, ABOVE),
    HDim(gender, 'Sex', CLOSEST, LEFT),
    HDim(employment_status, 'Employment Status', CLOSEST, LEFT),
    HDim(region, 'Region name', DIRECTLY, LEFT),
    HDim(NUTS2_code, 'NUTS Area Code', DIRECTLY, LEFT),    
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
new_table
