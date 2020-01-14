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
#1  Civil Service employment by responsibility level and sex
tab = tabs['Table 1']

# +
responsibility_level = tab.excel_ref('B10').fill(DOWN).is_not_blank() - tab.excel_ref('B22').expand(DOWN)
gender = tab.excel_ref('C7').expand(RIGHT).one_of(gender_type)
employment_type = tab.excel_ref('B6').expand(RIGHT).is_not_blank()
observations = gender.fill(DOWN).is_not_blank() - tab.excel_ref('B22').expand(RIGHT).expand(DOWN)
#savepreviewhtml(observations)
dimensions = [
        HDimConst('Measure Type', 'headcount'),
        HDimConst('Year', '2018'),
        HDimConst('Ethnicity', 'all'),
        HDimConst('Disability Status', 'not-applicable'),
        HDimConst('ONS Age Range', 'all'),
        HDimConst('Region name', 'all'),
        HDimConst('Nationality', 'all'),
        HDimConst('Salary Band', 'all'),
        HDimConst('Department', 'all'),
        HDimConst('Profession of Post', 'all'),
        HDimConst('Status of Employment', 'not-applicable'),
        HDimConst('NUTS Area Code', 'not-applicable'),
        HDimConst('ONS area code', 'not-applicable'),
        HDimConst('Entrants or Leavers', 'not-applicable'),
        HDim(employment_type, 'Type of Employment', CLOSEST, LEFT),
        HDim(responsibility_level, 'Responsibility Level', DIRECTLY, LEFT),
        HDim(gender, 'Sex', DIRECTLY, ABOVE),
 
]
c1 = ConversionSegment(observations, dimensions, processTIMEUNIT=True)
#savepreviewhtml(c1)
new_table = c1.topandas()

# +
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
new_table['Department'] = new_table['Department'].map(lambda x: pathify(x))
new_table['Sex'] = new_table['Sex'].map(lambda x: pathify(x))
new_table = new_table.replace({'Sex' : {'male' : 'M','female' : 'F','total' : 'T' }})
new_table['Disability Status'] = new_table['Disability Status'].map(lambda x: pathify(x))
new_table['Type of Employment'] = new_table['Type of Employment'].map(lambda x: pathify(x))
new_table['Status of Employment'] = new_table['Status of Employment'].map(lambda x: pathify(x))
new_table['Profession of Post'] = new_table['Profession of Post'].map(lambda x: pathify(x))
new_table['Nationality'] = new_table['Nationality'].map(lambda x: pathify(x))
new_table['Ethnicity'] = new_table['Ethnicity'].map(lambda x: pathify(x))
new_table['Entrants or Leavers'] = new_table['Entrants or Leavers'].map(lambda x: pathify(x))
new_table['Region name'] = new_table['Region name'].map(lambda x: pathify(x))
new_table['Measure Type'] = new_table['Measure Type'].map(lambda x: pathify(x))
new_table = new_table.fillna('not-applicable')
new_table
# -


