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


# Table 12 : Civil Service employment; regional distribution by government department

tabs = {tab.name: tab for tab in scraper.distribution(latest=True).as_databaker()}
tab = tabs['Table 12']

region = tab.excel_ref('C6').expand(RIGHT).is_not_blank() 
department = tab.excel_ref('B10').fill(DOWN).is_not_blank() - tab.excel_ref('B17') - tab.excel_ref('B26') - tab.excel_ref('B29') - tab.excel_ref('B33') - tab.excel_ref('B37') - tab.excel_ref('B40') - tab.excel_ref('B45') - tab.excel_ref('B48') - tab.excel_ref('B51') - tab.excel_ref('B58') - tab.excel_ref('B61') - tab.excel_ref('B64') - tab.excel_ref('B70') - tab.excel_ref('B77') - tab.excel_ref('B80') - tab.excel_ref('B83') - tab.excel_ref('B88') - tab.excel_ref('B93') - tab.excel_ref('B96') - tab.excel_ref('B100') - tab.excel_ref('B107') - tab.excel_ref('B110') - tab.excel_ref('B113') - tab.excel_ref('B121') - tab.excel_ref('B124') - tab.excel_ref('B127') - tab.excel_ref('B130') - tab.excel_ref('B133') - tab.excel_ref('B136') - tab.excel_ref('B139') - tab.excel_ref('B142') - tab.excel_ref('B145') - tab.excel_ref('B148') - tab.excel_ref('B167')- tab.excel_ref('B174') - tab.excel_ref('B77') - tab.excel_ref('B180') - tab.excel_ref('B183') - tab.excel_ref('B186') - tab.excel_ref('B189') - tab.excel_ref('B195').expand(DOWN)
observations = region.fill(DOWN).is_not_blank() - tab.excel_ref('B195').expand(RIGHT).expand(DOWN)
#savepreviewhtml(department)
dimensions = [
    HDimConst('Measure Type', 'headcount'),
    HDimConst('Year', '2018'),
    HDimConst('Sex', 'U'),
    HDimConst('Ethnicity', 'all'),
    HDimConst('Disability Status', 'not-applicable'),
    HDimConst('ONS Age Range', 'all'),
    HDimConst('Nationality', 'all'),
    HDimConst('Responsibility Level', 'all-employees'),
    HDimConst('Type of Employment', 'all-employees'),
    HDimConst('Status of Employment', 'not-applicable'),
    HDimConst('Profession of Post', 'all'),
    HDimConst('Salary Band', 'all'),
    HDimConst('Entrants or Leavers', 'not-applicable'),
    HDimConst('NUTS Area Code', 'not-applicable'),
    HDimConst('ONS area code', 'not-applicable'),
    HDim(department, 'Department', DIRECTLY, LEFT),
    HDim(region, 'Region name', DIRECTLY, ABOVE),
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
new_table['Department'] = new_table['Department'].map(lambda x: pathify(x))
new_table = new_table.fillna('not-applicable')
new_table
