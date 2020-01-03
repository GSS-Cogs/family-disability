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
tab = tabs['Table 9'] #Entrants and leavers to the Civil Service by sex and responsibility level 

entrants_leavers = tab.excel_ref('B5').expand(RIGHT).is_not_blank()
gender = tab.excel_ref('C6').expand(RIGHT).one_of(gender_type)
responsibility_level = tab.excel_ref('B9').fill(DOWN).is_not_blank() - tab.excel_ref('B9') - tab.excel_ref('B21').expand(DOWN)
observations = gender.fill(DOWN).is_not_blank() - tab.excel_ref('B21').expand(RIGHT).expand(DOWN)
#savepreviewhtml(profession_of_post)
dimensions = [
    HDimConst('Measure Type', 'Count'),
    HDimConst('Period', '31/03/2018'),
    HDimConst('Ethnicity', 'All'),
    HDimConst('Disability Status', 'not-applicable'),
    HDimConst('Age Group', 'All'),
    HDimConst('Nationality', 'All'),
    HDimConst('Responsibility Level', 'All'),
    HDimConst('Employment Type', 'All'),
    HDimConst('Salary Band', 'All'),
    HDimConst('Department', 'All'),
    HDimConst('Profession of Post', 'All'),
    HDim(gender, 'Sex', DIRECTLY, ABOVE),
    HDim(entrants_leavers, 'Entrants or Leavers', CLOSEST, LEFT),
]
c1 = ConversionSegment(observations, dimensions, processTIMEUNIT=True)
new_table = c1.topandas()
new_table
