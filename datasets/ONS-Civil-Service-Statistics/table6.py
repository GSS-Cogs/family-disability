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
tab = tabs['Table 6']

salary_band = tab.excel_ref('B9').fill(DOWN).is_not_blank() - tab.excel_ref('B9') - tab.excel_ref('B28').expand(DOWN)
gender = tab.excel_ref('C6').expand(RIGHT).one_of(gender_type)
employment_type = tab.excel_ref('C5').expand(RIGHT).is_not_blank()
observations = gender.fill(DOWN).is_not_blank() - tab.excel_ref('B29').expand(RIGHT).expand(DOWN)
dimensions = [
    HDimConst('Measure Type', 'Count'),
    HDimConst('Period', '31/03/2018'),
    HDimConst('Ethnicity', 'All'),
    HDimConst('Disability Status', 'not-applicable'),
    HDimConst('Age Group', 'All'),
    HDimConst('Nationality', 'All'),
    HDimConst('Responsibility Level', 'All'),
    HDimConst('Department', 'All'),
    HDimConst('Profession of Post', 'All'),
    HDimConst('Entrants or Leavers', 'not-applicable'),
    HDim(employment_type, 'Employment Type', CLOSEST, LEFT),
    HDim(salary_band, 'Salary Band', DIRECTLY, LEFT),
    HDim(gender, 'Sex', DIRECTLY, ABOVE)
]
c1 = ConversionSegment(observations, dimensions, processTIMEUNIT=True)
new_table = c1.topandas()

new_table.rename(columns={'OBS': 'Value'}, inplace=True)

# +
new_table = new_table [['Value', 'DATAMARKER', 'Period','Disability Status', 'Ethnicity', 'Measure Type','Age Group','Nationality','Responsibility Level', 'Department', 'Profession of Post', 'Entrants or Leavers', 'Employment Type', 'Salary Band', 'Sex']]
new_table


# -







