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
scraper = Scraper('https://digital.nhs.uk/data-and-information/publications/statistical/adult-social-care-activity-and-finance-report')
scraper.select_dataset(latest=True)

# Joining of Adult Social Care activity and finance tables to next table

next_table = pd.DataFrame()

# +
# %%capture

# %run "T1.py"
next_table = pd.concat([next_table, new_table])
# %run "T2.py"
next_table = pd.concat([next_table, new_table])
# %run "T3.py"
next_table = pd.concat([next_table, new_table])
# %run "T4.py"
next_table = pd.concat([next_table, new_table])
# %run "T5.py"
next_table = pd.concat([next_table, new_table])
# %run "T6.py"
next_table = pd.concat([next_table, new_table])
# %run "T7.py"
next_table = pd.concat([next_table, new_table])
# %run "T8.py"
next_table = pd.concat([next_table, new_table])
# %run "T9.py"
next_table = pd.concat([next_table, new_table])
# %run "T10.py"
next_table = pd.concat([next_table, new_table])
# %run "T11.py"
next_table = pd.concat([next_table, new_table])
# %run "T12.py"
next_table = pd.concat([next_table, new_table])
# %run "T13.py"
next_table = pd.concat([next_table, new_table])
# %run "T14.py"
next_table = pd.concat([next_table, new_table])
# %run "T15.py"
next_table = pd.concat([next_table, new_table])
# %run "T16.py"
next_table = pd.concat([next_table, new_table])
# %run "T17.py"
next_table = pd.concat([next_table, new_table])
# %run "T18.py"
next_table = pd.concat([next_table, new_table])
# %run "T19.py"
next_table = pd.concat([next_table, new_table])
# %run "T20.py"
next_table = pd.concat([next_table, new_table])
# -

from pathlib import Path
out = Path('out')
out.mkdir(exist_ok=True)
next_table.drop_duplicates().to_csv(out / 'observations.csv', index = False)

scraper.dataset.family = 'disability'
with open(out / 'observations.csv-metadata.trig', 'wb') as metadata:
    metadata.write(scraper.generate_trig())

csvw = CSVWMetadata('https://gss-cogs.github.io/family-disability/reference/')
csvw.create(out / 'observations.csv', out / 'observations.csv-schema.json')
