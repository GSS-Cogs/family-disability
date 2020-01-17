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


# table 38:   Civil Service employment by government department and disability status1 2

tabs = {tab.name: tab for tab in scraper.distribution(latest=True).as_databaker()}
tab = tabs['Table 38']

department = tab.excel_ref('B9').expand(DOWN).is_not_blank() - tab.excel_ref('B193').expand(DOWN)
disability_status = tab.excel_ref('B5').expand(RIGHT).is_not_blank() - tab.excel_ref('K5').expand(RIGHT)
observations = disability_status.fill(DOWN).is_not_blank() - tab.excel_ref('B193').expand(DOWN).expand(RIGHT) 
#savepreviewhtml(observations)


dimensions = [
    HDimConst('Year', '2018'),
    HDimConst('Measure Type', 'headcount'),
    HDimConst('ONS Age Range', 'all'),
    HDimConst('Region name', 'all'),
    HDimConst('Nationality', 'all'),
    HDimConst('Salary Band', 'all'),
    HDimConst('Sex', 'U'),
    HDimConst('Ethnicity', 'all'),
    HDimConst('Profession of Post', 'all'),
    HDimConst('Entrants or Leavers', 'not-applicable'),
    HDimConst('Status of Employment', 'not-applicable'),
    HDimConst('Type of Employment', 'all-employees'),
    HDimConst('NUTS Area Code', 'not-applicable'),
    HDimConst('ONS area code', 'not-applicable'),
    HDimConst('Responsibility Level', 'all-employees'),
    HDim(department, 'Department', DIRECTLY, LEFT), 
    HDim(disability_status, 'Disability Status', DIRECTLY, ABOVE), 
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
new_table = new_table.replace({'Disability Status' : 
                               {'Not Declared3' : 'Not Declared',
                                'Not Reported4' : 'Not Reported',}})

new_table['Disability Status'] = new_table['Disability Status'].map(lambda x: pathify(x))
new_table['Department'] = new_table['Department'].map(lambda x: pathify(x))
new_table


