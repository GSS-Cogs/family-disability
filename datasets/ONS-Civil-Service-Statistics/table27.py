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
    HDimConst('Sex', 'all'),
    HDimConst('Profession of Post', 'not-applicable'),
    HDimConst('Entrants or Leavers', 'not-applicable'),
    HDimConst('Employment Type', 'full-time'),
    HDimConst('Employment Status', 'not-applicable'),
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
new_table['DATAMARKER'] = 'not-applicable'
new_table['DATAMARKER'].replace('..', 'between-one-and-five', inplace=True)
new_table = new_table.rename(columns={'DATAMARKER':'Marker'})
new_table = new_table.fillna('not-applicable')
new_table
