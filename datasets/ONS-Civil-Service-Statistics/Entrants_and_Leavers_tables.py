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


#######################################################
#Entrants and Leavers
tabs = {tab.name: tab for tab in scraper.distribution(latest=True).as_databaker()}
entry_leave_tables = pd.DataFrame()


tab = tabs['Table 40']
department = tab.excel_ref('B9').expand(DOWN).is_not_blank() - tab.excel_ref('B193').expand(DOWN)
entrants_or_leavers = tab.excel_ref('B5').expand(RIGHT).is_not_blank()
gender = tab.excel_ref('B6').expand(RIGHT).is_not_blank()
observations = gender.fill(DOWN).is_not_blank() - tab.excel_ref('B193').expand(DOWN).expand(RIGHT) 
dimensions = [
    HDimConst('Period', '2018'),
    HDimConst('Measure Type', 'Headcount'),
    HDim(department, 'Department', DIRECTLY, LEFT), 
    HDim(gender, 'Sex', DIRECTLY, ABOVE), 
    HDim(entrants_or_leavers, 'Entrants or Leavers', CLOSEST, LEFT), 
]
c1 = ConversionSegment(observations, dimensions, processTIMEUNIT=True)
table_40 = c1.topandas()
entry_leave_tables = pd.concat([table_40, entry_leave_tables])

tab = tabs['Table 41']
department = tab.excel_ref('B9').expand(DOWN).is_not_blank() - tab.excel_ref('B194').expand(DOWN)
ethnicity = tab.excel_ref('B5').expand(RIGHT).is_not_blank() - tab.excel_ref('Z5').expand(RIGHT).is_not_blank()
entrants_or_leavers = tab.excel_ref('B6').expand(RIGHT).is_not_blank() - tab.excel_ref('Z6').expand(RIGHT).is_not_blank()
observations = entrants_or_leavers.fill(DOWN).is_not_blank() - tab.excel_ref('B194').expand(DOWN).expand(RIGHT) 
dimensions = [
    HDimConst('Period', '2018'),
    HDimConst('Measure Type', 'Headcount'),
    HDim(department, 'Department', DIRECTLY, LEFT), 
    HDim(ethnicity, 'Ethnicity', CLOSEST, LEFT), 
    HDim(entrants_or_leavers, 'Entrants or Leavers', DIRECTLY, ABOVE), 
]
c1 = ConversionSegment(observations, dimensions, processTIMEUNIT=True)
table_41 = c1.topandas()
entry_leave_tables = pd.concat([table_41, entry_leave_tables], sort=True)

# +
entry_leave_tables.rename(columns={'OBS': 'Value'}, inplace=True)
if 'DATAMARKER' in entry_leave_tables.columns:
    print('marker found in columns')
    entry_leave_tables['DATAMARKER'].replace('..', 'Between one and five', inplace=True)
    entry_leave_tables['DATAMARKER'].replace('-', 'not-applicable', inplace=True)
    entry_leave_tables = entry_leave_tables.rename(columns={'DATAMARKER':'Marker'})
    entry_leave_tables['Marker'] = entry_leave_tables['Marker'].fillna(value='not-applicable')
else:
    print('marker not found in colmns making it')
    entry_leave_tables['DATAMARKER'] = 'not-applicable'
    entry_leave_tables = entry_leave_tables.rename(columns={'DATAMARKER':'Marker'})

entry_leave_tables = entry_leave_tables.replace({'Sex' : {'Male' : 'M','Female' : 'F','Total' : 'T', ' ' : 'U' }})
entry_leave_tables['Sex'] = entry_leave_tables['Sex'].fillna(value='U')
entry_leave_tables['Department'] = entry_leave_tables['Department'].fillna(value='all')
entry_leave_tables['Entrants or Leavers'] = entry_leave_tables['Entrants or Leavers'].fillna(value='all').map(lambda x: pathify(x))
entry_leave_tables = entry_leave_tables.replace({'Ethnicity' : 
                              {'Not Declared5' : 'Not Declared',
                               'Not Reported6' : 'Not Reported',}})
entry_leave_tables['Ethnicity'] = entry_leave_tables['Ethnicity'].fillna(value='all').map(lambda x: pathify(x))
entry_leave_tables['Period'] = 'year/' + entry_leave_tables['Period']
entry_leave_tables
# -



