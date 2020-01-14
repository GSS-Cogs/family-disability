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


# Table 10 :Regional distribution of Civil Service employment

tabs = {tab.name: tab for tab in scraper.distribution(latest=True).as_databaker()}
tab = tabs['Table 10']

area_code = tab.excel_ref('A11').expand(DOWN) - tab.excel_ref('A30').expand(DOWN)
region = tab.excel_ref('B11').expand(DOWN).is_not_blank() - tab.excel_ref('B30').expand(DOWN)
employment_status = tab.excel_ref('B7').expand(RIGHT).is_not_blank() #- tab.excel_ref('F7').expand(RIGHT).is_not_blank()
employment_type = tab.excel_ref('C6').expand(RIGHT).is_not_blank()
observations = employment_status.fill(DOWN).is_not_blank() - tab.excel_ref('A30').expand(DOWN).expand(RIGHT)

# +

dimensions = [
    HDimConst('Measure Type', 'headcount'),
    HDimConst('Year', '2018'),
    HDimConst('Sex', 'all'),
    HDimConst('ONS Age Range', 'all'),
    HDimConst('Ethnicity', 'all'),
    HDimConst('Nationality', 'all'),
    HDimConst('Salary Band', 'all'),
    HDimConst('Profession of Post', 'not-applicable'),
    HDimConst('Entrants or Leavers', 'not-applicable'),
    HDimConst('NUTS Area Code', 'not-applicable'),
    HDimConst('Disability Status', 'not-applicable'),
    HDimConst('Responsibility Level', 'all'),
    HDimConst('Department', 'all'),
    HDim(area_code, 'ONS area code', DIRECTLY, LEFT),
    HDim(region, 'Region name', DIRECTLY, LEFT), 
    HDim(employment_status, 'Status of Employment', DIRECTLY, ABOVE), 
    HDim(employment_type, 'Type of Employment', CLOSEST, LEFT), 
]
c1 = ConversionSegment(observations, dimensions, processTIMEUNIT=True)
new_table = c1.topandas()
# -

new_table.loc[new_table["Type of Employment"]=="Headcount", "Type of Employment"] = 'all-employees'
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
