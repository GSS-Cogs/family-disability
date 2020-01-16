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


# table 33:  Mean earnings by responsibility level, government department and gender (All Employees)

tabs = {tab.name: tab for tab in scraper.distribution(latest=True).as_databaker()}
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
#savepreviewhtml(observations)

dimensions = [
    HDimConst('Measure Type', 'mean-earnings'),
    HDimConst('Year', '2018'),
    HDimConst('ONS Age Range', 'all'),
    HDimConst('Region name', 'all'),
    HDimConst('Nationality', 'all'),
    HDimConst('Salary Band', 'all'),
    HDimConst('Ethnicity', 'all'),
    HDimConst('Disability Status', 'not-applicable'),
    HDimConst('Profession of Post', 'not-applicable'),
    HDimConst('Entrants or Leavers', 'not-applicable'),
    HDimConst('Type of Employment', 'all-employees'),
    HDimConst('Status of Employment', 'not-applicable'),
    HDimConst('NUTS Area Code', 'not-applicable'),
    HDimConst('ONS area code', 'not-applicable'),
    HDim(gender, 'Sex', DIRECTLY, ABOVE),
    HDim(responsibility_level, 'Responsibility Level', CLOSEST, LEFT), 
    HDim(department, 'Department', DIRECTLY, LEFT),
]
c1 = ConversionSegment(observations, dimensions, processTIMEUNIT=True)
new_table = c1.topandas() 

new_table.rename(columns={'OBS': 'Value'}, inplace=True)
if 'DATAMARKER' in new_table.columns:
    print('marker found in columns')
    new_table['DATAMARKER'].replace('..', 'between-one-and-five', inplace=True)
    new_table['DATAMARKER'].replace('-', 'not-applicable', inplace=True)
    new_table = new_table.rename(columns={'DATAMARKER':'Marker'})
    new_table = new_table.fillna('not-applicable') 
else:
    print('marker not found in colmns making it')
    new_table['DATAMARKER'] = 'not-applicable'
    new_table = new_table.rename(columns={'DATAMARKER':'Marker'})

# +
#///////////////////////////////////
out = Path('output')
out.mkdir(exist_ok=True, parents=True)

def createCodeListforColumn(dta,colNme):
    try:
        titles =('Label','Notation','Parent Notation','Sort Priority')
        cdeLst = dta.unique()
        cdeLst = pd.DataFrame(cdeLst)
        #### Create a version of the column name with lowercase and spaces replaced with underscore(_)
        colNmeP = colNme.replace(' ','-').replace('_','-').lower()
        #### Create the standard codelist and output
        cdeLst.columns = [titles[0]]
        cdeLst[titles[1]] = cdeLst[titles[0]].apply(pathify)
        cdeLst[titles[1]] = cdeLst[titles[1]].str.replace('/', '-', regex=True)
        cdeLst[titles[2]] = ''
        cdeLst[titles[3]] = cdeLst.reset_index().index + 1
        #### Output the file
        cdeLst.to_csv(out / f'{colNmeP}.csv', index = False)
        return cdeLst
    except Exception as e:
        return "createCodeListforColumn: " + str(e)

createCodeListforColumn(new_table['Department'],'Department33')
# -

new_table['Department'] = new_table['Department'].map(lambda x: pathify(x))
new_table['Responsibility Level'] = new_table['Responsibility Level'].map(lambda x: pathify(x))
new_table['Sex'] = new_table['Sex'].map(lambda x: pathify(x))
new_table = new_table.replace({'Sex' : {'male19' : 'M','female19' : 'F','total' : 'T' }})
new_table
