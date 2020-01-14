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


# Responsibility Level
# Table 23 :Civil Service employment by responsibility level, age and sex 
# - All Employees 
# - Headcount 

tabs = {tab.name: tab for tab in scraper.distribution(latest=True).as_databaker()}
tab = tabs['Table 23']

responsibility_level = tab.excel_ref('B9').expand(DOWN).is_not_blank() - tab.excel_ref('B21').expand(DOWN)
gender = tab.excel_ref('C6').expand(RIGHT)#.is_not_blank() - tab.excel_ref('W5').expand(RIGHT)
age_group = tab.excel_ref('C5').expand(RIGHT).is_not_blank() #- tab.excel_ref('W5').expand(RIGHT)
observations = gender.fill(DOWN).is_not_blank() - tab.excel_ref('B21').expand(DOWN).expand(RIGHT)
#savepreviewhtml(observations)

dimensions = [
    HDimConst('Measure Type', 'headount'),
    HDimConst('Year', '2018'),
    HDimConst('Ethnicity', 'all'),
    HDimConst('Nationality', 'all'),
    HDimConst('Salary Band', 'all'),
    HDimConst('Profession of Post', 'not-applicable'),
    HDimConst('Entrants or Leavers', 'not-applicable'),
    HDimConst('Employment Type', 'full-time-employees'),
    HDimConst('Department', 'all'),
    HDimConst('Employment Status', 'not-applicable'),
    HDimConst('NUTS Area Code', 'not-applicable'),
    HDimConst('ONS area code', 'not-applicable'),
    HDimConst('Region name', 'not-applicable'), 
    HDimConst('Disability Status', 'not-applicable'),
    HDim(gender, 'Sex', DIRECTLY, ABOVE), 
    HDim(responsibility_level, 'Responsibility Level', DIRECTLY, LEFT), 
    HDim(age_group, 'ONS Age Range', CLOSEST, LEFT), 
]
c1 = ConversionSegment(observations, dimensions, processTIMEUNIT=True)
new_table = c1.topandas()
#savepreviewhtml(c1)


# Tidy up 

age_not_reported = new_table['ONS Age Range'] == 'Not reported'
age_total = new_table['ONS Age Range'] == 'Total'
new_table.loc[age_not_reported, 'Sex'] = 'Not reported'
new_table.loc[age_total, 'Sex'] = 'Total'
new_table.rename(columns={'OBS': 'Value'}, inplace=True)
new_table['DATAMARKER'].replace('..', 'between-one-and-five', inplace=True)
new_table = new_table.rename(columns={'DATAMARKER':'Marker'})
new_table = new_table.fillna('not-applicable')
new_table



