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
#Government Department Tables 
#Removed observations without area codes (Overseas, not reported and all employees)
tabs = {tab.name: tab for tab in scraper.distribution(latest=True).as_databaker()}
gov_tables = pd.DataFrame()


tab = tabs['Table 36']
department = tab.excel_ref('B9').expand(DOWN).is_not_blank() - tab.excel_ref('B194').expand(DOWN)
gender = tab.excel_ref('B6').expand(RIGHT).is_not_blank()
observations = gender.fill(DOWN).is_not_blank() - tab.excel_ref('B194').expand(DOWN).expand(RIGHT) 
dimensions = [
    HDimConst('Period', '2018'),
    HDimConst('Measure Type', 'Percentage of each Gender by department'),
    HDim(department, 'Department', DIRECTLY, LEFT), 
    HDim(gender, 'Sex', DIRECTLY, ABOVE), 
]
c1 = ConversionSegment(observations, dimensions, processTIMEUNIT=True)
table_36 = c1.topandas()
gov_tables = pd.concat([table_36, gov_tables])

tab = tabs['Table 37']
department = tab.excel_ref('B9').expand(DOWN).is_not_blank() - tab.excel_ref('B193').expand(DOWN)
ethnicity = tab.excel_ref('B5').expand(RIGHT).is_not_blank() - tab.excel_ref('K5').expand(RIGHT)
observations = ethnicity.fill(DOWN).is_not_blank() - tab.excel_ref('B193').expand(DOWN).expand(RIGHT) 
dimensions = [
    HDimConst('Period', '2018'),
    HDimConst('Measure Type', 'headcount'),
    HDim(department, 'Department', DIRECTLY, LEFT), 
    HDim(ethnicity, 'Ethnicity', DIRECTLY, ABOVE), 
]
c1 = ConversionSegment(observations, dimensions, processTIMEUNIT=True)
table_37 = c1.topandas()
gov_tables = pd.concat([table_37, gov_tables], sort=True)

tab = tabs['Table 38']
department = tab.excel_ref('B9').expand(DOWN).is_not_blank() - tab.excel_ref('B193').expand(DOWN)
disability_status = tab.excel_ref('B5').expand(RIGHT).is_not_blank() - tab.excel_ref('K5').expand(RIGHT)
observations = disability_status.fill(DOWN).is_not_blank() - tab.excel_ref('B193').expand(DOWN).expand(RIGHT) 
dimensions = [
    HDimConst('Period', '2018'),
    HDimConst('Measure Type', 'headcount'),
    HDim(department, 'Department', DIRECTLY, LEFT), 
    HDim(disability_status, 'Disability Status', DIRECTLY, ABOVE), 
]
c1 = ConversionSegment(observations, dimensions, processTIMEUNIT=True)
table_38 = c1.topandas()
gov_tables = pd.concat([table_38, gov_tables], sort=True)

tab = tabs['Table 39']
department = tab.excel_ref('B9').expand(DOWN).is_not_blank() - tab.excel_ref('B193').expand(DOWN)
age_group = tab.excel_ref('B5').expand(RIGHT).is_not_blank()
observations = age_group.fill(DOWN).is_not_blank() - tab.excel_ref('B193').expand(DOWN).expand(RIGHT) 
dimensions = [
    HDimConst('Period', '2018'),
    HDimConst('Measure Type', 'headcount'),
    HDim(department, 'Department', DIRECTLY, LEFT), 
    HDim(age_group, 'ONS Age Range', DIRECTLY, ABOVE), 
]
c1 = ConversionSegment(observations, dimensions, processTIMEUNIT=True)
table_39 = c1.topandas() 
gov_tables = pd.concat([table_39, gov_tables], sort=True)




gov_tables.rename(columns={'OBS': 'Value'}, inplace=True)
if 'DATAMARKER' in gov_tables.columns:
    print('marker found in columns')
    gov_tables['DATAMARKER'].replace('..', 'between-one-and-five', inplace=True)
    gov_tables['DATAMARKER'].replace('-', 'not-applicable', inplace=True)
    gov_tables = gov_tables.rename(columns={'DATAMARKER':'Marker'})
    gov_tables['Marker'] = gov_tables['Marker'].fillna(value='not-applicable')
else:
    print('marker not found in colmns making it')
    gov_tables['DATAMARKER'] = 'not-applicable'
    gov_tables = gov_tables.rename(columns={'DATAMARKER':'Marker'})
gov_tables = gov_tables.replace({'Sex' : {'Male' : 'M','Female' : 'F','Total' : 'T', ' ' : 'U' }})
gov_tables['Sex'] = gov_tables['Sex'].fillna(value='U')
gov_tables['Department'] = gov_tables['Department'].fillna(value='all').map(lambda x: pathify(x))
gov_tables = gov_tables.replace({'Type of Employment' : 
                               {'  Full-time4' : 'full-time-employees',
                                '  Part-time5' : 'part-time-employees',
                                '  All5' : 'all-employees',}})
gov_tables = gov_tables.replace({'Ethnicity' : 
                              {'Not Declared3' : 'Not Declared',
                               'Not Reported4' : 'Not Reported',}})
gov_tables['Ethnicity'] = gov_tables['Ethnicity'].fillna(value='all').map(lambda x: pathify(x))
gov_tables = gov_tables.replace({'Disability Status' : 
                               {'Not Declared3' : 'Not Declared',
                                'Not Reported4' : 'Not Reported',}})
gov_tables['Disability Status'] = gov_tables['Disability Status'].fillna(value='unknown').map(lambda x: pathify(x))
gov_tables['ONS Age Range'] = gov_tables['ONS Age Range'].fillna(value='all').map(lambda x: pathify(x))
gov_tables['Measure Type'] = gov_tables['Measure Type'].map(lambda x: pathify(x))
gov_tables['Period'] = 'year/' + gov_tables['Period']
gov_tables



