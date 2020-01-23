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
#SResponsibility Level Tables 
#Removed observations without area codes (Overseas, not reported and all employees)
#As well as NUTS area code /ONS area code 

tabs = {tab.name: tab for tab in scraper.distribution(latest=True).as_databaker()}
res_tables = pd.DataFrame()
# -


tab = tabs['Table 20']
department = tab.excel_ref('B8').expand(DOWN).is_not_blank() - tab.excel_ref('B194').expand(DOWN)
responsibility_level = tab.excel_ref('B5').expand(RIGHT).is_not_blank()
observations = responsibility_level.fill(DOWN).is_not_blank() - tab.excel_ref('B194').expand(DOWN).expand(RIGHT)
dimensions = [
    HDimConst('Measure Type', 'Headcount'),
    HDimConst('Period', '2018'),
    HDim(department, 'Department', DIRECTLY, LEFT), 
    HDim(responsibility_level, 'Responsibility Level', DIRECTLY, ABOVE), 
]
c1 = ConversionSegment(observations, dimensions, processTIMEUNIT=True)
table_20 = c1.topandas()
res_tables = pd.concat([table_20, res_tables])

tab = tabs['Table 21']
department = tab.excel_ref('B9').fill(DOWN).is_not_blank() - tab.excel_ref('B193').expand(DOWN)
responsibility_level = tab.excel_ref('C5').expand(RIGHT).is_not_blank()
observations = responsibility_level.fill(DOWN).is_not_blank() - tab.excel_ref('B194').expand(DOWN).expand(RIGHT)
dimensions = [
    HDimConst('Measure Type', 'Headcount'),
    HDimConst('Period', '2018'),
    HDimConst('Type of Employment', 'full-time-equivalent'),
    HDim(department, 'Department', DIRECTLY, LEFT), 
    HDim(responsibility_level, 'Responsibility Level', DIRECTLY, ABOVE), 
]
c1 = ConversionSegment(observations, dimensions, processTIMEUNIT=True)
table_21 = c1.topandas()
res_tables = pd.concat([table_21, res_tables], sort=True)

tab = tabs['Table 22']
responsibility_level = tab.excel_ref('C5').expand(RIGHT).is_not_blank()
gender = tab.excel_ref('C6').expand(RIGHT).is_not_blank()
department = tab.excel_ref('B9').fill(DOWN).is_not_blank() - tab.excel_ref('B194').expand(DOWN)
observations = gender.fill(DOWN).is_not_blank() - tab.excel_ref('B194').expand(DOWN).expand(RIGHT)
dimensions = [
    HDimConst('Measure Type', 'Headcount'),
    HDimConst('Period', '2018'),
    HDim(department, 'Department', DIRECTLY, LEFT), 
    HDim(gender, 'Sex', DIRECTLY, ABOVE), 
    HDim(responsibility_level, 'Responsibility Level', CLOSEST, LEFT), 
]
c1 = ConversionSegment(observations, dimensions, processTIMEUNIT=True)
table_22 = c1.topandas()
res_tables = pd.concat([table_22, res_tables], sort=True)

tab = tabs['Table 23']
responsibility_level = tab.excel_ref('B9').expand(DOWN).is_not_blank() - tab.excel_ref('B21').expand(DOWN)
gender = tab.excel_ref('C6').expand(RIGHT)#.is_not_blank() - tab.excel_ref('W5').expand(RIGHT)
age_group = tab.excel_ref('C5').expand(RIGHT).is_not_blank() #- tab.excel_ref('W5').expand(RIGHT)
observations = gender.fill(DOWN).is_not_blank() - tab.excel_ref('B21').expand(DOWN).expand(RIGHT)
dimensions = [
    HDimConst('Measure Type', 'Headcount'),
    HDimConst('Period', '2018'),
    HDim(gender, 'Sex', DIRECTLY, ABOVE), 
    HDimConst('Type of Employment', 'full-time-employees'),
    HDim(responsibility_level, 'Responsibility Level', DIRECTLY, LEFT), 
    HDim(age_group, 'ONS Age Range', CLOSEST, LEFT), 
]
c1 = ConversionSegment(observations, dimensions, processTIMEUNIT=True)
table_23 = c1.topandas()
res_tables = pd.concat([table_23, res_tables], sort=True)

tab = tabs['Table 25']
responsibility_level = tab.excel_ref('C5').expand(RIGHT).is_not_blank()
department = tab.excel_ref('B9').fill(DOWN).is_not_blank() - tab.excel_ref('B193').expand(DOWN)
observations = responsibility_level.fill(DOWN).is_not_blank() - tab.excel_ref('B193').expand(DOWN).expand(RIGHT)
dimensions = [
    HDimConst('Measure Type', 'Median Earnings'),
    HDimConst('Period', '2018'),
    HDimConst('Type of Employment', 'full-time-employees'),
    HDim(department, 'Department', DIRECTLY, LEFT), 
    HDim(responsibility_level, 'Responsibility Level', DIRECTLY, ABOVE), 
]
c1 = ConversionSegment(observations, dimensions, processTIMEUNIT=True)
table_25 = c1.topandas()
res_tables = pd.concat([table_25, res_tables], sort=True)

# +
tab = tabs['Table 26']
responsibility_level = tab.excel_ref('C5').expand(RIGHT).is_not_blank()
area_code = tab.excel_ref('A8').fill(DOWN) - tab.excel_ref('A25').expand(DOWN)
region = tab.excel_ref('B8').fill(DOWN).is_not_blank() - tab.excel_ref('B25').expand(DOWN)
observations = responsibility_level.fill(DOWN).is_not_blank() - tab.excel_ref('B25').expand(DOWN).expand(RIGHT)
dimensions = [
    HDimConst('Measure Type', 'Median Earnings'),
    HDimConst('Period', '2018'),
    HDimConst('Type of Employment', 'full-time-employees'),
    #HDim(area_code, 'ONS area code', DIRECTLY, LEFT), 
    HDim(region, 'Region name', DIRECTLY, LEFT),
    HDim(responsibility_level, 'Responsibility Level', DIRECTLY, ABOVE), 
]
c1 = ConversionSegment(observations, dimensions, processTIMEUNIT=True)
table_26 = c1.topandas()

res_tables = pd.concat([table_26, res_tables], sort=True)
# -

tab = tabs['Table 27']
responsibility_level = tab.excel_ref('B8').expand(DOWN).is_not_blank() - tab.excel_ref('B20').expand(DOWN)
ethnicity = tab.excel_ref('C5').expand(RIGHT).is_not_blank()
observations = ethnicity.fill(DOWN).is_not_blank() - tab.excel_ref('B20').expand(DOWN).expand(RIGHT)
dimensions = [
    HDimConst('Measure Type', 'Median Earnings'),
    HDimConst('Period', '2018'),
    HDimConst('Type of Employment', 'full-time-employees'),
    HDim(ethnicity, 'Ethnicity', DIRECTLY, ABOVE),
    HDim(responsibility_level, 'Responsibility Level', DIRECTLY, LEFT), 
]
c1 = ConversionSegment(observations, dimensions, processTIMEUNIT=True)
table_27 = c1.topandas()
res_tables = pd.concat([table_27, res_tables], sort=True)

tab = tabs['Table 28']
responsibility_level = tab.excel_ref('B8').expand(DOWN).is_not_blank() - tab.excel_ref('B20').expand(DOWN)
remove = tab.excel_ref('H5')
disability_status = tab.excel_ref('C5').expand(RIGHT).is_not_blank() - remove
observations = disability_status.fill(DOWN).is_not_blank() - remove.expand(DOWN) - tab.excel_ref('B20').expand(DOWN).expand(RIGHT)
dimensions = [
    HDimConst('Measure Type', 'Median Earnings'),
    HDimConst('Period', '2018'),
    HDimConst('Department', 'all'),
    HDimConst('Type of Employment', 'full-time-employees'),
    HDim(disability_status, 'Disability Status', DIRECTLY, ABOVE),
    HDim(responsibility_level, 'Responsibility Level', DIRECTLY, LEFT), 
]
c1 = ConversionSegment(observations, dimensions, processTIMEUNIT=True)
table_28 = c1.topandas()
res_tables = pd.concat([table_28, res_tables], sort=True)

tab = tabs['Table 29']
measure_type = tab.excel_ref('C5').expand(RIGHT).is_not_blank()
department = tab.excel_ref('B11').expand(DOWN).is_not_blank() - tab.excel_ref('B194').expand(DOWN)
remove_1 = tab.excel_ref('E6')
remove_2 = tab.excel_ref('I6')
gender = tab.excel_ref('C6').expand(RIGHT).is_not_blank() - remove_1 - remove_2
observations = gender.fill(DOWN).is_not_blank() - tab.excel_ref('B194').expand(DOWN).expand(RIGHT) - remove_1.expand(DOWN) - remove_2.expand(DOWN)
dimensions = [
    HDimConst('Period', '2018'),
    HDimConst('ONS Age Range', 'all'),
    HDimConst('Type of Employment', 'full-time-employees'),
    HDim(gender, 'Sex', DIRECTLY, ABOVE),
    HDim(department, 'Department', DIRECTLY, LEFT), 
    HDim(measure_type, 'Measure Type', CLOSEST, LEFT),
]
c1 = ConversionSegment(observations, dimensions, processTIMEUNIT=True)
table_29 = c1.topandas()
res_tables = pd.concat([table_29, res_tables], sort=True)

tab = tabs['Table 30']
measure_type = tab.excel_ref('C5').expand(RIGHT).is_not_blank()
department = tab.excel_ref('B11').expand(DOWN).is_not_blank() - tab.excel_ref('B194').expand(DOWN)
remove_1 = tab.excel_ref('E6')
remove_2 = tab.excel_ref('I6')
gender = tab.excel_ref('C6').expand(RIGHT).is_not_blank() - remove_1 - remove_2
observations = gender.fill(DOWN).is_not_blank() - tab.excel_ref('B194').expand(DOWN).expand(RIGHT) - remove_1.expand(DOWN) - remove_2.expand(DOWN)
dimensions = [
    HDimConst('Period', '2018'),
    HDimConst('ONS Age Range', 'all'),
    HDimConst('Type of Employment', 'part-time-employees'),
    HDim(gender, 'Sex', DIRECTLY, ABOVE),
    HDim(department, 'Department', DIRECTLY, LEFT), 
    HDim(measure_type, 'Measure Type', CLOSEST, LEFT),
]
c1 = ConversionSegment(observations, dimensions, processTIMEUNIT=True)
table_30 = c1.topandas()
res_tables = pd.concat([table_30, res_tables], sort=True)

tab = tabs['Table 31']
measure_type = tab.excel_ref('C5').expand(RIGHT).is_not_blank()
department = tab.excel_ref('B11').expand(DOWN).is_not_blank() - tab.excel_ref('B194').expand(DOWN)
remove_1 = tab.excel_ref('E6')
remove_2 = tab.excel_ref('I6')
gender = tab.excel_ref('C6').expand(RIGHT).is_not_blank() - remove_1 - remove_2
observations = gender.fill(DOWN).is_not_blank() - tab.excel_ref('B194').expand(DOWN).expand(RIGHT) - remove_1.expand(DOWN) - remove_2.expand(DOWN)
dimensions = [
    HDimConst('Period', '2018'),
    HDimConst('ONS Age Range', 'all'),
    HDimConst('Type of Employment', 'full-time-equivalent'),
    HDim(gender, 'Sex', DIRECTLY, ABOVE),
    HDim(department, 'Department', DIRECTLY, LEFT), 
    HDim(measure_type, 'Measure Type', CLOSEST, LEFT),
]
c1 = ConversionSegment(observations, dimensions, processTIMEUNIT=True)
table_31 = c1.topandas()
res_tables = pd.concat([table_31, res_tables], sort=True)

tab = tabs['Table 32']
responsibility_level = tab.excel_ref('C5').expand(RIGHT).is_not_blank()
remove_1 = tab.excel_ref('E6')
remove_2 = tab.excel_ref('I6')
remove_3 = tab.excel_ref('M6')
remove_4 = tab.excel_ref('Q6')
remove_5 = tab.excel_ref('U6')
department = tab.excel_ref('B11').expand(DOWN).is_not_blank() - tab.excel_ref('B194').expand(DOWN)
gender = tab.excel_ref('C6').expand(RIGHT).is_not_blank() - remove_1 - remove_2 - remove_3 - remove_4 - remove_5
observations = gender.fill(DOWN).is_not_blank() - tab.excel_ref('B194').expand(DOWN).expand(RIGHT) - remove_1.expand(DOWN) - remove_2.expand(DOWN) - remove_3.expand(DOWN) - remove_4.expand(DOWN) - remove_5.expand(DOWN)
dimensions = [
    HDimConst('Measure Type', 'Median Earnings'),
    HDimConst('Period', '2018'),
    HDim(gender, 'Sex', DIRECTLY, ABOVE),
    HDim(responsibility_level, 'Responsibility Level', CLOSEST, LEFT), 
    HDim(department, 'Department', DIRECTLY, LEFT),
]
c1 = ConversionSegment(observations, dimensions, processTIMEUNIT=True)
table_32 = c1.topandas()
res_tables = pd.concat([table_32, res_tables], sort=True)

tab = tabs['Table 33']
responsibility_level = tab.excel_ref('C5').expand(RIGHT).is_not_blank()
remove_1 = tab.excel_ref('E6')
remove_2 = tab.excel_ref('I6')
remove_3 = tab.excel_ref('M6')
remove_4 = tab.excel_ref('Q6')
remove_5 = tab.excel_ref('U6')
department = tab.excel_ref('B11').expand(DOWN).is_not_blank() - tab.excel_ref('B194').expand(DOWN)
gender = tab.excel_ref('C6').expand(RIGHT).is_not_blank() - remove_1 - remove_2 - remove_3 - remove_4 - remove_5
observations = gender.fill(DOWN).is_not_blank() - tab.excel_ref('B194').expand(DOWN).expand(RIGHT) - remove_1.expand(DOWN) - remove_2.expand(DOWN) - remove_3.expand(DOWN) - remove_4.expand(DOWN) - remove_5.expand(DOWN)
dimensions = [
    HDimConst('Measure Type', 'Mean Earnings'),
    HDimConst('Period', '2018'),
    HDim(gender, 'Sex', DIRECTLY, ABOVE),
    HDim(responsibility_level, 'Responsibility Level', CLOSEST, LEFT), 
    HDim(department, 'Department', DIRECTLY, LEFT),
]
c1 = ConversionSegment(observations, dimensions, processTIMEUNIT=True)
table_33 = c1.topandas() 
res_tables = pd.concat([table_33, res_tables], sort=True)

# +
tab = tabs['Table 34']
cells_to_remove = ['A11', 'A16', 'A21', 'A26', 'A31', 'A36']
employee_type = tab.excel_ref('A10').expand(DOWN).is_not_blank() - tab.excel_ref('A40').expand(DOWN)
for cell in cells_to_remove:
    employee_type = employee_type - tab.excel_ref(cell)
responsibility_level = tab.excel_ref('A10').expand(DOWN).is_not_blank() - tab.excel_ref('A40').expand(DOWN) - employee_type
year = tab.excel_ref('B6').expand(RIGHT).is_not_blank()
observations = year.fill(DOWN).is_not_blank() - tab.excel_ref('A40').expand(DOWN).expand(RIGHT) 
#savepreviewhtml(observations)

dimensions = [
    HDimConst('Measure Type', 'Median gender pay gap in percent'),
    HDim(year, 'Period', DIRECTLY, ABOVE),
    HDim(responsibility_level, 'Responsibility Level', CLOSEST, ABOVE), 
    HDim(employee_type, 'Type of Employment', DIRECTLY, LEFT), 

]
c1 = ConversionSegment(observations, dimensions, processTIMEUNIT=True)
table_34 = c1.topandas()
res_tables = pd.concat([table_34, res_tables], sort=True)
# + {}
res_tables.rename(columns={'OBS': 'Value'}, inplace=True)
if 'DATAMARKER' in res_tables.columns:
    print('marker found in columns')
    res_tables['DATAMARKER'].replace('..', 'between-one-and-five', inplace=True)
    res_tables['DATAMARKER'].replace('-', 'not-applicable', inplace=True)
    res_tables = res_tables.rename(columns={'DATAMARKER':'Marker'})
    res_tables['Marker'] = res_tables['Marker'].fillna(value='not-applicable')
else:
    print('marker not found in colmns making it')
    res_tables['DATAMARKER'] = 'not-applicable'
    res_tables = res_tables.rename(columns={'DATAMARKER':'Marker'})
    
#res_tables['Sex'] = res_tables['Sex'].map(lambda x: pathify(x))
res_tables = res_tables.replace({'Sex' : {'Male' : 'M','Female' : 'F','Total' : 'T',' ' : 'U' }})
res_tables = res_tables.replace({'Sex' : {'Male23' : 'M','Female23' : 'F','total' : 'T' }})
res_tables = res_tables.replace({'Sex' : {'Male19' : 'M','Female19' : 'F','total' : 'T' }})
res_tables['Sex'] = res_tables['Sex'].fillna(value='U')
res_tables['Department'] = res_tables['Department'].fillna(value='all').map(lambda x: pathify(x))
res_tables = res_tables.replace({'Type of Employment' : 
                               {'  Full-time4' : 'full-time-employees',
                                '  Part-time5' : 'part-time-employees',
                                '  All5' : 'all-employees',}})
res_tables['Type of Employment'] = res_tables['Type of Employment'].fillna(value='all-employees').map(lambda x: pathify(x))
res_tables['Region name'] = res_tables['Region name'].fillna(value='All regions').map(lambda x: pathify(x))
res_tables['Responsibility Level'] = res_tables['Responsibility Level'].fillna(value='all').map(lambda x: pathify(x))
res_tables = res_tables.replace({'Ethnicity' : 
                              {'Not Declared5' : 'Not Declared',
                               'Not Reported6' : 'Not Reported',
                               'Not Declared3' : 'Not Declared',
                               'Not Reported4' : 'Not Reported',}})
res_tables['Ethnicity'] = res_tables['Ethnicity'].fillna(value='all').map(lambda x: pathify(x))
res_tables = res_tables.replace({'Disability Status' : 
                               {'Not Declared5' : 'Not Declared',
                                'Not Reported6' : 'Not Reported',
                                'Not Declared3' : 'Not Declared',
                                'Not Reported3' : 'Not Reported',}})
res_tables['Disability Status'] = res_tables['Disability Status'].fillna(value='unknown').map(lambda x: pathify(x))
res_tables['ONS Age Range'] = res_tables['ONS Age Range'].fillna(value='all').map(lambda x: pathify(x))
res_tables = res_tables.replace({'Period' : {
    '2007.0' : '2007', '2008.0' : '2008', '2009.0' : '2009', '2010.0' : '2010',
    '2011.0' : '2011', '2012.0' : '2012', '2013.0' : '2013', '2014.0' : '2014', 
    '2015.0' : '2015', '2016.0' : '2016', '2017.0' : '2017', '2018.0' : '2018'}})
res_tables['Period'] = 'year/' + res_tables['Period']
res_tables
# -

