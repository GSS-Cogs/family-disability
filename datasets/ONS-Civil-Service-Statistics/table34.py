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


# Table 34:  Median Civil Service Gender Pay Gap (2007 - 2017) (All employees)

tabs = {tab.name: tab for tab in scraper.distribution(latest=True).as_databaker()}
tab = tabs['Table 34']

cells_to_remove = ['A11', 'A16', 'A21', 'A26', 'A31', 'A36']
employee_type = tab.excel_ref('A10').expand(DOWN).is_not_blank() - tab.excel_ref('A40').expand(DOWN)
for cell in cells_to_remove:
    employee_type = employee_type - tab.excel_ref(cell)
responsibility_level = tab.excel_ref('A10').expand(DOWN).is_not_blank() - tab.excel_ref('A40').expand(DOWN) - employee_type
year = tab.excel_ref('B6').expand(RIGHT).is_not_blank()
observations = year.fill(DOWN).is_not_blank() - tab.excel_ref('A40').expand(DOWN).expand(RIGHT) 
#savepreviewhtml(observations)


# +
dimensions = [
    HDimConst('Measure Type', 'Median Gender Pay Gap in %'),
    HDimConst('Sex', 'all'),
    HDimConst('ONS Age Range', 'all'),
    HDimConst('Region name', 'all'),
    HDimConst('Nationality', 'all'),
    HDimConst('Salary Band', 'all'),
    HDimConst('Ethnicity', 'all'),
    HDimConst('Disability Status', 'not-applicable'),
    HDimConst('Profession of Post', 'not-applicable'),
    HDimConst('Entrants or Leavers', 'not-applicable'),
    HDimConst('Status of Employment', 'not-applicable'),
    HDimConst('NUTS Area Code', 'not-applicable'),
    HDimConst('ONS area code', 'not-applicable'),
    HDimConst('Department', 'all'),
    HDim(year, 'Year', DIRECTLY, ABOVE),
    HDim(responsibility_level, 'Responsibility Level', CLOSEST, ABOVE), 
    HDim(employee_type, 'Type of Employment', DIRECTLY, LEFT), 

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
#new_table['Type of Employment'] = new_table['Type of Employment'].map(lambda x: pathify(x))
new_table = new_table.replace({'Type of Employment' : {'  Full-time4' : 'full-time-employees',
                                                       '  Part-time5' : 'part-time-employees',
                                                       '  All5' : 'all-employees' }})
new_table


