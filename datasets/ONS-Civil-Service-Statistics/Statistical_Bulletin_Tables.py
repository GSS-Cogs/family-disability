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
#######################################################
#Statistical Bulletin Tables 1-11
#Removed observations without area codes (Overseas, not reported and all employees)
#As well as NUTS area code 

tabs = {tab.name: tab for tab in scraper.distribution(latest=True).as_databaker()}
stats_tables = pd.DataFrame()


# +
tab = tabs['Table 1']
responsibility_level = tab.excel_ref('B10').fill(DOWN).is_not_blank() - tab.excel_ref('B22').expand(DOWN)
gender = tab.excel_ref('C7').expand(RIGHT).is_not_blank()
employment_type = tab.excel_ref('B6').expand(RIGHT).is_not_blank()
observations = gender.fill(DOWN).is_not_blank() - tab.excel_ref('B22').expand(RIGHT).expand(DOWN)
#savepreviewhtml(observations)
dimensions = [
        HDimConst('Measure Type', 'Headcount'),
        HDimConst('Period', '2018'),
        HDim(employment_type, 'Type of Employment', CLOSEST, LEFT),
        HDim(responsibility_level, 'Responsibility Level', DIRECTLY, LEFT),
        HDim(gender, 'Sex', DIRECTLY, ABOVE),
 
]
c1 = ConversionSegment(observations, dimensions, processTIMEUNIT=True)
table_1 = c1.topandas()
stats_tables = pd.concat([table_1, stats_tables])

# +
tab = tabs['Table 2']
responsibility_level = tab.excel_ref('B8').fill(DOWN).is_not_blank() - tab.excel_ref('B20').expand(DOWN)
ethnicity = tab.excel_ref('C5').expand(RIGHT).is_not_blank()
observations = ethnicity.fill(DOWN).is_not_blank() - tab.excel_ref('B21').expand(RIGHT).expand(DOWN)
dimensions = [    
    HDimConst('Measure Type', 'Headcount'),
    HDimConst('Period', '2018'),
    HDim(responsibility_level, 'Responsibility Level', DIRECTLY, LEFT),
    HDim(ethnicity, 'Ethnicity', DIRECTLY, ABOVE)  
]

c1 = ConversionSegment(observations, dimensions, processTIMEUNIT=True)
table_2 = c1.topandas()
stats_tables = pd.concat([table_2, stats_tables], sort=True)

# +
tab = tabs['Table 3']
responsibility_level = tab.excel_ref('B8').fill(DOWN).is_not_blank() - tab.excel_ref('B20').expand(DOWN)
disability_status = tab.excel_ref('C5').expand(RIGHT).is_not_blank()
observations = disability_status.fill(DOWN).is_not_blank() - tab.excel_ref('B21').expand(RIGHT).expand(DOWN)
dimensions = [
    HDimConst('Measure Type', 'Headcount'),
    HDimConst('Period', '2018'),
    HDim(responsibility_level, 'Responsibility Level', DIRECTLY, LEFT),
    HDim(disability_status, 'Disability Status', DIRECTLY, ABOVE)
]

c1 = ConversionSegment(observations, dimensions, processTIMEUNIT=True)
#savepreviewhtml(c1)
table_3 = c1.topandas()
stats_tables = pd.concat([table_3, stats_tables], sort=True)

# +
tab = tabs['Table 4']
responsibility_level = tab.excel_ref('B8').fill(DOWN).is_not_blank() - tab.excel_ref('B20').expand(DOWN)
age_group = tab.excel_ref('C5').expand(RIGHT).is_not_blank()
observations = age_group.fill(DOWN).is_not_blank() - tab.excel_ref('B20').expand(RIGHT).expand(DOWN)

dimensions = [
    HDimConst('Measure Type', 'Headcount'),
    HDimConst('Period', '2018'),
    HDim(responsibility_level, 'Responsibility Level', DIRECTLY, LEFT),
    HDim(age_group, 'ONS Age Range', DIRECTLY, ABOVE)   
]
c1 = ConversionSegment(observations, dimensions, processTIMEUNIT=True)
table_4 = c1.topandas()
stats_tables = pd.concat([table_4, stats_tables], sort=True)
# -

tab = tabs['Table 5']
responsibility_level = tab.excel_ref('B8').fill(DOWN).is_not_blank() - tab.excel_ref('B20').expand(DOWN)
nationality = tab.excel_ref('C5').expand(RIGHT).is_not_blank()
observations = nationality.fill(DOWN).is_not_blank() - tab.excel_ref('B20').expand(RIGHT).expand(DOWN)
dimensions = [
    HDimConst('Measure Type', 'Headcount'),
    HDimConst('Period', '2018'),
    HDim(responsibility_level, 'Responsibility Level', DIRECTLY, LEFT),
    HDim(nationality, 'Nationality', DIRECTLY, ABOVE)
]
c1 = ConversionSegment(observations, dimensions, processTIMEUNIT=True)
table_5 = c1.topandas()
stats_tables = pd.concat([table_5, stats_tables], sort=True)

tab = tabs['Table 6']
salary_band = tab.excel_ref('B9').fill(DOWN).is_not_blank() - tab.excel_ref('B9') - tab.excel_ref('B28').expand(DOWN)
gender = tab.excel_ref('C6').expand(RIGHT).is_not_blank()
employment_type = tab.excel_ref('C5').expand(RIGHT).is_not_blank()
observations = gender.fill(DOWN).is_not_blank() - tab.excel_ref('B29').expand(RIGHT).expand(DOWN)
dimensions = [
    HDimConst('Measure Type', 'Headcount'),
    HDimConst('Period', '2018'),
    HDim(employment_type, 'Type of Employment', CLOSEST, LEFT),
    HDim(salary_band, 'Salary Band', DIRECTLY, LEFT),
    HDim(gender, 'Sex', DIRECTLY, ABOVE)   
]
c1 = ConversionSegment(observations, dimensions, processTIMEUNIT=True)
table_6 = c1.topandas()
table_6 = table_6.replace({'Sex' : {'Male' : 'M','Female ' : 'F','Total' : 'T', ' ' : 'U' }})
stats_tables = pd.concat([table_6, stats_tables], sort=True)

tab = tabs['Table 8']
profession_of_post = tab.excel_ref('C5').expand(RIGHT).is_not_blank() 
department = tab.excel_ref('B9').fill(DOWN).is_not_blank() - tab.excel_ref('B16') - tab.excel_ref('B25') - tab.excel_ref('B28') - tab.excel_ref('B32') - tab.excel_ref('B36') - tab.excel_ref('B39') - tab.excel_ref('B44') - tab.excel_ref('B47') - tab.excel_ref('B50') - tab.excel_ref('B57') - tab.excel_ref('B60') - tab.excel_ref('B63') - tab.excel_ref('B69') - tab.excel_ref('B76') - tab.excel_ref('B79') - tab.excel_ref('B82') - tab.excel_ref('B87') - tab.excel_ref('B92') - tab.excel_ref('B95') - tab.excel_ref('B99') - tab.excel_ref('B106') - tab.excel_ref('B109') - tab.excel_ref('B112') - tab.excel_ref('B120') - tab.excel_ref('B123') - tab.excel_ref('B126') - tab.excel_ref('B129') - tab.excel_ref('B132') - tab.excel_ref('B135') - tab.excel_ref('B138') - tab.excel_ref('B141') - tab.excel_ref('B144') - tab.excel_ref('B147') - tab.excel_ref('B166')- tab.excel_ref('B173') - tab.excel_ref('B76') - tab.excel_ref('B179') - tab.excel_ref('B182') - tab.excel_ref('B185') - tab.excel_ref('B188') - tab.excel_ref('B194').expand(DOWN)
observations = profession_of_post.fill(DOWN).is_not_blank() - tab.excel_ref('B193').expand(RIGHT).expand(DOWN)
dimensions = [
    HDimConst('Measure Type', 'Headcount'),
    HDimConst('Period', '2018'),
    HDim(department, 'Department', DIRECTLY, LEFT),
    HDim(profession_of_post, 'Profession of Post', DIRECTLY, ABOVE), 
]
c1 = ConversionSegment(observations, dimensions, processTIMEUNIT=True)
table_8 = c1.topandas()
stats_tables = pd.concat([table_8, stats_tables], sort=True)

tab = tabs['Table 9']
entrants_leavers = tab.excel_ref('B5').expand(RIGHT).is_not_blank()
gender = tab.excel_ref('C6').expand(RIGHT).is_not_blank()
responsibility_level = tab.excel_ref('B9').fill(DOWN).is_not_blank() - tab.excel_ref('B9') - tab.excel_ref('B21').expand(DOWN)
observations = gender.fill(DOWN).is_not_blank() - tab.excel_ref('B21').expand(RIGHT).expand(DOWN)
dimensions = [
    HDimConst('Measure Type', 'Headcount'),
    HDimConst('Period', '2018'),
    HDim(gender, 'Sex', DIRECTLY, ABOVE),
    HDim(responsibility_level, 'Responsibility Level', DIRECTLY, LEFT),
    HDim(entrants_leavers, 'Entrants or Leavers', CLOSEST, LEFT),
]
c1 = ConversionSegment(observations, dimensions, processTIMEUNIT=True)
table_9 = c1.topandas()
stats_tables = pd.concat([table_9, stats_tables], sort=True)

tab = tabs['Table 10']
area_code = tab.excel_ref('A11').expand(DOWN) - tab.excel_ref('A30').expand(DOWN)
region = tab.excel_ref('B11').expand(DOWN).is_not_blank() - tab.excel_ref('B26').expand(DOWN)
employment_status = tab.excel_ref('B7').expand(RIGHT).is_not_blank() #- tab.excel_ref('F7').expand(RIGHT).is_not_blank()
employment_type = tab.excel_ref('C6').expand(RIGHT).is_not_blank()
observations = employment_status.fill(DOWN).is_not_blank() - tab.excel_ref('A26').expand(DOWN).expand(RIGHT)
dimensions = [
    HDimConst('Measure Type', 'All Employees'),#
    HDimConst('Period', '2018'),
    #HDim(area_code, 'ONS area code', DIRECTLY, LEFT), #dropped for now
    HDim(region, 'Region name', DIRECTLY, LEFT), 
    HDim(employment_status, 'Status of Employment', DIRECTLY, ABOVE), 
    HDim(employment_type, 'Type of Employment', CLOSEST, LEFT), 
]
c1 = ConversionSegment(observations, dimensions, processTIMEUNIT=True)
table_10 = c1.topandas()
#savepreviewhtml(c1)
stats_tables = pd.concat([table_10, stats_tables], sort=True)

# +
stats_tables.rename(columns={'OBS': 'Value'}, inplace=True)
if 'DATAMARKER' in stats_tables.columns:
    print('marker found in columns')
    stats_tables['DATAMARKER'].replace('..', 'between-one-and-five', inplace=True)
    stats_tables['DATAMARKER'].replace('-', 'not-applicable', inplace=True)
    stats_tables = stats_tables.rename(columns={'DATAMARKER':'Marker'})
    stats_tables['Marker'] = stats_tables['Marker'].fillna(value='not-applicable')
else:
    print('marker not found in colmns making it')
    stats_tables['DATAMARKER'] = 'not-applicable'
    stats_tables = stats_tables.rename(columns={'DATAMARKER':'Marker'})
    

stats_tables = stats_tables.replace({'Sex' : {'Male' : 'M','Female' : 'F','Total' : 'T', ' ' : 'U' }})
stats_tables['Sex'] = stats_tables['Sex'].fillna(value='U')

stats_tables['Department'] = stats_tables['Department'].fillna(value='all')
stats_tables['Profession of Post'] = stats_tables['Profession of Post'].fillna(value='all').map(lambda x: pathify(x))
stats_tables['Status of Employment'] = stats_tables['Status of Employment'].fillna(value='all').map(lambda x: pathify(x))
stats_tables = stats_tables.replace({'Type of Employment' : {'Full Time' : 'Full Time Employees','Part Time' : 'Part Time Employees','Total' : 'All Employees' }})
stats_tables['Type of Employment'] = stats_tables['Type of Employment'].fillna(value='All employees')#.map(lambda x: pathify(x))
stats_tables = stats_tables.replace({'Type of Employment' : 
                               {'full-time' : 'full-time-employees',
                                'part-time' : 'part-time-employees',
                                'Full-time employees2' : 'Full-time employees',
                               'Part-time employees3' : 'Part-time employees',
                               'All employees3' : 'All employees'}})
#stats_tables['Region name'] = stats_tables['Region name'].map(lambda x: pathify(x))
#stats_tables['NUTS Region name'] = stats_tables['NUTS Region name'].map(lambda x: pathify(x))
stats_tables['Responsibility Level'] = stats_tables['Responsibility Level'].fillna(value='all').map(lambda x: pathify(x))
stats_tables = stats_tables.replace({'Ethnicity' : 
                               {'Not Declared4' : 'Not Declared',
                                'Not Reported5' : 'Not Reported',}})
stats_tables['Ethnicity'] = stats_tables['Ethnicity'].fillna(value='all').map(lambda x: pathify(x))
stats_tables = stats_tables.replace({'Nationality' : 
                               {'Not Declared5' : 'Not Declared',
                                'Not Reported6' : 'Not Reported',}})
stats_tables['Nationality'] = stats_tables['Nationality'].fillna(value='all').map(lambda x: pathify(x))
stats_tables['Region name'] = stats_tables['Region name'].fillna(value='All regions')
stats_tables = stats_tables.replace({'Disability Status' : 
                               {'Not Declared6' : 'Not Declared',
                                'Not Declared4' : 'Not Declared',
                                'Not Reported7' : 'Not Reported',
                                'Not Reported5' : 'Not Reported'
                               }})
stats_tables['Disability Status'] = stats_tables['Disability Status'].fillna(value='unknown').map(lambda x: pathify(x))
stats_tables['ONS Age Range'] = stats_tables['ONS Age Range'].fillna(value='all').map(lambda x: pathify(x))
stats_tables['Salary Band'] = stats_tables['Salary Band'].fillna(value='unknown').map(lambda x: pathify(x))
stats_tables['Entrants or Leavers'] = stats_tables['Entrants or Leavers'].fillna(value='all').map(lambda x: pathify(x))
stats_tables['Period'] = 'year/' + stats_tables['Period']
stats_tables
