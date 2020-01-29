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

from gssutils import *
from gssutils.metadata import THEME
import pandas as pd

next_table = pd.DataFrame()

# +
# %%capture

#Statistical Bulletin Tables
# %run "Statistical_Bulletin_Tables.py"
next_table = pd.concat([next_table, stats_tables])

#Responsibility Level / earnings
# %run "Responsibility_Level_and_Earnings_Tables.py"
next_table = pd.concat([next_table, res_tables])

#Government Department
# %run "Government_Department_tables.py"
next_table = pd.concat([next_table, gov_tables])

#Entrants and Leavers
# %run "Entrants_and_Leavers_tables.py"
next_table = pd.concat([next_table, entry_leave_tables])

############################################
#extracted regional tabs into their own cube  for now 
#Regional tables
# %run "Civil_Service_Statistics_Regional_tables.py"
#res_tables
# -

next_table = next_table [['Period', 'Disability Status', 'Responsibility Level', 'Department', 'ONS Age Range', 
                          'Sex', 'Type of Employment', 'Status of Employment', 'Salary Band', 'Profession of Post', 
                          'Nationality', 'Ethnicity', 'Entrants or Leavers', 'Region name', 
                          'Value', 'Marker', 'Measure Type']] #,'ONS area code','NUTS Area Code','NUTS Region name'

next_table = next_table.replace({'Department' : 
                                 {'Ministry of Housing, Communities and Local Government (excl. agencies)1' : 'Ministry of Housing, Communities and Local Government (excl. agencies)',
                                  'Ministry of Housing, Communities and Local Government (excl. agencies)3' : 'Ministry of Housing, Communities and Local Government (excl. agencies)',
                                  'Ministry of Housing, Communities and Local Government (excl. agencies)2' : 'Ministry of Housing, Communities and Local Government (excl. agencies)',
                                  'Ministry of Housing, Communities and Local Government (excl. agencies)4' : 'Ministry of Housing, Communities and Local Government (excl. agencies)',
                                  'Ministry of Housing, Communities and Local Government (excl. agencies)5' : 'Ministry of Housing, Communities and Local Government (excl. agencies)',
                                  'Ministry of Housing, Communities and Local Government (excl. agencies)6' : 'Ministry of Housing, Communities and Local Government (excl. agencies)',
                                  'Ministry of Housing, Communities and Local Government (excl. agencies)7' : 'Ministry of Housing, Communities and Local Government (excl. agencies)',
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
                                  #'Education and Skills Funding Agency6' : 'Education and Skills Funding Agency',
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

next_table['Disability Status'] = next_table['Disability Status'].fillna(value='unknown').map(lambda x: pathify(x))
next_table['Marker'] = next_table['Marker'].map(lambda x: pathify(x))
next_table['ONS Age Range'] = next_table['ONS Age Range'].fillna(value='all').map(lambda x: pathify(x))
next_table['Entrants or Leavers'] = next_table['Entrants or Leavers'].fillna(value='all').map(lambda x: pathify(x))
next_table['Nationality'] = next_table['Nationality'].fillna(value='all').map(lambda x: pathify(x))
next_table['Profession of Post'] = next_table['Profession of Post'].fillna(value='all').map(lambda x: pathify(x))
next_table['Salary Band'] = next_table['Salary Band'].fillna(value='unknown').map(lambda x: pathify(x))
next_table['Status of Employment'] = next_table['Status of Employment'].fillna(value='All').map(lambda x: pathify(x))
next_table['Region name'] = next_table['Region name'].fillna(value='All regions').map(lambda x: pathify(x))
next_table['Department'] = next_table['Department'].map(lambda x: pathify(x))
next_table['Responsibility Level'] = next_table['Responsibility Level'].fillna(value='all').map(lambda x: pathify(x))
next_table['Type of Employment'] = next_table['Type of Employment'].fillna(value='All employees').map(lambda x: pathify(x))
next_table = next_table.replace({'Sex' : {'Male' : 'M','Female' : 'F','Total' : 'T','' : 'U' }})
next_table = next_table.replace({'Sex' : {'Male ' : 'M','Female' : 'F','Total' : 'T' }})
next_table['Sex'] = next_table['Sex'].fillna(value='U')
next_table = next_table.replace({'Sex' : {'not-reported' : 'U' }})
#next_table = next_table.rename(columns={'Marker':'Markers'})
next_table

destinationFolder = Path('out')
destinationFolder.mkdir(exist_ok=True, parents=True) 

# +
import numpy as np
from gssutils.metadata import THEME
scraper.set_base_uri('http://gss-data.org.uk')
scraper.dataset.family = 'disability'
scraper.dataset.theme = THEME['health-social-care']

tblSet = [next_table,regional_tables]
i = 1
for t in tblSet:
    fleNme = 'observations-' + str(i) + '.csv'
    t.drop_duplicates().to_csv(destinationFolder / (fleNme), index = False)
    scraper.set_dataset_id(f'gss_data/disability/ONS-Civil-Service-Statistics/observations-{i}/')
    
    with open(destinationFolder / (fleNme + '-metadata.trig'), 'wb') as metadata:metadata.write(scraper.generate_trig())

    csvw = CSVWMetadata('https://gss-cogs.github.io/family-disability/reference/')
    csvw.create(destinationFolder / fleNme, destinationFolder / (fleNme + '-schema.json'))
    i = i + 1
# -


