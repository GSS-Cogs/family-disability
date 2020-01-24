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
next_table['Disability Status'] = next_table['Disability Status'].fillna(value='unknown').map(lambda x: pathify(x))
next_table['ONS Age Range'] = next_table['ONS Age Range'].fillna(value='all').map(lambda x: pathify(x))
next_table['Entrants or Leavers'] = next_table['Entrants or Leavers'].fillna(value='all').map(lambda x: pathify(x))
next_table['Nationality'] = next_table['Nationality'].fillna(value='all').map(lambda x: pathify(x))
next_table['Profession of Post'] = next_table['Profession of Post'].fillna(value='all').map(lambda x: pathify(x))
next_table['Salary Band'] = next_table['Salary Band'].fillna(value='unknown').map(lambda x: pathify(x))
next_table['Status of Employment'] = next_table['Status of Employment'].fillna(value='all').map(lambda x: pathify(x))
next_table['Region name'] = next_table['Region name'].fillna(value='All regions').map(lambda x: pathify(x))
next_table['Responsibility Level'] = next_table['Responsibility Level'].fillna(value='all').map(lambda x: pathify(x))
next_table['Type of Employment'] = next_table['Type of Employment'].fillna(value='all-employees').map(lambda x: pathify(x))
next_table = next_table.replace({'Sex' : {'Male' : 'M','Female' : 'F','Total' : 'T','' : 'U' }})
next_table = next_table.replace({'Sex' : {'Male ' : 'M','Female' : 'F','Total' : 'T' }})
next_table['Sex'] = next_table['Sex'].fillna(value='U')
next_table = next_table.replace({'Sex' : {'not-reported' : 'U' }})
next_table

destinationFolder = Path('out')
destinationFolder.mkdir(exist_ok=True, parents=True)
#OBS_ID = pathify(TITLE)
#civil-service-statistics
#next_table.drop_duplicates().to_csv(destinationFolder / 'civil-service-statistics.csv', index = False)
#civil-service-statistics-regional
#res_tables.drop_duplicates().to_csv(destinationFolder / 'civil-service-statistics-regional.csv', index = False)    

# +
import numpy as np
from gssutils.metadata import THEME

tblSet = [next_table,regional_tables]
i = 1
for t in tblSet:
    fleNme = 'observations-' + str(i) + '.csv'
    t.drop_duplicates().to_csv(destinationFolder / (fleNme), index = False)
    scraper.set_dataset_id(f'gss_data/disability/ONS-Civil-Service-Statistics/observations-{i}/')
    scraper.dataset.family = 'disability'
    
    with open(destinationFolder / ('pre' + fleNme + '-metadata.trig'), 'wb') as metadata:metadata.write(scraper.generate_trig())

    csvw = CSVWMetadata('https://gss-cogs.github.io/family-disability/reference/')
    csvw.create(destinationFolder / fleNme, destinationFolder / (fleNme + '-schema.json'))
    i = i + 1
# -

headSet = [
    'civil-service-statistics',
    'Civil_Service_Statistics_Regional',
]
headMain = 'Civil Service Statistics (unvalidated)'
#
# # +
#### As each trig file is created multiple @prefix ns lines are added. This code gets rid of them
import os
i = 1 #### Main looping index
k = 1 #### Secondary index to skip over lines with ns2
lineWanted = False
#### Loop around each element in the main heading list
for t in headSet:
    newDat = ''
    curNme = f'out/preobservations-{i}.csv-metadata.trig'    #### Current file name
    newNme = f'out/observations-{i}.csv-metadata.trig'       #### New file name
    #### Open the file and loop around each line adding or deleting as you go
    with open(curNme, "r") as input:
        #### Also open the new file to add to as you go
        with open(newNme, "w") as output: 
            #### Loop around the input file
            for line in input:
                #### Change the lines to the value in the variabl headMain
                if headMain in line.strip("\n"):
                    newLine = line
                    newLine = line.replace(headMain, headMain + ' - ' + t)
                    output.write(newLine)
                else: 
                    lineWanted = True
                    #### Ignore lines with ns2 but loop for other ns# lines, deleteing any extra ones that do not match the value of k
                    if '@prefix ns2:' not in line.strip("\n"):
                        if '@prefix ns' in line.strip("\n"):
                            if f'@prefix ns{k}:' not in line.strip("\n"):
                                #### You do not want this line so ignore
                                lineWanted = False
                    #### If the line is needed check if it is a line that needs changing then write to new file 
                    if lineWanted: 
                        if 'a pmd:Dataset' in line.strip("\n"):
                            line = line.replace(f'observations-{i}/', f'observations-{i}')
                    
                        if 'pmd:graph' in line.strip("\n"):
                            line = line.replace(f'observations-{i}/', f'observations-{i}')
                        #### Output the line to the new file                    
                        output.write(line)
                        
    #### Close both files
    input.close
    output.close
    #### Old trig file no longer needed so remove/delete
    os.remove(curNme)

    #### Increment i, ns2 is used for something else so you have got to jump k up by 1 at this point
    i = i + 1
    if i == 2:
        k = k + 2
    else:
        k = k + 1
