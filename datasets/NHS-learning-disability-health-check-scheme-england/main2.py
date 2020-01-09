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


def createDimensionColumnsCSVDefinition(colNme):
    try:
        #### Create a version of the column name with lowercase and spaces replaced with underscore(_)
        colNmeP = colNme.replace(' ','-').replace('_','-').lower()
        
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
        cdeLst[titles[1]] = cdeLst[titles[1]].str.replace('/', '-', regex=True)
        cdeLst[titles[2]] = ''
        cdeLst[titles[3]] = cdeLst.reset_index().index + 1
        #### Output the file
        cdeLst.to_csv(out / f'{colNmeP}.csv', index = False)
        
        return cdeLst
    except Exception as e:
        return "createCodeListforColumn: " + str(e)


#### Create new names for columns
meas = 'NHS LDHC Measure Code'
quse = 'NHS LDHC Quality Service'


# +
#### Rename the column and create a codelist

#### Remove rows that only consist of Unallocated as values
tbl = tbl[tbl['REGION_ONS_CODE'] != 'Unallocated']

tbl = tbl.rename(columns={'MEASURE':meas})
#t = createCodeListforColumn(tbl[meas],meas)
#t = createDimensionColumnsCSVDefinition(meas)

tbl = tbl.rename(columns={'QUALITY_SERVICE':quse})
#t = createCodeListforColumn(tbl[quse],quse)
#t = createDimensionColumnsCSVDefinition(quse)

#### Do more renaming of columns
tbl = tbl.rename(columns={'REGION_ONS_CODE':'ONS Geography'})
tbl = tbl.rename(columns={'SUB_REGION_ONS_CODE':'ONS Sub Geography'})
tbl = tbl.rename(columns={'CCG_ONS_CODE':'ONS CCG Geography'})
tbl = tbl.rename(columns={'PRACTICE_CODE':'GP Practice Code'})
tbl = tbl.rename(columns={'ACH_DATE':'Period'})
tbl = tbl.rename(columns={'VALUE':'Value'})
tbl = tbl.rename(columns={'PRACTICE_CODE':'GP Practice Code'})

#### Create a codelist for GP Practices
#t = createCodeListforColumn(tbl['GP Practice Code'],'GP Practice Code')
#t = createDimensionColumnsCSVDefinition('GP Practice Code')

#### Check for NANs in the Value column
tbl['Value'][np.isnan(tbl['Value'])] = 0 

#### Reformat the Date
tbl['Period'] = pd.to_datetime(tbl['Period'])
tbl['Period'] = 'day/' + tbl['Period'].apply(lambda x: x.strftime('%Y-%m-%d'))

#### Pathifying things
tbl['NHS LDHC Quality Service'] = tbl['NHS LDHC Quality Service'].apply(pathify)
#tbl['ONS Geography'] = tbl['ONS Geography'].apply(pathify)
#tbl['ONS SUB Geography'] = tbl['ONS SUB Geography'].apply(pathify)
#tbl['ONS CCG Geography'] = tbl['ONS CCG Geography'].apply(pathify)
#tbl['GP Practice Code'] = tbl['GP Practice Code'].apply(pathify)
tbl['NHS LDHC Measure Code'] = tbl['NHS LDHC Measure Code'].apply(pathify)

tbl['Measure Type'] = 'Count'

#### Due to PMD not currently being able to cope with multiple refArea columns i am removing
#### the 2 higher geography codes and keeping the lowest one, ONS CCG Geography, This is the NHS Trust
tbl.drop(columns=['ONS Geography','ONS Sub Geography'])
# -

tbl

# +
tbl.drop_duplicates().to_csv(out / 'observations.csv', index = False)

scraper.dataset.family = 'disability'

with open(out / 'preobservations.csv-metadata.trig', 'wb') as metadata:
    metadata.write(scraper.generate_trig())

csvw = CSVWMetadata('https://gss-cogs.github.io/family-disability/reference/')
csvw.create(out / 'observations.csv', out / 'observations.csv-schema.json')


# -
def createASetOfCodelistsForDataFrame(mainDat, paramDat):
    try:
        
        return 'Codelists Created'
    except Exception as e:
        return "createASetOfCodelistsForDataFrame: " + str(e)


# +
#### Create a DataFrame with all the column names
cols = pd.DataFrame(list(tbl))
#### Create a list of column names to use
colNmes = ['ColumnNames','CodeList','TypeDefinition']
#### This holds the Column Names
cols.columns = ['ColumnNames']
#### Add a Column to hold a Y or N value to define if a CodeList is needed
cols[colNmes[1]] = ''
cols[colNmes[1]][0] = 'Y'
cols[colNmes[1]][1] = 'N'
cols[colNmes[1]][2] = 'N'
cols[colNmes[1]][3] = 'N'
cols[colNmes[1]][4] = 'Y'
cols[colNmes[1]][5] = 'N'
cols[colNmes[1]][6] = 'Y'
cols[colNmes[1]][7] = 'N'
cols[colNmes[1]][8] = 'N'
#### Create a Column to define what type a Column it is, Dimension (D), Attribute (A), Measure (M) etc.
cols[colNmes[2]] = ''
cols[colNmes[2]][0] = 'D'
cols[colNmes[2]][1] = 'D'
cols[colNmes[2]][2] = 'D'
cols[colNmes[2]][3] = 'D'
cols[colNmes[2]][4] = 'D'
cols[colNmes[2]][5] = 'D'
cols[colNmes[2]][6] = 'D'
cols[colNmes[2]][7] = 'M'
cols[colNmes[2]][8] = 'D'

cde = createASetOfCodelistsForDataFrame(tbl, cols)
                                  
cols
# -

tbl


# +
#### As each trig file is created multiple @prefix ns lines are added. This code gets rid of them
import os

hed = '[MI] Learning Disabilities Health Check Scheme, England, Quarter 2, 2019-20"@en'
curNme = f'out/preobservations.csv-metadata.trig'    #### Current file name
newNme = f'out/observations.csv-metadata.trig'       #### New file name
#### Open the file and loop around each line adding or deleting as you go
with open(curNme, "r") as input:
    #### Also open the new file to add to as you go
     with open(newNme, "w") as output: 
        #### Loop around the input file
        for line in input:
            if '[MI]' in line.strip("\n"):
                line = line.replace('[', '')
                line = line.replace(']', '')
                line = line.replace(',', '')
        
            output.write(line)
                        
#### Close both files
input.close
output.close
#### Old trig file no longer needed so remove/delete
os.remove(curNme)


# -


