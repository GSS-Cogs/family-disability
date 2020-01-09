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
# %run "T22.py"
next_table = pd.concat([next_table, new_table])
# %run "T23.py"
next_table = pd.concat([next_table, new_table])
# %run "T24.py"
next_table = pd.concat([next_table, new_table])
# %run "T25.py"
next_table = pd.concat([next_table, new_table])
# %run "T26.py"
next_table = pd.concat([next_table, new_table])
# %run "T28.py"
next_table = pd.concat([next_table, new_table])
# %run "T29.py"
next_table = pd.concat([next_table, new_table])
# %run "T30.py"
next_table = pd.concat([next_table, new_table])
# %run "T31.py"
next_table = pd.concat([next_table, new_table])
# %run "T32.py"
next_table = pd.concat([next_table, new_table])
# %run "T33.py"
next_table = pd.concat([next_table, new_table])
# %run "T34.py"
next_table = pd.concat([next_table, new_table])
# %run "T35.py"
next_table = pd.concat([next_table, new_table])
# %run "T36.py"
next_table = pd.concat([next_table, new_table])
# %run "T37.py"
next_table = pd.concat([next_table, new_table])
# %run "T38.py"
next_table = pd.concat([next_table, new_table])
# %run "T39.py"
next_table = pd.concat([next_table, new_table])
# %run "T40.py"
next_table = pd.concat([next_table, new_table])
# %run "T41.py"
next_table = pd.concat([next_table, new_table])
# %run "T42.py"
next_table = pd.concat([next_table, new_table])
# %run "T43.py"
next_table = pd.concat([next_table, new_table])
# %run "T44.py"
next_table = pd.concat([next_table, new_table])
# %run "T45.py"
next_table = pd.concat([next_table, new_table])
# %run "T46.py"
next_table = pd.concat([next_table, new_table])
# %run "T47.py"
next_table = pd.concat([next_table, new_table])
# %run "T48.py"
next_table = pd.concat([next_table, new_table])
# %run "T49.py"
next_table = pd.concat([next_table, new_table])
# %run "T50.py"
next_table = pd.concat([next_table, new_table])
# %run "T51.py"
next_table = pd.concat([next_table, new_table])
# %run "T52.py"
next_table = pd.concat([next_table, new_table])
# %run "T53.py"
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
