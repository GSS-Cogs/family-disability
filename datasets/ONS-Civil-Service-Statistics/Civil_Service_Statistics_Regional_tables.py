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


# Table 12 : Civil Service employment; regional distribution by government department

# +
#######################################################
#Regional tables 12-19
#Removed observations without area codes (Overseas, not reported and all employees)
#As well as NUTS area code 

tabs = {tab.name: tab for tab in scraper.distribution(latest=True).as_databaker()}
regional_tables = pd.DataFrame()
# -

tab = tabs['Table 12']
region = tab.excel_ref('C6').expand(RIGHT).is_not_blank() 
department = tab.excel_ref('B10').fill(DOWN).is_not_blank() - tab.excel_ref('B17') - tab.excel_ref('B26') - tab.excel_ref('B29') - tab.excel_ref('B33') - tab.excel_ref('B37') - tab.excel_ref('B40') - tab.excel_ref('B45') - tab.excel_ref('B48') - tab.excel_ref('B51') - tab.excel_ref('B58') - tab.excel_ref('B61') - tab.excel_ref('B64') - tab.excel_ref('B70') - tab.excel_ref('B77') - tab.excel_ref('B80') - tab.excel_ref('B83') - tab.excel_ref('B88') - tab.excel_ref('B93') - tab.excel_ref('B96') - tab.excel_ref('B100') - tab.excel_ref('B107') - tab.excel_ref('B110') - tab.excel_ref('B113') - tab.excel_ref('B121') - tab.excel_ref('B124') - tab.excel_ref('B127') - tab.excel_ref('B130') - tab.excel_ref('B133') - tab.excel_ref('B136') - tab.excel_ref('B139') - tab.excel_ref('B142') - tab.excel_ref('B145') - tab.excel_ref('B148') - tab.excel_ref('B167')- tab.excel_ref('B174') - tab.excel_ref('B77') - tab.excel_ref('B180') - tab.excel_ref('B183') - tab.excel_ref('B186') - tab.excel_ref('B189') - tab.excel_ref('B195').expand(DOWN)
observations = tab.excel_ref('C10').expand(RIGHT).expand(DOWN).is_not_blank() - tab.excel_ref('O10').expand(RIGHT).expand(DOWN) - tab.excel_ref('B195').expand(RIGHT).expand(DOWN)
#savepreviewhtml(department)
dimensions = [
    HDimConst('Measure Type', 'Headcount'),
    HDimConst('Period', '2018'),
    HDim(department, 'Department', DIRECTLY, LEFT),
    HDim(region, 'Region name', DIRECTLY, ABOVE),
]
c1 = ConversionSegment(observations, dimensions, processTIMEUNIT=True)
table_12 = c1.topandas()
regional_tables = pd.concat([table_12, regional_tables])

# +
#table 13 
tab = tabs['Table 13']
employment_status = tab.excel_ref('B5').expand(RIGHT).is_not_blank()
gender = tab.excel_ref('B6').expand(RIGHT).is_not_blank()
employment_type = tab.excel_ref('B7').expand(RIGHT).is_not_blank()
region = tab.excel_ref('B10').expand(DOWN).is_not_blank() - tab.excel_ref('B30').expand(DOWN)
area_code = tab.excel_ref('A10').expand(DOWN) - tab.excel_ref('A30').expand(DOWN)
observations = employment_type.fill(DOWN).is_not_blank() - tab.excel_ref('A25').expand(DOWN).expand(RIGHT)
#savepreviewhtml(area_code)

dimensions = [
    HDimConst('Measure Type', 'Headcount'),
    HDimConst('Department', 'all'),
    HDimConst('Period', '2018'),
    HDim(employment_type, 'Type of Employment', DIRECTLY, ABOVE),
    HDim(gender, 'Sex', CLOSEST, LEFT),
    HDim(employment_status, 'Status of Employment', CLOSEST, LEFT),
    HDim(region, 'Region name', DIRECTLY, LEFT),
    HDim(area_code, 'ONS area code', DIRECTLY, LEFT),  
    
]
c1 = ConversionSegment(observations, dimensions, processTIMEUNIT=True)
table13 = c1.topandas()
regional_tables = pd.concat([table13, regional_tables], sort=True)

# +
tab = tabs['Table 14']
gender = tab.excel_ref('B6').expand(RIGHT).is_not_blank()
employment_type = tab.excel_ref('B7').expand(RIGHT).is_not_blank()
employment_status = tab.excel_ref('B5').expand(RIGHT).is_not_blank()

region_cells_to_remove = ['B11', 'B15', 'B22', 'B28', 'B33', 'B38', 'B43', 'B50', 'B56', 'B62', 'B66' ]
nuts_region = tab.excel_ref('B12').expand(DOWN).is_not_blank() - tab.excel_ref('B80').expand(DOWN)
for cell in region_cells_to_remove:
    nuts_region = nuts_region - tab.excel_ref(cell)

nuts_region_cells_to_remove = ['B11', 'B15', 'B22', 'B28', 'B33', 'B38', 'B43', 'B50', 'B56', 'B62', 'B66', '73' ] 
region2 = tab.excel_ref('B12').expand(DOWN).is_not_blank() - tab.excel_ref('B80').expand(DOWN)
for cell in nuts_region_cells_to_remove:
    region2 = region2 - tab.excel_ref(cell)
region = tab.excel_ref('B10').expand(DOWN).is_not_blank() - region2 - tab.excel_ref('B80').expand(DOWN)

NUTS_code = tab.excel_ref('A12').expand(DOWN) - tab.excel_ref('A80').expand(DOWN)
observations = employment_type.fill(DOWN).is_not_blank() - tab.excel_ref('B74').expand(DOWN).expand(RIGHT)
#savepreviewhtml(region)
dimensions = [
    HDimConst('Measure Type', 'Headcount'),
    HDimConst('Period', '2018'),
    HDim(employment_type, 'Type of Employment', DIRECTLY, ABOVE),
    HDim(gender, 'Sex', CLOSEST, LEFT),
    HDim(employment_status, 'Status of Employment', CLOSEST, LEFT),
    HDim(region, 'Region name', CLOSEST, ABOVE),
    HDim(nuts_region, 'NUTS Region name',DIRECTLY, LEFT ),
    HDim(NUTS_code, 'NUTS Area Code', DIRECTLY, LEFT),
]
c1 = ConversionSegment(observations, dimensions, processTIMEUNIT=True)
#savepreviewhtml(c1)
table14 = c1.topandas()
regional_tables = pd.concat([table14, regional_tables], sort=True)

# +
tab = tabs['Table 15']
cells_to_remove = ['B12', 'B17', 'B26', 'B32', 'B39', 'B43', 'B50', 'B54', 'B57', 'B60', 'B67', 'B74',
                   'B79', 'B83', 'B87','B92', 'B102', 'B109', 'B114', 'B123', 'B128', 'B134','B139', 'B143', 
                   'B151', 'B156', 'B163', 'B177', 'B178', 'B184', 'B188', 'B190','B196', 'B205', 'B212', 
                   'B221', 'B230', 'B232']
cells_to_remove2 = ['B11', 'B22', 'B49', 'B66', 'B82', 'B101', 'B122', 'B150', 'B177', 'B195', 'B211', 'B240', ]

nuts_region = tab.excel_ref('B10').expand(DOWN).is_not_blank() - tab.excel_ref('B252').expand(DOWN)
for cell in cells_to_remove:
    nuts_region = nuts_region - tab.excel_ref(cell)
for cell in cells_to_remove2:
    nuts_region = nuts_region - tab.excel_ref(cell)

region = tab.excel_ref('B10').expand(DOWN).is_not_blank() - nuts_region - tab.excel_ref('B252').expand(DOWN)
for cell in cells_to_remove:
    region = region - tab.excel_ref(cell)
    
gender = tab.excel_ref('B6').expand(RIGHT).is_not_blank()
employment_status = tab.excel_ref('B5').expand(RIGHT).is_not_blank()
employment_type = tab.excel_ref('B7').expand(RIGHT).is_not_blank()
NUTS_code = tab.excel_ref('A12').expand(DOWN) - tab.excel_ref('A252').expand(DOWN)
observations = employment_type.fill(DOWN).is_not_blank() - tab.excel_ref('B246').expand(DOWN).expand(RIGHT)
#savepreviewhtml(observations)
dimensions = [
    HDimConst('Measure Type', 'Headcount'),
    HDimConst('Period', '2018'),
    HDim(employment_type, 'Type of Employment', DIRECTLY, ABOVE),
    HDim(gender, 'Sex', CLOSEST, LEFT),
    HDim(employment_status, 'Status of Employment', CLOSEST, LEFT),
    HDim(region, 'Region name', CLOSEST, ABOVE),
    HDim(nuts_region, 'NUTS Region name',DIRECTLY, LEFT ),
    HDim(NUTS_code, 'NUTS Area Code', DIRECTLY, LEFT),
]
c1 = ConversionSegment(observations, dimensions, processTIMEUNIT=True)
table_15 = c1.topandas()
regional_tables = pd.concat([table_15, regional_tables], sort=True)
# -

tab = tabs['Table 16']
area_code = tab.excel_ref('A9').expand(DOWN).is_not_blank() - tab.excel_ref('A130').expand(DOWN)
region = tab.excel_ref('B9').expand(DOWN).is_not_blank() - tab.excel_ref('B130').expand(DOWN)
responsibility_level = tab.excel_ref('C9').fill(DOWN).is_not_blank() - tab.excel_ref('c130').expand(DOWN)
gender = tab.excel_ref('D5').expand(RIGHT).is_not_blank() - tab.excel_ref('G5').expand(RIGHT)
observations = gender.fill(DOWN).is_not_blank() - tab.excel_ref('C105').expand(DOWN).expand(RIGHT)
#savepreviewhtml(area_code)
dimensions = [
    HDimConst('Measure Type', 'Headcount'),
    HDimConst('Period', '2018'),
    HDim(area_code, 'ONS area code', CLOSEST, ABOVE), 
    HDim(responsibility_level, 'Responsibility Level', DIRECTLY, LEFT),
    HDim(region, 'Region name', CLOSEST, ABOVE),
    HDim(gender, 'Sex', DIRECTLY, ABOVE),
]
c1 = ConversionSegment(observations, dimensions, processTIMEUNIT=True)
table_16 = c1.topandas()
regional_tables = pd.concat([table_16, regional_tables], sort=True)

tab = tabs['Table 17']
area_code = tab.excel_ref('A8').expand(DOWN).is_not_blank() - tab.excel_ref('A129').expand(DOWN)
region = tab.excel_ref('B8').expand(DOWN).is_not_blank() - tab.excel_ref('B129').expand(DOWN)
responsibility_level = tab.excel_ref('C8').fill(DOWN).is_not_blank() - tab.excel_ref('C129').expand(DOWN)
ethnicity = tab.excel_ref('D5').expand(RIGHT).is_not_blank() - tab.excel_ref('L5').expand(RIGHT)
observations = ethnicity.fill(DOWN).is_not_blank() - tab.excel_ref('C104').expand(DOWN).expand(RIGHT)
#savepreviewhtml(area_code)
dimensions = [
    HDimConst('Measure Type', 'Headcount'),
    HDimConst('Period', '2018'),
    HDim(area_code, 'ONS area code', CLOSEST, ABOVE), 
    HDim(responsibility_level, 'Responsibility Level', DIRECTLY, LEFT),
    HDim(region, 'Region name', CLOSEST, ABOVE),
    HDim(ethnicity, 'Ethnicity', DIRECTLY, ABOVE),
]
c1 = ConversionSegment(observations, dimensions, processTIMEUNIT=True)
table_17 = c1.topandas()
regional_tables = pd.concat([table_17, regional_tables], sort=True)

tab = tabs['Table 18']
area_code = tab.excel_ref('A8').expand(DOWN).is_not_blank() - tab.excel_ref('A130').expand(DOWN)
region = tab.excel_ref('B8').expand(DOWN).is_not_blank() - tab.excel_ref('B130').expand(DOWN)
responsibility_level = tab.excel_ref('C8').fill(DOWN).is_not_blank() - tab.excel_ref('C130').expand(DOWN)
disability_status = tab.excel_ref('D5').expand(RIGHT).is_not_blank() - tab.excel_ref('L5').expand(RIGHT)
observations = disability_status.fill(DOWN).is_not_blank() - tab.excel_ref('C104').expand(DOWN).expand(RIGHT)
#savepreviewhtml(area_code)
dimensions = [
    HDimConst('Measure Type', 'Headcount'),
    HDimConst('Period', '2018'),
    HDim(area_code, 'ONS area code', CLOSEST, ABOVE), 
    HDim(responsibility_level, 'Responsibility Level', DIRECTLY, LEFT),
    HDim(region, 'Region name', CLOSEST, ABOVE),
    HDim(disability_status, 'Disability Status', DIRECTLY, ABOVE),
]
c1 = ConversionSegment(observations, dimensions, processTIMEUNIT=True)
table_18 = c1.topandas()
regional_tables = pd.concat([table_18, regional_tables], sort=True)

tab = tabs['Table 19']
area_code = tab.excel_ref('A8').expand(DOWN).is_not_blank() - tab.excel_ref('A28').expand(DOWN)
region = tab.excel_ref('B8').expand(DOWN).is_not_blank() - tab.excel_ref('B28').expand(DOWN)
age_group = tab.excel_ref('D5').expand(RIGHT).is_not_blank() - tab.excel_ref('L5').expand(RIGHT)
observations = age_group.fill(DOWN).is_not_blank() - tab.excel_ref('B23').expand(RIGHT).expand(DOWN)
#savepreviewhtml(area_code)
dimensions = [
    HDimConst('Measure Type', 'Headcount'),
    HDimConst('Period', '2018'),
    HDim(age_group, 'ONS Age Range', DIRECTLY, ABOVE),
    HDim(area_code, 'ONS area code', CLOSEST, ABOVE), 
    HDim(region, 'Region name', CLOSEST, ABOVE),
]
c1 = ConversionSegment(observations, dimensions, processTIMEUNIT=True)
table_19 = c1.topandas()
regional_tables = pd.concat([table_19, regional_tables], sort=True)

regional_tables = regional_tables.replace({'Department' : 
                                 {'Ministry of Housing, Communities and Local Government (excl. agencies)1' : 'Ministry of Housing, Communities and Local Government (excl. agencies)',
                                  'Ministry of Housing, Communities and Local Government (excl. agencies)3' : 'Ministry of Housing, Communities and Local Government (excl. agencies)',
                                  'Ministry of Housing, Communities and Local Government (excl. agencies)2' : 'Ministry of Housing, Communities and Local Government (excl. agencies)',
                                  'Ministry of Housing, Communities and Local Government (excl. agencies)4' : 'Ministry of Housing, Communities and Local Government (excl. agencies)',
                                  'Ministry of Housing, Communities and Local Government (excl. agencies)5' : 'Ministry of Housing, Communities and Local Government (excl. agencies)',
                                  'Ministry of Housing, Communities and Local Government (excl. agencies)6' : 'Ministry of Housing, Communities and Local Government (excl. agencies)',
                                  'Ministry of Defence4' : 'Ministry of Defence',
                                  'Ministry of Defence6' : 'Ministry of Defence',
                                  'Ministry of Defence5' : 'Ministry of Defence',
                                  'Ministry of Defence7' : 'Ministry of Defence',
                                  'Ministry of Defence8' : 'Ministry of Defence',
                                  'Ministry of Defence9' : 'Ministry of Defence',
                                  'Royal Fleet Auxiliary4' : 'Royal Fleet Auxiliary',
                                  'Royal Fleet Auxiliary5' : 'Royal Fleet Auxiliary',
                                  'Royal Fleet Auxiliary6' : 'Royal Fleet Auxiliary',
                                  'Royal Fleet Auxiliary7' : 'Royal Fleet Auxiliary',
                                  'Royal Fleet Auxiliary8' : 'Royal Fleet Auxiliary',
                                  'Royal Fleet Auxiliary9' : 'Royal Fleet Auxiliary',
                                  'Department for Exiting the European Union5' : 'Department for Exiting the European Union',
                                  'Department for Exiting the European Union6' : 'Department for Exiting the European Union',
                                  'Department for Exiting the European Union7' : 'Department for Exiting the European Union',
                                  'Department for Exiting the European Union8' : 'Department for Exiting the European Union',
                                  'Department for Exiting the European Union9' : 'Department for Exiting the European Union',
                                  'Department for Exiting the European Union10' : 'Department for Exiting the European Union',
                                  'Education and Skills Funding Agency6' : 'Education and Skills Funding Agency',
                                  'Education and Skills Funding Agency7' : 'Education and Skills Funding Agency',
                                  'Education and Skills Funding Agency8' : 'Education and Skills Funding Agency',
                                  'Education and Skills Funding Agency9' : 'Education and Skills Funding Agency',
                                  'Education and Skills Funding Agency10' : 'Education and Skills Funding Agency',
                                  'Education and Skills Funding Agency11' : 'Education and Skills Funding Agency',
                                  'Veterinary Medicines Directorate ' : 'Veterinary Medicines Directorate',
                                  'Charity Commission ' : 'Charity Commission',
                                  'ESTYN ' : 'ESTYN',
                                  "Department for Business, Energy and Industrial Strategy (excl. agencies')" : "Department for Business, Energy and Industrial Strategy (excl. agencies)",
                                  'Department of Health and Social Care (excl. agencies)10 ' : 'Department of Health and Social Care (excl. agencies)',
                                  'Department of Health and Social Care (excl. agencies)10' : 'Department of Health and Social Care (excl. agencies)',
                                  'Department of Health and Social Care (excl. agencies)9' : 'Department of Health and Social Care (excl. agencies)',
                                  'Department of Health and Social Care (excl. agencies)9 ' : 'Department of Health and Social Care (excl. agencies)',
                                  'Department of Health and Social Care (excl. agencies)11 ' : 'Department of Health and Social Care (excl. agencies)',
                                  'Department of Health and Social Care (excl. agencies)11' : 'Department of Health and Social Care (excl. agencies)',
                                  'Department of Health and Social Care (excl. agencies)12 ' : 'Department of Health and Social Care (excl. agencies)',
                                  'Department of Health and Social Care (excl. agencies)13 ' : 'Department of Health and Social Care (excl. agencies)',
                                  'Department of Health and Social Care (excl. agencies)8 ' : 'Department of Health and Social Care (excl. agencies)',
                                  'Public Health England9 10' : 'Public Health England',
                                  'Public Health England10 11' : 'Public Health England',
                                  'Public Health England11 12' : 'Public Health England',
                                  'Public Health England13 14' : 'Public Health England',
                                  'Public Health England14 15' : 'Public Health England',
                                  'National Infrastructure Commission12' : 'National Infrastructure Commission',
                                  'National Infrastructure Commission14' : 'National Infrastructure Commission',
                                  'National Infrastructure Commission16' : 'National Infrastructure Commission',
                                  'National Infrastructure Commission13' : 'National Infrastructure Commission',
                                  'National Infrastructure Commission11' : 'National Infrastructure Commission',
                                  'National Infrastructure Commission17' : 'National Infrastructure Commission',
                                  'Ministry of Justice (excl. agencies) ' : 'Ministry of Justice (excl. agencies)',
                                  "Her Majesty's Prison and Probation Service15" : "Her Majesty's Prison and Probation Service",
                                  "Her Majesty's Prison and Probation Service16" : "Her Majesty's Prison and Probation Service",
                                  "Her Majesty's Prison and Probation Service17" : "Her Majesty's Prison and Probation Service",
                                  "Her Majesty's Prison and Probation Service12" : "Her Majesty's Prison and Probation Service",
                                  "Her Majesty's Prison and Probation Service19" : "Her Majesty's Prison and Probation Service",
                                  "Her Majesty's Prison and Probation Service20" : "Her Majesty's Prison and Probation Service",
                                  'Office of Rail and Road ' : 'Office of Rail and Road',
                                  'Registers of Scotland ' : 'Registers of Scotland',
                                  'UK Space Agency2' : 'UK Space Agency',
                                  'Scottish Fiscal Commission16' : 'Scottish Fiscal Commission',
                                  'Scottish Fiscal Commission17' : 'Scottish Fiscal Commission',
                                  'Scottish Fiscal Commission18' : 'Scottish Fiscal Commission',
                                  'Scottish Fiscal Commission13' : 'Scottish Fiscal Commission',
                                  'Scottish Fiscal Commission20' : 'Scottish Fiscal Commission',
                                  'Scottish Fiscal Commission21' : 'Scottish Fiscal Commission',
                                  'Scottish Prison Service ' : 'Scottish Prison Service',
                                  'Education and Skills Funding Agency6' : 'Education and Skills Funding Agency'
                                 }})


# +
regional_tables.rename(columns={'OBS': 'Value'}, inplace=True)
if 'DATAMARKER' in regional_tables.columns:
    print('marker found in columns')
    regional_tables['DATAMARKER'].replace('..', 'Between one and five', inplace=True)
    regional_tables['DATAMARKER'].replace('-', 'not-applicable', inplace=True)
    regional_tables = regional_tables.rename(columns={'DATAMARKER':'Marker'})
    regional_tables['Marker'] = regional_tables['Marker'].fillna(value='not-applicable')
else:
    print('marker not found in colmns making it')
    regional_tables['DATAMARKER'] = 'not-applicable'
    regional_tables = regional_tables.rename(columns={'DATAMARKER':'Marker'})
    
north_east = regional_tables['Region name'] == 'North East'
regional_tables.loc[north_east, 'ONS area code'] = 'E12000001'
north_west = regional_tables['Region name'] == 'North West'
regional_tables.loc[north_west, 'ONS area code'] = 'E12000002'
yorkshire_humber = regional_tables['Region name'] == 'Yorkshire and The Humber'
regional_tables.loc[yorkshire_humber, 'ONS area code'] = 'E12000003'
east_midlands = regional_tables['Region name'] == 'East Midlands'
regional_tables.loc[east_midlands, 'ONS area code'] = 'E12000004'
west_midlands = regional_tables['Region name'] == 'West Midlands'
regional_tables.loc[west_midlands, 'ONS area code'] = 'E12000005'
east = regional_tables['Region name'] == 'East'
regional_tables.loc[east, 'ONS area code'] = 'E12000006'
london = regional_tables['Region name'] == 'London'
regional_tables.loc[london, 'ONS area code'] = 'E12000007'
south_east = regional_tables['Region name'] == 'South East'
regional_tables.loc[south_east, 'ONS area code'] = 'E12000008'
south_west = regional_tables['Region name'] == 'South West'
regional_tables.loc[south_west, 'ONS area code'] = 'E12000009'
england = regional_tables['Region name'] == 'England'
regional_tables.loc[england, 'ONS area code'] = 'E92000001'
wales = regional_tables['Region name'] == 'Wales'
regional_tables.loc[wales, 'ONS area code'] = 'W92000004'
scotland = regional_tables['Region name'] == 'Scotland'
regional_tables.loc[scotland, 'ONS area code'] = 'S92000003'
n_ireland = regional_tables['Region name'] == 'Northern Ireland'
regional_tables.loc[n_ireland, 'ONS area code'] = 'N92000002'

#selectstring = new_table['Sex'].where(new_table['Age Group'] == 'Not reported') == 'Not reported'
#m1 = (df['c'] >= 0) & (df['c'] <= 43)
m1=(regional_tables['Region name'] =='London') & (regional_tables['NUTS Region name'].isnull())
regional_tables.loc[m1,'NUTS Region name'] = regional_tables.loc[m1,'NUTS Region name'].fillna('All London')
m2=(regional_tables['Region name'] =='North West') & (regional_tables['NUTS Region name'].isnull())
regional_tables.loc[m2,'NUTS Region name'] = regional_tables.loc[m2,'NUTS Region name'].fillna('All North West') 
m3=(regional_tables['Region name'] =='Yorkshire and The Humber') & (regional_tables['NUTS Region name'].isnull())
regional_tables.loc[m3,'NUTS Region name'] = regional_tables.loc[m3,'NUTS Region name'].fillna('All Yorkshire and The Humber')  
m4=(regional_tables['Region name'] =='North East') & (regional_tables['NUTS Region name'].isnull())
regional_tables.loc[m4,'NUTS Region name'] = regional_tables.loc[m4,'NUTS Region name'].fillna('All North East') 
m5=(regional_tables['Region name'] =='East Midlands') & (regional_tables['NUTS Region name'].isnull())
regional_tables.loc[m5,'NUTS Region name'] = regional_tables.loc[m5,'NUTS Region name'].fillna('All East Midlands') 
m6=(regional_tables['Region name'] =='West Midlands') & (regional_tables['NUTS Region name'].isnull())
regional_tables.loc[m6,'NUTS Region name'] = regional_tables.loc[m6,'NUTS Region name'].fillna('All West Midlands') 
m7=(regional_tables['Region name'] =='East') & (regional_tables['NUTS Region name'].isnull())
regional_tables.loc[m7,'NUTS Region name'] = regional_tables.loc[m7,'NUTS Region name'].fillna('All East') 
m8=(regional_tables['Region name'] =='South East') & (regional_tables['NUTS Region name'].isnull())
regional_tables.loc[m8,'NUTS Region name'] = regional_tables.loc[m8,'NUTS Region name'].fillna('All South East') 
m9=(regional_tables['Region name'] =='South West') & (regional_tables['NUTS Region name'].isnull())
regional_tables.loc[m9,'NUTS Region name'] = regional_tables.loc[m9,'NUTS Region name'].fillna('All South West') 
m10=(regional_tables['Region name'] =='Wales') & (regional_tables['NUTS Region name'].isnull())
regional_tables.loc[m10,'NUTS Region name'] = regional_tables.loc[m10,'NUTS Region name'].fillna('All Wales') 
m11=(regional_tables['Region name'] =='Scotland') & (regional_tables['NUTS Region name'].isnull())
regional_tables.loc[m11,'NUTS Region name'] = regional_tables.loc[m11,'NUTS Region name'].fillna('All Scotland') 
m12=(regional_tables['Region name'] =='Northern Ireland') & (regional_tables['NUTS Region name'].isnull())
regional_tables.loc[m12,'NUTS Region name'] = regional_tables.loc[m12,'NUTS Region name'].fillna('All Northern Ireland') 
m13=(regional_tables['Region name'] =='England') & (regional_tables['NUTS Region name'].isnull())
regional_tables.loc[m13,'NUTS Region name'] = regional_tables.loc[m13,'NUTS Region name'].fillna('All England') 


regional_tables = regional_tables.replace({'Sex' : {'Male' : 'M','Female' : 'F','Total' : 'T', ' ' : 'U' }})
regional_tables = regional_tables.replace({'Sex' : {'Male ' : 'M','Female ' : 'F','Total ' : 'T', '' : 'U' }})
regional_tables['Sex'] = regional_tables['Sex'].fillna(value='U')
regional_tables['Department'] = regional_tables['Department'].fillna(value='all').map(lambda x: pathify(x))
regional_tables['Status of Employment'] = regional_tables['Status of Employment'].fillna(value='All')#.map(lambda x: pathify(x))
regional_tables = regional_tables.replace({'Type of Employment' : {'Full Time' : 'Full Time Employees','Part Time' : 'Part Time Employees','Total' : 'All Employees' }})
regional_tables = regional_tables.replace({'Type of Employment' : 
                               {'full-time' : 'Full-time employees',
                                'part-time' : 'Part-time employees',}})
regional_tables['Type of Employment'] = regional_tables['Type of Employment'].fillna(value='All employees')#.map(lambda x: pathify(x))
regional_tables['Region name'] = regional_tables['Region name'].map(lambda x: pathify(x))
regional_tables['NUTS Region name'] = regional_tables['NUTS Region name'].map(lambda x: pathify(x))
regional_tables['Responsibility Level'] = regional_tables['Responsibility Level'].fillna(value='all').map(lambda x: pathify(x))
regional_tables = regional_tables.replace({'Ethnicity' : 
                               {'Not Declared6' : 'Not Declared',
                                'Not Reported7' : 'Not Reported',}})
regional_tables['Ethnicity'] = regional_tables['Ethnicity'].fillna(value='all').map(lambda x: pathify(x))

regional_tables = regional_tables.replace({'Disability Status' : 
                               {'Not Declared6' : 'Not Declared',
                                'Not Reported7' : 'Not Reported',}})
regional_tables['Disability Status'] = regional_tables['Disability Status'].fillna(value='unknown').map(lambda x: pathify(x))
regional_tables['ONS Age Range'] = regional_tables['ONS Age Range'].fillna(value='all').map(lambda x: pathify(x))
regional_tables['Period'] = 'year/' + regional_tables['Period']
#regional_tables['NUTS Area Code'] = regional_tables['NUTS Area Code'].map(lambda x: pathify(x))
regional_tables['Marker'] = regional_tables['Marker'].map(lambda x: pathify(x))
#Drop nuts area code for now 
regional_tables = regional_tables [['Period', 'Disability Status', 'Responsibility Level', 'Department', 'ONS Age Range', 
                        'Sex', 'Type of Employment', 'Status of Employment','Ethnicity',
                        'Region name', 'NUTS Region name', 'Value', 'Marker', 'Measure Type']] # 'ONS area code',
regional_tables
# -




