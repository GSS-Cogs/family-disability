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
tab = tabs['Table 8'] #Civil Service employment; profession by government department

department = tab.excel_ref('C5').expand(RIGHT).is_not_blank() 
profession_of_post = tab.excel_ref('B9').fill(DOWN).is_not_blank() - tab.excel_ref('B16') - tab.excel_ref('B25') - tab.excel_ref('B28') - tab.excel_ref('B32') - tab.excel_ref('B36') - tab.excel_ref('B39') - tab.excel_ref('B44') - tab.excel_ref('B47') - tab.excel_ref('B50') - tab.excel_ref('B57') - tab.excel_ref('B60') - tab.excel_ref('B63') - tab.excel_ref('B69') - tab.excel_ref('B76') - tab.excel_ref('B79') - tab.excel_ref('B82') - tab.excel_ref('B87') - tab.excel_ref('B92') - tab.excel_ref('B95') - tab.excel_ref('B99') - tab.excel_ref('B106') - tab.excel_ref('B109') - tab.excel_ref('B112') - tab.excel_ref('B120') - tab.excel_ref('B123') - tab.excel_ref('B126') - tab.excel_ref('B129') - tab.excel_ref('B132') - tab.excel_ref('B135') - tab.excel_ref('B138') - tab.excel_ref('B141') - tab.excel_ref('B144') - tab.excel_ref('B147') - tab.excel_ref('B166')- tab.excel_ref('B173') - tab.excel_ref('B76') - tab.excel_ref('B179') - tab.excel_ref('B182') - tab.excel_ref('B185') - tab.excel_ref('B188') - tab.excel_ref('B194').expand(DOWN)
observations = department.fill(DOWN).is_not_blank() - tab.excel_ref('B193').expand(RIGHT).expand(DOWN)
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
    HDimConst('Sex', 'All'),
    HDimConst('Salary Band', 'All'),
    HDimConst('Entrants or Leavers', 'not-applicable'),
    HDim(department, 'Department', DIRECTLY, ABOVE),
    HDim(profession_of_post, 'Profession of Post', DIRECTLY, LEFT),
]
c1 = ConversionSegment(observations, dimensions, processTIMEUNIT=True)
new_table = c1.topandas()
new_table
