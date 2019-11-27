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
scraper = Scraper('https://www.gov.uk/government/statistics/special-educational-needs-in-england-january-2019')

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
# -

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
