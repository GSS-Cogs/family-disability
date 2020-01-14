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
tab = tabs['Table 8'] #Civil Service employment; profession by government department

profession_of_post = tab.excel_ref('C5').expand(RIGHT).is_not_blank() 
department = tab.excel_ref('B9').fill(DOWN).is_not_blank() - tab.excel_ref('B16') - tab.excel_ref('B25') - tab.excel_ref('B28') - tab.excel_ref('B32') - tab.excel_ref('B36') - tab.excel_ref('B39') - tab.excel_ref('B44') - tab.excel_ref('B47') - tab.excel_ref('B50') - tab.excel_ref('B57') - tab.excel_ref('B60') - tab.excel_ref('B63') - tab.excel_ref('B69') - tab.excel_ref('B76') - tab.excel_ref('B79') - tab.excel_ref('B82') - tab.excel_ref('B87') - tab.excel_ref('B92') - tab.excel_ref('B95') - tab.excel_ref('B99') - tab.excel_ref('B106') - tab.excel_ref('B109') - tab.excel_ref('B112') - tab.excel_ref('B120') - tab.excel_ref('B123') - tab.excel_ref('B126') - tab.excel_ref('B129') - tab.excel_ref('B132') - tab.excel_ref('B135') - tab.excel_ref('B138') - tab.excel_ref('B141') - tab.excel_ref('B144') - tab.excel_ref('B147') - tab.excel_ref('B166')- tab.excel_ref('B173') - tab.excel_ref('B76') - tab.excel_ref('B179') - tab.excel_ref('B182') - tab.excel_ref('B185') - tab.excel_ref('B188') - tab.excel_ref('B194').expand(DOWN)
observations = profession_of_post.fill(DOWN).is_not_blank() - tab.excel_ref('B193').expand(RIGHT).expand(DOWN)
dimensions = [
    HDimConst('Measure Type', 'headcount'),
    HDimConst('Year', '2018'),
    HDimConst('Ethnicity', 'all'),
    HDimConst('Disability Status', 'not-applicable'),
    HDimConst('ONS Age Range', 'all'),
    HDimConst('Nationality', 'all'),
    HDimConst('Responsibility Level', 'all'),
    HDimConst('Region name', 'all'),
    HDimConst('Employment Status', 'not-applicable'),
    HDimConst('NUTS Area Code', 'not-applicable'),
    HDimConst('ONS area code', 'not-applicable'),
    HDimConst('Sex', 'all'),
    HDimConst('Salary Band', 'all'),
    HDimConst('Employment Type', 'all-employees'),
    HDimConst('Entrants or Leavers', 'not-applicable'),
    HDim(department, 'Department', DIRECTLY, LEFT),
    HDim(profession_of_post, 'Profession of Post', DIRECTLY, ABOVE), 
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
