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
scraper = Scraper('https://www.gov.uk/government/collections/statistics-special-educational-needs-sen')
scraper.select_dataset(title=lambda x: x.startswith('Special educational needs in England'), latest=True)

next_table = pd.DataFrame()

# +
# %%capture

# %run "Table 1.py"
next_table = pd.concat([next_table, new_table])
# %run "Table 2a.py"
next_table = pd.concat([next_table, new_table])
# %run "Table 2b.py"
next_table = pd.concat([next_table, new_table])
# %run "Table 3.py"
next_table = pd.concat([next_table, new_table])
# %run "Table 4.py"
next_table = pd.concat([next_table, new_table])
# %run "Table 5.py"
next_table = pd.concat([next_table, new_table])
# %run "Table 6.py"
next_table = pd.concat([next_table, new_table])
# %run "Table 7.py"
next_table = pd.concat([next_table, new_table])
# %run "Table 8.py"
next_table = pd.concat([next_table, new_table])
# %run "Table 9.py"
next_table = pd.concat([next_table, new_table])
# %run "Table 10.py"
next_table = pd.concat([next_table, new_table])
# %run "Table 11.py"
next_table = pd.concat([next_table, new_table])
# %run "Table 12.py"
next_table = pd.concat([next_table, new_table])
# %run "Table 13.py"
next_table = pd.concat([next_table, new_table])
# %run "Table 14.py"
next_table = pd.concat([next_table, new_table])
# %run "Table 15.py"
next_table = pd.concat([next_table, new_table])
# %run "Table 16.py"
next_table = pd.concat([next_table, new_table])
# %run "Table 17.py"
next_table = pd.concat([next_table, new_table])
# %run "Table 18.py"
next_table = pd.concat([next_table, new_table])
# %run "Table 19.py"
next_table = pd.concat([next_table, new_table])
# %run "Table A.py"
next_table = pd.concat([next_table, new_table])
# %run "Table B.py"
next_table = pd.concat([next_table, new_table])
# %run "Table C1.py"
next_table = pd.concat([next_table, new_table])
# %run "Table C2.py"
next_table = pd.concat([next_table, new_table])
# %run "Table D.py"
next_table = pd.concat([next_table, new_table])
# %run "Table E.py"
next_table = pd.concat([next_table, new_table])
# %run "Table F.py"
next_table = pd.concat([next_table, new_table])
# %run "Table G.py"
next_table = pd.concat([next_table, new_table])
# -

next_table.rename(columns={'Geography': 'ONS Geography',
                             'Age' : 'Dfe-Age',
                             'Sex' : 'Dfe-Sex',
                             'Special support type' : 'Special Education Support Type',
                             'Special need type' : 'Special Education Need Type',
                             'Education provider' : 'Special Education Provider'
                              }, inplace=True)

from pathlib import Path
out = Path('out')
out.mkdir(exist_ok=True)
next_table.drop_duplicates().to_csv(out / 'observations.csv', index = False)

scraper.dataset.family = 'health'
scraper.dataset.theme = THEME['health-social-care']
with open(out / 'dataset.trig', 'wb') as metadata:
    metadata.write(scraper.generate_trig())

csvw = CSVWMetadata('https://gss-cogs.github.io/family-disability/reference/')
csvw.create(out / 'observations.csv', out / 'observations.csv-schema.json')

next_table.tail()


