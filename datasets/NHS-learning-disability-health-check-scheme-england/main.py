# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:light
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.4'
#       jupytext_version: 1.2.4
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

# +
#### NHS Learning Disability Health Check Scheme

# +
from gssutils import *
import numpy as np
import json

info = json.load(open('info.json'))
info['landingPage']
scraper = Scraper(info['landingPage'])
scraper.select_dataset(latest=True)
scraper
# -
dist = scraper.distribution(latest=True, mediaType='text/csv')
tbl = dist.as_pandas(encoding='Windows-1252')
tbl.drop(columns=['REGION_CODE','SUB_REGION_CODE','CCG_CODE','STP_CODE','DQ_FLAG'], inplace=True)
tbl.drop(columns=['REGION_NAME','STP _NAME','SUB_REGION_NAME','CCG_NAME','PRACTICE_NAME'], inplace=True)

out = Path('out')
out.mkdir(exist_ok=True, parents=True)


def createCodeListforColumn(dta,colNme):
    try:
        titles =('Label','Notation','Parent Notation','Priority')
        cdeLst = dta.unique()
        cdeLst = pd.DataFrame(cdeLst)
        
        #### Create a version of the column name with lowercase and spaces replaced with underscore(_)
        colNmeP = colNme.replace(' ','-').replace('_','-').lower()
        
        #### Create the standard codelist and output
        cdeLst.columns = [titles[0]]
        cdeLst[titles[1]] = cdeLst[titles[0]].apply(pathify)
        cdeLst[titles[2]] = ''
        cdeLst[titles[3]] = cdeLst.reset_index().index + 1
        cdeLst[titles[1]] = cdeLst[titles[1]].str.replace('/', '-', regex=True)
        #### Output the file
        cdeLst.to_csv(out / f'{colNmeP}.csv', index = False)
        
        #### Create definition for the columns.csv file based on a dimension
        colTitles = ('title','name','component_attachment','property_template','value_template','datatype','value_transformation','regex','range')
        colOut = pd.DataFrame()
        colOut[colTitles[0]] = colNme,
        colOut[colTitles[1]] = colNmeP,
        colOut[colTitles[2]] = 'qb:dimension'
        colOut[colTitles[3]] = 'http://gss-data.org.uk/def/dimension/' + colNmeP
        colOut[colTitles[4]] = 'http://gss-data.org.uk/def/concept/' + colNmeP + '/{' + colNmeP.replace('-','_') + '}'
        colOut[colTitles[5]] = 'string'
        colOut[colTitles[6]] = 'slugize'
        colOut[colTitles[7]] = ''
        colOut[colTitles[8]] = 'http://gss-data.org.uk/def/classes/' + colNmeP + '/' + colNmeP.replace('-','_')
        #### Output the file
        colOut.to_csv(out / f'{colNmeP}__columnsCSV_Definition.csv', index = False)
        
        return colOut
    except Exception as e:
        return "createCodeListforColumn: " + str(e)


# +
#### Rename the column and create a codelist
meas = 'NHS LDHC Measure Code'
quse = 'NHS LDHC Quality Service'

tbl = tbl.rename(columns={'MEASURE':meas})
#t = createCodeListforColumn(tbl[meas],meas)

tbl = tbl.rename(columns={'QUALITY_SERVICE':quse})
#t = createCodeListforColumn(tbl[quse],quse)

#### Do more renaming of columns
tbl = tbl.rename(columns={'REGION_ONS_CODE':'ONS Geography'})
tbl = tbl.rename(columns={'SUB_REGION_ONS_CODE':'ONS SUB Geography'})
tbl = tbl.rename(columns={'CCG_ONS_CODE':'ONS CCG Geography'})
tbl = tbl.rename(columns={'PRACTICE_CODE':'Practice Code'})
tbl = tbl.rename(columns={'ACH_DATE':'Date'})
tbl = tbl.rename(columns={'VALUE':'Value'})

#### Check for NANs in the Value column
tbl['Value'][np.isnan(tbl['Value'])] = 0 

tbl.to_csv(out / 'observations.csv', index = False)
# -

tbl


