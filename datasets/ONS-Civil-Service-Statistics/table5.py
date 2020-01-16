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


tabs = {tab.name: tab for tab in scraper.distribution(latest=True).as_databaker()}
#5  Civil Service employment by national identity and responsibility level 1 2
tab = tabs['Table 5']

# +
responsibility_level = tab.excel_ref('B8').fill(DOWN).is_not_blank() - tab.excel_ref('B20').expand(DOWN)
nationality = tab.excel_ref('C5').expand(RIGHT).is_not_blank()
observations = nationality.fill(DOWN).is_not_blank() - tab.excel_ref('B20').expand(RIGHT).expand(DOWN)

dimensions = [
    HDimConst('Measure Type', 'headcount'),
    HDimConst('Year', '2018'),
    HDimConst('Type of Employment', 'all-employees'),
    HDimConst('Sex', 'U'),
    HDimConst('Ethnicity', 'all'),
    HDimConst('Salary Band', 'all'),
    HDimConst('Department', 'all'),
    HDimConst('Region name', 'all'),
    HDimConst('Profession of Post', 'all'),
    HDimConst('ONS Age Range', 'all'),
    HDimConst('Disability Status', 'not-applicable'),
    HDimConst('Entrants or Leavers', 'not-applicable'),
    HDimConst('Status of Employment', 'not-applicable'),
    HDimConst('NUTS Area Code', 'not-applicable'),
    HDimConst('ONS area code', 'not-applicable'),
    HDim(responsibility_level, 'Responsibility Level', DIRECTLY, LEFT),
    HDim(nationality, 'Nationality', DIRECTLY, ABOVE)
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


new_table['Responsibility Level'] = new_table['Responsibility Level'].map(lambda x: pathify(x))
new_table['Nationality'] = new_table['Nationality'].map(lambda x: pathify(x))
new_table = new_table.fillna('not-applicable')
new_table