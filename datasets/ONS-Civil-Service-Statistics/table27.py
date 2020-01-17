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


# table 27:  Civil Service employment; Median earnings by ethnicity and responsibility level1 2

tabs = {tab.name: tab for tab in scraper.distribution(latest=True).as_databaker()}
tab = tabs['Table 27']

responsibility_level = tab.excel_ref('B8').expand(DOWN).is_not_blank() - tab.excel_ref('B20').expand(DOWN)
ethnicity = tab.excel_ref('C5').expand(RIGHT).is_not_blank()
observations = ethnicity.fill(DOWN).is_not_blank() - tab.excel_ref('B20').expand(DOWN).expand(RIGHT)
#savepreviewhtml(observations)

dimensions = [
    HDimConst('Measure Type', 'median-earnings'),
    HDimConst('Year', '2018'),
    HDimConst('ONS Age Range', 'all'),
    HDimConst('Region name', 'all'),
    HDimConst('Nationality', 'all'),
    HDimConst('Salary Band', 'all'),
    HDimConst('Sex', 'U'),
    HDimConst('Profession of Post', 'all'),
    HDimConst('Entrants or Leavers', 'not-applicable'),
    HDimConst('Type of Employment', 'full-time-employees'),
    HDimConst('Status of Employment', 'not-applicable'),
    HDimConst('NUTS Area Code', 'not-applicable'),
    HDimConst('ONS area code', 'not-applicable'),
    HDimConst('Department', 'all'),
    HDimConst('Disability Status', 'not-applicable'), 
    HDim(ethnicity, 'Ethnicity', DIRECTLY, ABOVE),
    HDim(responsibility_level, 'Responsibility Level', DIRECTLY, LEFT), 
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
new_table = new_table.replace({'Ethnicity' : 
                               {'Not Declared5' : 'Not Declared',
                                'Not Reported6' : 'Not Reported',}})

new_table['Responsibility Level'] = new_table['Responsibility Level'].map(lambda x: pathify(x))
new_table['Ethnicity'] = new_table['Ethnicity'].map(lambda x: pathify(x))
new_table
