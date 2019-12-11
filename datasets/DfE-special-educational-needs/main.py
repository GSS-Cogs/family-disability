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

next_table = next_table[next_table['ONS Geography'] != '.']

new_table['Period'] = pd.to_numeric(new_table['Period'], errors='coerce').fillna(0)
new_table['Period'] = new_table['Period'].astype('Int64')
next_table['Period'] = 'year/'+ next_table['Period'].astype(str)

next_table['Dfe-Age'] = next_table['Dfe-Age'].str.replace('\.0', '')
next_table['Dfe-Age'] = ('year/') + next_table['Dfe-Age']
next_table['Dfe-Age'] = next_table['Dfe-Age'].map(
    lambda x: {
        'year/All' : 'all', 'year/2 and under' : 'under-2', 
       'year/12 and above': '12-plus', 'year/Total All Ages' :'all', 'year/4 and under' :'under-4',
       'year/19+' : '19-plus', 'year/all' : 'all'
        }.get(x, x))

next_table['Dfe-Sex'] = next_table['Dfe-Sex'].map(
    lambda x: { 'All' : 'T', 'Boys' :'B', 'Girls' :'G', 'Total' : 'T', 'Total(5)' :'T', 'all' :'T'        
        }.get(x, x))

next_table['Special Education Provider'] = next_table['Special Education Provider'].apply(pathify)

next_table['Special Education Need Type'] = next_table['Special Education Need Type'].str.rstrip('()24569')
next_table['Special Education Need Type'] = next_table['Special Education Need Type'].apply(pathify)
next_table['Special Education Need Type'] = next_table['Special Education Need Type'].map(
    lambda x: {  'other-difficulty/disability' : 'other-difficulty-or-disability',
               'speech-language-and-communications-needs' : 'speech-language-and-communications-need'
        }.get(x, x))

next_table['Special Education Support Type'] = next_table['Special Education Support Type'].str.rstrip('()57')
next_table['Special Education Support Type'] = next_table['Special Education Support Type'].str.replace('\.0', '')
next_table['Special Education Support Type'] = next_table['Special Education Support Type'].apply(pathify)

next_table['Special Education Support Type'] = next_table['Special Education Support Type'].map(
    lambda x: {  'gypsy-/-roma' : 'gypsy-or-roma', 
                 'other-difficulty/disability' : 'other-difficulty-or-disability',
                'sen-support-by-ethnic-group-gypsy-/-roma' : 'sen-support-by-ethnic-group-gypsy-or-roma',
                'statements-or-ehc-plans-support-by-ethnic-group-gypsy-/-roma' : 'statements-or-ehc-plans-support-by-ethnic-group-gypsy-or-roma',
               'pupils-on-sen-support-secondary-other-difficulty/disability' : 'pupils-on-sen-support-secondary-other-difficulty-or-disability',
               'pupils-with-statements-or-ehc-plans-secondary-other-difficulty/disability' : 'pupils-with-statements-or-ehc-plans-secondary-other-difficulty-or-disability',
                'pupils-on-sen-supporteligible-and-claiming-free-school-meals' : 'pupils-on-sen-support-eligible-and-claiming-free-school-meals',       
        }.get(x, x))

from pathlib import Path
out = Path('out')
out.mkdir(exist_ok=True)
next_table.drop_duplicates().to_csv(out / 'observations.csv', index = False)

scraper.dataset.family = 'disability'
with open(out / 'observations.csv-metadata.trig', 'wb') as metadata:
    metadata.write(scraper.generate_trig())

csvw = CSVWMetadata('https://gss-cogs.github.io/family-disability/reference/')
csvw.create(out / 'observations.csv', out / 'observations.csv-schema.json')
