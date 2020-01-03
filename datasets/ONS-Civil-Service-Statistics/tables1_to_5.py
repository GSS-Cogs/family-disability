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


# +
dist = scraper.distribution(latest=True)
tabs = (t for t in dist.as_databaker())
tabs_required = list(tabs)[0:6]

#tabs = {tab.name: tab for tab in scraper.distribution(latest=True).as_databaker()}
#tab = tabs['Table 1']
tidied_sheets = []
gender_type = ['Male', 'Female', 'Total']

# +
#Tables 1 - 5 
for tab in tabs_required:
    
    if 'Table 1' in tab.name:
        responsibility_level = tab.excel_ref('B8').fill(DOWN).is_not_blank() - tab.excel_ref('B9') - tab.excel_ref('B22').expand(DOWN)
        gender = tab.excel_ref('C7').expand(RIGHT).one_of(gender_type)
        employment_type = tab.excel_ref('B6').expand(RIGHT).is_not_blank()
        observations = gender.fill(DOWN).is_not_blank() - tab.excel_ref('B22').expand(RIGHT).expand(DOWN)
        dimensions = [
            HDimConst('Measure Type', 'Count'),
            HDimConst('Period', '31/03/2018'),
            HDimConst('Ethnicity', 'All'),
            HDimConst('Disability Status', 'not-applicable'),
            HDimConst('Age Group', 'All'),
            HDimConst('Nationality', 'All'),
            HDimConst('Salary Band', 'All'),
            HDim(employment_type, 'Employment Type', CLOSEST, LEFT),
            HDim(responsibility_level, 'Responsibility Level', DIRECTLY, LEFT),
            HDim(gender, 'Sex', DIRECTLY, ABOVE)
        ]
        c1 = ConversionSegment(observations, dimensions, processTIMEUNIT=True)
        new_table_1 = c1.topandas()
        tidied_sheets.append(new_table_1)
        
    if 'Table 2' in tab.name:
        responsibility_level = tab.excel_ref('B8').fill(DOWN).is_not_blank() - tab.excel_ref('B20').expand(DOWN)
        ethnicity = tab.excel_ref('C5').expand(RIGHT).is_not_blank()
        observations = ethnicity.fill(DOWN).is_not_blank() - tab.excel_ref('B21').expand(RIGHT).expand(DOWN)
        dimensions = [
            HDimConst('Measure Type', 'Count'),
            HDimConst('Period', '31/03/2018'),
            HDimConst('Employment Type', 'All'),
            HDimConst('Sex', 'All'),
            HDimConst('Disability Status', 'not-applicable'),
            HDimConst('Age Group', 'All'),
            HDimConst('Nationality', 'All'),
            HDimConst('Salary Band', 'All'),
            HDim(responsibility_level, 'Responsibility Level', DIRECTLY, LEFT),
            HDim(ethnicity, 'Ethnicity', DIRECTLY, ABOVE)
        ]
        c1 = ConversionSegment(observations, dimensions, processTIMEUNIT=True)
        new_table_2 = c1.topandas()
        tidied_sheets.append(new_table_2)
        
    if 'Table 3' in tab.name:
        responsibility_level = tab.excel_ref('B8').fill(DOWN).is_not_blank() - tab.excel_ref('B20').expand(DOWN)
        disability_status = tab.excel_ref('C5').expand(RIGHT).is_not_blank()
        observations = disability_status.fill(DOWN).is_not_blank() - tab.excel_ref('B21').expand(RIGHT).expand(DOWN)
        dimensions = [
            HDimConst('Measure Type', 'Count'),
            HDimConst('Period', '31/03/2018'),
            HDimConst('Employment Type', 'All'),
            HDimConst('Sex', 'All'),
            HDimConst('Ethnicity', 'All'),
            HDimConst('Age Group', 'All'),
            HDimConst('Nationality', 'All'),
            HDimConst('Salary Band', 'All'),
            HDim(responsibility_level, 'Responsibility Level', DIRECTLY, LEFT),
            HDim(disability_status, 'Disability Status', DIRECTLY, ABOVE)
        ]
        c1 = ConversionSegment(observations, dimensions, processTIMEUNIT=True)
        new_table_3 = c1.topandas()
        tidied_sheets.append(new_table_3)
        
    if 'Table 4' in tab.name:
        responsibility_level = tab.excel_ref('B8').fill(DOWN).is_not_blank() - tab.excel_ref('B20').expand(DOWN)
        age_group = tab.excel_ref('C5').expand(RIGHT).is_not_blank()
        observations = age_group.fill(DOWN).is_not_blank() - tab.excel_ref('B20').expand(RIGHT).expand(DOWN)
        #savepreviewhtml(responsibility_level)
        dimensions = [
            HDimConst('Measure Type', 'Count'),
            HDimConst('Period', '31/03/2018'),
            HDimConst('Employment Type', 'All'),
            HDimConst('Sex', 'All'),
            HDimConst('Ethnicity', 'All'),
            HDimConst('Nationality', 'All'),
            HDimConst('Salary Band', 'All'),
            HDimConst('Disability Status', 'not-applicable'),
            HDim(responsibility_level, 'Responsibility Level', DIRECTLY, LEFT),
            HDim(age_group, 'Age Group', DIRECTLY, ABOVE)
        ]
        c1 = ConversionSegment(observations, dimensions, processTIMEUNIT=True)
        new_table_4 = c1.topandas()
        tidied_sheets.append(new_table_4)
        
    if 'Table 5' in tab.name:
        responsibility_level = tab.excel_ref('B8').fill(DOWN).is_not_blank() - tab.excel_ref('B20').expand(DOWN)
        nationality = tab.excel_ref('C5').expand(RIGHT).is_not_blank()
        observations = nationality.fill(DOWN).is_not_blank() - tab.excel_ref('B20').expand(RIGHT).expand(DOWN)
        #savepreviewhtml(responsibility_level)
        dimensions = [
            HDimConst('Measure Type', 'Count'),
            HDimConst('Period', '31/03/2018'),
            HDimConst('Employment Type', 'All'),
            HDimConst('Sex', 'All'),
            HDimConst('Ethnicity', 'All'),
            HDimConst('Disability Status', 'not-applicable'),
            HDimConst('Age Group', 'All'),
            HDimConst('Salary Band', 'All'),
            HDim(responsibility_level, 'Responsibility Level', DIRECTLY, LEFT),
            HDim(nationality, 'Nationality', DIRECTLY, ABOVE)
        ]
        c1 = ConversionSegment(observations, dimensions, processTIMEUNIT=True)
        new_table_5 = c1.topandas()
        tidied_sheets.append(new_table_5)
        
new_table_5
# -






