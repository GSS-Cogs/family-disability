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
# %run "table1.py"
next_table = pd.concat([next_table, new_table])
# %run "table2.py"
next_table = pd.concat([next_table, new_table])
# %run "table3.py"
next_table = pd.concat([next_table, new_table])
# %run "table4.py"
next_table = pd.concat([next_table, new_table])
# %run "table5.py"
next_table = pd.concat([next_table, new_table])
# %run "table6.py"
next_table = pd.concat([next_table, new_table])

# #%run "table7.py" TO DO - LOOK AT AGAIN 
#next_table = pd.concat([next_table, new_table])

# %run "table8.py"
next_table = pd.concat([next_table, new_table])
# %run "table9.py"
next_table = pd.concat([next_table, new_table])
# %run "table10.py"
next_table = pd.concat([next_table, new_table])
# %run "table11.py"
next_table = pd.concat([next_table, new_table])
# -

# # %%capture
#
# #Statistical Bulletin Tables
# # %run "table1.py"
# next_table = pd.concat([next_table, new_table])
# # %run "table2.py"
# next_table = pd.concat([next_table, new_table])
# # %run "table3.py"
# next_table = pd.concat([next_table, new_table])
# # %run "table4.py"
# next_table = pd.concat([next_table, new_table])
# # %run "table5.py"
# next_table = pd.concat([next_table, new_table])
# # %run "table6.py"
# next_table = pd.concat([next_table, new_table])
#
# # #%run "table7.py" TO DO - LOOK AT AGAIN 
# #next_table = pd.concat([next_table, new_table])
#
# # %run "table8.py"
# next_table = pd.concat([next_table, new_table])
# # %run "table9.py"
# next_table = pd.concat([next_table, new_table])
# # %run "table10.py"
# next_table = pd.concat([next_table, new_table])
# # %run "table11.py"
# next_table = pd.concat([next_table, new_table])
#
# #Regional
# # %run "table12.py"
# next_table = pd.concat([next_table, new_table])
# # %run "table13.py"
# next_table = pd.concat([next_table, new_table])
# # %run "table14.py"
# next_table = pd.concat([next_table, new_table])
# # %run "table15.py"
# next_table = pd.concat([next_table, new_table])
# # %run "table16.py"
# next_table = pd.concat([next_table, new_table])
# # %run "table17.py"
# next_table = pd.concat([next_table, new_table])
# # %run "table18.py"
# next_table = pd.concat([next_table, new_table])
# # %run "table19.py"
# next_table = pd.concat([next_table, new_table])
#
# #Responsibility Level
# # %run "table20.py"
# next_table = pd.concat([next_table, new_table])
# # %run "table21.py"
# next_table = pd.concat([next_table, new_table])
# # %run "table22.py"
# next_table = pd.concat([next_table, new_table])
# # %run "table23.py"
# next_table = pd.concat([next_table, new_table])
#
# #Earnings
# # %run "table25.py"
# next_table = pd.concat([next_table, new_table])
# # %run "table26.py"
# next_table = pd.concat([next_table, new_table])
# # %run "table27.py"
# next_table = pd.concat([next_table, new_table])
# # %run "table28.py"
# next_table = pd.concat([next_table, new_table])
# # %run "table29.py"
# next_table = pd.concat([next_table, new_table])
# # %run "table30.py"
# next_table = pd.concat([next_table, new_table])
# # %run "table32.py"
# next_table = pd.concat([next_table, new_table])
# # %run "table32.py"
# next_table = pd.concat([next_table, new_table])
# # %run "table33.py"
# next_table = pd.concat([next_table, new_table])
# # %run "table34.py"
# next_table = pd.concat([next_table, new_table])
#
# #Government Department
# # %run "table36.py"
# next_table = pd.concat([next_table, new_table])
# # %run "table37.py"
# next_table = pd.concat([next_table, new_table])
# # %run "table38.py"
# next_table = pd.concat([next_table, new_table])
# # %run "table39.py"
# next_table = pd.concat([next_table, new_table])
#
# #Entrants and Leavers
# # %run "table40.py"
# next_table = pd.concat([next_table, new_table])
# # %run "table41.py"
# next_table = pd.concat([next_table, new_table])
#

next_table['Responsibility Level'] = next_table['Responsibility Level'].map(lambda x: pathify(x))
next_table['Department'] = next_table['Department'].map(lambda x: pathify(x))
next_table['Sex'] = next_table['Sex'].map(lambda x: pathify(x))
next_table = next_table.replace({'Sex' : {'male' : 'M','female' : 'F','total' : 'T' }})
next_table['Disability Status'] = next_table['Disability Status'].map(lambda x: pathify(x))
next_table['Employment Type'] = next_table['Employment Type'].map(lambda x: pathify(x))
next_table['Employment Status'] = next_table['Employment Status'].map(lambda x: pathify(x))
next_table['Profession of Post'] = next_table['Profession of Post'].map(lambda x: pathify(x))
next_table['Nationality'] = next_table['Nationality'].map(lambda x: pathify(x))
next_table['Ethnicity'] = next_table['Ethnicity'].map(lambda x: pathify(x))
next_table['Entrants or Leavers'] = next_table['Entrants or Leavers'].map(lambda x: pathify(x))
next_table['Region name'] = next_table['Region name'].map(lambda x: pathify(x))
next_table['Measure Type'] = next_table['Measure Type'].map(lambda x: pathify(x))
next_table = next_table.fillna('not-applicable')
next_table = next_table [['Year', 'Disability Status', 'Responsibility Level', 'Department', 'ONS Age Range', 
                          'Sex', 'Employment Type', 'Employment Status', 'Salary Band', 'Profession of Post', 
                          'Nationality', 'Ethnicity', 'Entrants or Leavers', 'Region name', 'ONS area code', 
                          'NUTS Area Code', 'Value', 'Marker', 'Measure Type']]
next_table

# +
destinationFolder = Path('out')
destinationFolder.mkdir(exist_ok=True, parents=True)

TITLE = 'Civil Service Statistics (unvalidated)'
OBS_ID = pathify(TITLE)
GROUP_ID = 'ONS-Civil-Service-Statistics'

next_table.drop_duplicates().to_csv(destinationFolder / f'{OBS_ID}.csv', index = False)

# +
from gssutils.metadata import THEME
scraper.set_base_uri('http://gss-data.org.uk')
scraper.set_dataset_id(f'gss_data/disability/{GROUP_ID}/{OBS_ID}')
scraper.dataset.title = f'{TITLE}'
scraper.dataset.family = 'disability'

with open(destinationFolder / f'{OBS_ID}.csv-metadata.trig', 'wb') as metadata:
    metadata.write(scraper.generate_trig())

schema = CSVWMetadata('https://gss-cogs.github.io/family-disability/reference/')
schema.create(destinationFolder / f'{OBS_ID}.csv', destinationFolder / f'{OBS_ID}.csv-schema.json')
