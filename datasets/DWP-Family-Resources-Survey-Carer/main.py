# +
#### Family Resources Survey for Financial Year 2017 to 2018 - Carer ####

# +
from gssutils import *
import datetime as d
import numpy as np

#### Construct a string based on the year you need to look at.
oneYrAgo = int(d.datetime.now().year) - 1        #### Get the year 1 year ago
twoYrAgo = oneYrAgo - 1                          #### Get the year 2 years ago
yrStr = str(twoYrAgo) + str(oneYrAgo)[2:4]       #### Join the years as a string, 201718
yrStr2 = str(twoYrAgo) + '/' + str(oneYrAgo)[2:4] #### This is for adding to columns later
try:
    #### EXAMPLE: https://www.gov.uk/government/statistics/family-resources-survey-#### Construct a string based on the year you need to look at.
    oneYrAgo = int(d.datetime.now().year) - 1        #### Get the year 1 year ago
    twoYrAgo = oneYrAgo - 1                          #### Get the year 2 years ago
    yrStr = str(twoYrAgo) + str(oneYrAgo)[2:4]       #### Join the years as a string, 201718financial-year-201718
    urlStr = "https://www.gov.uk/government/statistics/family-resources-survey-financial-year-" + yrStr

    scraper = Scraper(urlStr)
except Exception as e:
    print(e.message, e.args)

scraper


# +
# Table 5.1: Percentage of people providing informal care by gender, 2007/08 to 2017/18, United Kingdom
# Table 5.2: Percentage of people providing informal care by age & gender, 2007/08 to 2017/18, United Kingdom
# Table 5.8: Percentage of people receiving care by age and gender, 2017,18, United Kingdom
# -

def extract_sheet_5_1_and_5_2_and_5_8(tab, mainCol, whichTab):
    try:
        st = '9'    # Start Row
        ed = '22'   # End RowgHeading = 'Sex'
        gHeading = 'Sex'
        # Set up the data for All
        col = tab.excel_ref('B' + st).fill(DOWN).is_not_blank() - tab.excel_ref('B' + ed).expand(DOWN).is_not_blank()
        All = tab.excel_ref('C' + st).fill(DOWN).is_not_blank() - tab.excel_ref('C' + ed).expand(DOWN).is_not_blank()
        ss1 = tab.excel_ref('D' + st).fill(DOWN).is_not_blank() - tab.excel_ref('D' + ed).expand(DOWN).is_not_blank()
        # Set the dimensions
        Dimensions = [
            HDim(col,mainCol, DIRECTLY, LEFT),
            HDim(ss1,'Sample Size', CLOSEST, ABOVE),
            HDimConst(gHeading,'All'),
            HDimConst('Unit','%')
            ]
        c1 = ConversionSegment(All, Dimensions, processTIMEUNIT=True)
        c1 = c1.topandas()
        # Set up the data for Males
        Males = tab.excel_ref('E' + st).fill(DOWN).is_not_blank() - tab.excel_ref('E' + ed).expand(DOWN).is_not_blank()
        ss2 = tab.excel_ref('F' + st).fill(DOWN).is_not_blank() - tab.excel_ref('F' + ed).expand(DOWN).is_not_blank()
        # Set the dimensions
        Dimensions = [
            HDim(col,mainCol, DIRECTLY, LEFT),
            HDim(ss2,'Sample Size', CLOSEST, ABOVE),
            HDimConst(gHeading,'Male'),
            HDimConst('Unit','%')
            ]
        c2 = ConversionSegment(Males, Dimensions, processTIMEUNIT=True)        
        c2 = c2.topandas()
        # Set up the data for Females
        Females = tab.excel_ref('G' + st).fill(DOWN).is_not_blank() - tab.excel_ref('G' + ed).expand(DOWN).is_not_blank()
        ss3 = tab.excel_ref('H' + st).fill(DOWN).is_not_blank() - tab.excel_ref('H' + ed).expand(DOWN).is_not_blank()
        # Set the dimensions
        Dimensions = [
            HDim(col,mainCol, DIRECTLY, LEFT),
            HDim(ss3,'Sample Size', CLOSEST, ABOVE),
            HDimConst(gHeading,'Female'),
            HDimConst('Unit','%')
            ]
        c3 = ConversionSegment(Females, Dimensions, processTIMEUNIT=True)       
        c3 = c3.topandas()
        # Join up the 3 tables
        tbl = pd.concat([c1, c2, c3])
        tbl.columns.values[0] = 'Value'
        
        # Set some extra columns
        if whichTab == 1:
            tbl['Age'] = 'All'
        elif whichTab == 2: 
            tbl['Year'] = yrStr2
        elif whichTab == 8:
            tbl['Year'] = yrStr2
            
        # make some changes to match standars for codelists
        tbl[gHeading][tbl[gHeading] == 'Male'] = 'M'
        tbl[gHeading][tbl[gHeading] == 'Female'] = 'F'
        tbl[gHeading][tbl[gHeading] == 'All'] = 'T'
        tbl['Age'][tbl['Age'] == 'All providing care'] = 'All'
        tbl['Age'][tbl['Age'] == 'All people receiving care'] = 'All'
    
        # Select the columns to return    
        tbl = tbl[['Year','Age',gHeading,'Sample Size','Value','Unit']]
        tbl = tbl.rename(columns={'Year':'Period'})
        return tbl
    except Exception as e:
        return "Error for table 5_1 or 5_2 or 5_8: " + str(e)


# +
# Table 5.3: Adult informal carers by gender, age and number of hours per week providing care, 2017/18, United Kingdom
# Table 5.6: Adult informal care by gender, age and net individual weekly income, 2017/18, United Kingdom
# -

def extract_sheet_5_3_and_5_6(tab, whichTbl):
    try:
        if whichTbl == 3: 
            rw = 10
        elif whichTbl == 6: 
            rw = 9
        gHeading = 'Sex'   
        col1 = tab.excel_ref('B' + str(rw)).fill(DOWN).is_not_blank()
        col2 = tab.excel_ref('C' + str(rw)).fill(DOWN).expand(RIGHT).is_not_blank()
        col3 = tab.excel_ref('C' + str(rw - 1)).expand(RIGHT).is_not_blank()
        # Create the table and convert to Pandas
        Dimensions = [
            HDim(col1,'Age', DIRECTLY, LEFT),
            HDim(col3,'Hours per Week', CLOSEST, LEFT),
            HDimConst('Unit','%'),
            HDimConst(gHeading,'All'),
            HDimConst('Year',yrStr2)
            ]
        tbl = ConversionSegment(col2, Dimensions, processTIMEUNIT=True)
        tbl = tbl.topandas()
        # Need to find where the Female and Male carer data starts and ends. Find it and then set Gender values
        mSt = tbl.loc[tbl['Age'].str.contains('male', na=False, regex=True)].index[0]    # Find where the Male data starts
        fSt = tbl.loc[tbl['Age'].str.contains('female', na=False, regex=True)].index[0]  # Find where the Female data starts
        aEd = tbl['Age'].count()                                                         # Get the total number of rows
        tbl[gHeading][mSt:fSt] = 'Male'
        tbl[gHeading][fSt:aEd] = 'Female'

        tbl = tbl[tbl['Hours per Week'] != 'All'] # Get rid of the 100% rows, can't see the point
        tblSS = tbl[tbl['Hours per Week'].str.contains('Sample', na=False, regex=True)] # Identify the Sample Size rows to join in with the data laterz
        tbl = tbl[~tbl['Hours per Week'].str.contains('Sample', na=False, regex=True)] # Remove the Sample Size Rows from the main dataset
        tbl = pd.merge(tbl, tblSS, on=['Age', gHeading])
        if whichTbl == 3:
            tbl = tbl.rename(columns={'OBS_x':'Value','Hours per Week_x':'Hours per Week','Unit_x':'Unit','OBS_y':'Sample Size', 'Year_x':'Year'})
            tbl = tbl[['Year', 'Age', 'Hours per Week', gHeading, 'Sample Size', 'Value', 'Unit']]
        elif whichTbl == 6:
            tbl = tbl.rename(columns={'OBS_x':'Value','Hours per Week_x':'Net Weekly Income','Unit_x':'Unit','OBS_y':'Sample Size', 'Year_x':'Year'})
            tbl = tbl[['Year', 'Age', 'Net Weekly Income', gHeading, 'Sample Size', 'Value', 'Unit']]
        tbl = tbl.rename(columns={'Year':'Period'})
        # make some changes to match standars for codelists
        tbl[gHeading][tbl[gHeading] == 'Male'] = 'M'
        tbl[gHeading][tbl[gHeading] == 'Female'] = 'F'
        tbl[gHeading][tbl[gHeading] == 'All'] = 'T'
        tbl['Age'][tbl['Age'].str.contains('carers')] = 'All'
        return tbl
    except Exception as e:
        return "Error for table 5_3 or 5_6: " + str(e)


# +
# Table 5.4: Adult informal carers by employment status and gender, 2017/18, United Kingdom
# Table 5.7: Who informal carers care for by gender, 2017/18, United Kingdom
# -

def extract_sheet_5_4_and_5_7(tab, whichTbl):
    try:
        if whichTbl == 4: 
            rw = 9
            col1 = tab.excel_ref('B' + str(rw)).fill(DOWN).is_not_blank()
            col2 = tab.excel_ref('C' + str(rw)).fill(DOWN).expand(RIGHT).is_not_blank()

        elif whichTbl == 7: 
            rw = 10
            rwEnd = 36
            col1 = tab.excel_ref('B' + str(rw)).fill(DOWN).is_not_blank() - tab.excel_ref('B' + str(rwEnd)).expand(DOWN).is_not_blank()
            col2 = tab.excel_ref("C10:E36").is_not_blank() #### Some formulas in cells next to the dataset, font has also been changed to white! specified a range instead
            
        col3 = tab.excel_ref('C' + str(rw - 1)).expand(RIGHT).is_not_blank()
        gHeading = 'Sex'   
        # Create the table and convert to Pandas
        heading = 'Employment Status'
        Dimensions = [
            HDimConst('Year',yrStr2),
            HDim(col1,heading, DIRECTLY, LEFT),
            HDim(col3,gHeading, CLOSEST, LEFT),
            HDimConst('Unit','%')
            ]
        tbl = ConversionSegment(col2, Dimensions, processTIMEUNIT=True)
        tbl = tbl.topandas()
        if whichTbl == 4:
            
            subHeading = 'Employment Type'
            tbl[subHeading] = tbl[heading]    # Create new column to hold the sub employment status
            #### Sort out the All Employment Sub Category
            mSt = tbl.loc[tbl[heading].str.contains('employment', na=False, regex=True)].index    # 
            fSt = tbl.loc[tbl[heading].str.contains('employees', na=False, regex=True)].index[0]     # 
            tbl[heading][mSt[0]:fSt] = 'In Employment'
            tbl[subHeading][mSt] = 'All'
            #### Sort out the All Employees Sub Category
            mSt = tbl.loc[tbl[heading].str.contains('employees', na=False, regex=True)].index    # 
            fSt = tbl.loc[tbl[heading].str.contains('self', na=False, regex=True)].index[0]         # 
            tbl[heading][mSt[0]:fSt] = 'Employees'
            tbl[subHeading][mSt] = 'All'
            #### Sort out the All Self-Employed Sub Category
            mSt = tbl.loc[tbl[heading].str.contains('self', na=False, regex=True)].index    # 
            fSt = tbl.loc[tbl[heading].str.contains('Unemployed', na=False, regex=True)].index[0]         # 
            tbl[heading][mSt[0]:fSt] = 'Self-Employed'
            tbl[subHeading][mSt] = 'All'
            #### Sort out the All Unemployed & Retired Sub Category
            tbl[subHeading][tbl[subHeading] == 'Unemployed'] = 'All'
            tbl[subHeading][tbl[subHeading] == 'Retired'] = 'All'
            ### Sort out the All Economically Inactive Sub Category
            mSt = tbl.loc[tbl[heading].str.contains('economically', na=False, regex=True)].index    # 
            fSt = tbl.loc[tbl[heading] == 'All'].index[0]    #
            tbl[heading][mSt[0]:fSt] = 'Economically Inactive'
            tbl[subHeading][mSt] = 'All'

            #### Sort out the Gender sub category
            gsubHeading = 'Adult Carers'
            tbl[gsubHeading] = 'All Adults'
            mSt = tbl.loc[tbl[gHeading].str.contains('carers', na=False, regex=True)].index    # 
            tbl[gsubHeading][mSt + 0] = 'Adult Informal Carers'
            tbl[gsubHeading][mSt + 1] = 'Adult Informal Carers'
            tbl[gsubHeading][mSt + 2] = 'Adult Informal Carers'
            tbl[gHeading][mSt] = 'All'
            tbl[gHeading][tbl[gHeading].str.strip() == 'All adults'] = 'All'

            tbl = tbl[tbl[heading] != 'All'] # Get rid of the 100% rows, can't see the point
            tblSS = tbl[tbl[heading].str.contains('Sample')] # Identify the Sample Size rows to join in with the data laterz
            tbl = tbl[~tbl[heading].str.contains('Sample')] # Remove the Sample Size Rows from the main dataset
            tbl = pd.merge(tbl, tblSS, on=[gHeading, gsubHeading])
            #### Rename Columns
            tbl = tbl.rename(columns={'OBS_x':'Value','Year_x':'Year','Unit_x':'Unit', heading + '_x':heading, subHeading + '_x':subHeading, 'OBS_y':'Sample Size'})
            tbl = tbl[['Year', heading, subHeading, gHeading, gsubHeading, 'Sample Size', 'Value', 'Unit']]
            
        elif whichTbl == 7:
            
            heading = 'Person cared for Type'
            subHeading = 'Person cared for'
            tbl = tbl.rename(columns={'Employment Status':heading})
            tbl[subHeading] = tbl[heading]
            #### Sort out the Household Member Sub Category
            mSt = tbl.loc[tbl[heading].str.contains('Household member', na=False, regex=True)].index    # 
            fSt = tbl.loc[tbl[heading].str.contains('Non-household member', na=False, regex=True)].index[0]     # 
            tbl[heading][mSt[0]:fSt] = 'Household Member'
            tbl[subHeading][mSt] = 'All'
            #### Sort out the Non-Household Member Sub Category
            mSt = tbl.loc[tbl[heading].str.contains('Non-household member', na=False, regex=True)].index    # 
            fSt = tbl.loc[tbl[heading].str.contains('More than 1 person cared for', na=False, regex=True)].index[0]     # 
            tbl[heading][mSt[0]:fSt] = 'Non-Household Member'
            tbl[subHeading][mSt] = 'All'
            #### Sort out the More than 1 person cared for Sub Category
            mSt = tbl.loc[tbl[heading].str.contains('More than 1 person cared for', na=False, regex=True)].index    # 
            fSt = tbl.loc[tbl[heading].str.contains('Sample size', na=False, regex=True)].index[0]     # 
            tbl[heading][mSt[0]:fSt] = 'More than 1 person cared for'
            tbl[subHeading][mSt] = 'All'
            
            tbl = tbl[tbl[heading] != 'All'] # Get rid of the 100% rows, can't see the point
            tblSS = tbl[tbl[heading].str.contains('Sample')] # Identify the Sample Size rows to join in with the data laterz
            tbl = tbl[~tbl[heading].str.contains('Sample')] # Remove the Sample Size Rows from the main dataset
            tbl = pd.merge(tbl, tblSS, on=[gHeading])
            #### Rename Columns
            tbl = tbl.rename(columns={'OBS_x':'Value','Year_x':'Year','Unit_x':'Unit', heading + '_x':heading, subHeading + '_x':subHeading, 'OBS_y':'Sample Size'})
            tbl = tbl[['Year', heading, subHeading, gHeading, 'Sample Size', 'Value', 'Unit']]
            
            tbl[subHeading][tbl[subHeading].str.contains('Friend')] = 'Non-Relative ' + tbl[subHeading][tbl[subHeading].str.contains('Friend')]
            tbl[subHeading][tbl[subHeading].str.contains('Client')] = 'Non-Relative ' + tbl[subHeading][tbl[subHeading].str.contains('Client')]
            tbl[subHeading][tbl[subHeading] == 'Other'] = 'Non-Relative ' + tbl[subHeading][tbl[subHeading] == 'Other']
            tbl = tbl[~tbl[heading].str.contains('Non-relative')]
            
        tbl = tbl.rename(columns={'Year':'Period'})
        return tbl
    except Exception as e:
        "Error for table 5_4 or 5_7: " + str(e) 


# +
# Table 5.5: Adult informal carers by main source of total weekly household income hours caring and gender, 2017/18, United Kingdom
# -

def extract_sheet_5_5(tab):
    try:
        tab = [t for t in sheets if t.name == '5_5'][0]
        col1 = tab.excel_ref('B8').fill(DOWN).is_not_blank()
        col2 = tab.excel_ref('C8').fill(DOWN).expand(RIGHT).is_not_blank()
        col3 = tab.excel_ref('C7').expand(RIGHT).is_not_blank()
        # Create the table and convert to Pandas
        heading = 'Source of Income'
        headingHrs = 'Hours per Week'
        headingG = 'Sex'
        Dimensions = [
            HDimConst('Year',yrStr2),
            HDim(col1,heading, DIRECTLY, LEFT),
            HDim(col3,headingHrs, CLOSEST, LEFT),
            HDimConst('Unit','%')
            ]
        tbl = ConversionSegment(col2, Dimensions, processTIMEUNIT=True)
        tbl = tbl.topandas()

        tbl[headingG] = 'All'
        tbl[headingG][(tbl[headingHrs] == 'Males') | (tbl[headingHrs] == 'Females')] = tbl[headingHrs]
        tbl[headingHrs][(tbl[headingHrs] == 'Males') | (tbl[headingHrs] == 'Females')] = 'All'

        tbl = tbl[tbl[heading] != 'All'] # Get rid of the 100% rows, can't see the point
        tblSS = tbl[tbl[heading].str.contains('Sample')] # Identify the Sample Size rows to join in with the data laterz
        tbl = tbl[~tbl[heading].str.contains('Sample')] # Remove the Sample Size Rows from the main dataset
        tbl = pd.merge(tbl, tblSS, on=[headingHrs, headingG])
        tbl[headingHrs][(tbl[headingHrs] == 'All adult carers')] = 'All'

        #### Rename Columns
        tbl = tbl.rename(columns={'OBS_x':'Value','Year_x':'Year','Unit_x':'Unit', heading + '_x':heading, headingHrs + '_x':headingHrs, 'OBS_y':'Sample Size'})
        tbl = tbl[['Year', heading, headingHrs, headingG, 'Sample Size', 'Value', 'Unit']]
        # Rename the Gender items to match standards
        tbl[headingG][tbl[headingG] == 'Male'] = 'M'
        tbl[headingG][tbl[headingG] == 'Female'] = 'F'
        tbl[headingG][tbl[headingG] == 'All'] = 'T'
        # Rename the items with a notes number attached
        tbl[heading][tbl[heading] == 'State Pension plus any IS/PC1,2'] = 'State Pension plus any IS/PC'
        tbl[heading][tbl[heading] == 'Non-state pensions3'] = 'Non-state pensions'
        tbl[heading][tbl[heading] == 'Disability benefits4'] = 'Disability benefits'
        tbl[heading][tbl[heading] == 'Other benefits5,6'] = 'Other benefits'
    
        tbl = tbl.rename(columns={'Year':'Period'})
        return tbl
    except Exception as e:
        "Error for table 5_5: " + str(e) 


# +
# Table 5.9: People receiving care at least once a week by age and frequency of care, 2017/18, United Kingdom
# -

def extract_sheet_5_9(tab):
    try:
        rw = 10
        heading = 'Frequency of care'
        
        col1 = tab.excel_ref('B' + str(rw)).fill(DOWN).is_not_blank()
        col2 = tab.excel_ref('C' + str(rw)).fill(DOWN).expand(RIGHT).is_not_blank()
        col3 = tab.excel_ref('C' + str(rw - 1)).expand(RIGHT).is_not_blank()
        # Create the table and convert to Pandas
        Dimensions = [
            HDim(col1,'Age', DIRECTLY, LEFT),
            HDim(col3,heading, CLOSEST, LEFT),
            HDimConst('Unit','%'),
            HDimConst('Year',yrStr2)
            ]
        tbl = ConversionSegment(col2, Dimensions, processTIMEUNIT=True)
        tbl = tbl.topandas()
        
        tbl = tbl[tbl[heading] != 'All'] # Get rid of the 100% rows, can't see the point
        tblSS = tbl[tbl[heading].str.contains('Sample')] # Identify the Sample Size rows to join in with the data laterz
        tbl = tbl[~tbl[heading].str.contains('Sample')] # Remove the Sample Size Rows from the main dataset
        tbl = pd.merge(tbl, tblSS, on=['Age'])
        #### Rename Columns
        tbl = tbl.rename(columns={'OBS_x':'Value', 'Year_x':'Year','Unit_x':'Unit', heading + '_x':heading, 'OBS_y':'Sample Size'})
        tbl = tbl[['Year', 'Age', heading, 'Sample Size', 'Value', 'Unit']]
        tbl['Age'][tbl['Age'] == 'All receiving care'] = 'All'
        tbl = tbl.rename(columns={'Year':'Period'})
        return tbl
    except Exception as e:
        err = pd.DataFrame(e.message, columns = ['Error']) 
        return err


# +
# Table 5.10: People receiving care by main source of total weekly household income and gender, 2017/18, United Kingdom
# -

def extract_sheet_5_10(tab):
    try:                
        rw = 9
        col1 = tab.excel_ref('B' + str(rw)).fill(DOWN).is_not_blank()
        col2 = tab.excel_ref('C' + str(rw)).fill(DOWN).expand(RIGHT).is_not_blank()    
        col3 = tab.excel_ref('C' + str(rw - 1)).expand(RIGHT).is_not_blank()
        col4 = tab.excel_ref('C' + str(rw - 2)).expand(RIGHT).is_not_blank()
        heading = 'Source of Income'
        # Create the table and convert to Pandas
        headingG = 'Sex'
        Dimensions = [
            HDimConst('Year',yrStr2),
            HDim(col1,heading, DIRECTLY, LEFT),
            HDim(col3,headingG, CLOSEST, LEFT),
            HDim(col4,'People', CLOSEST, LEFT),
            HDimConst('Unit','%')
            ]
        tbl = ConversionSegment(col2, Dimensions, processTIMEUNIT=True)
        tbl = tbl.topandas()
        
        tbl = tbl[tbl[heading] != 'All'] # Get rid of the 100% rows, can't see the point
        tblSS = tbl[tbl[heading].str.contains('Sample')] # Identify the Sample Size rows to join in with the data laterz
        tbl = tbl[~tbl[heading].str.contains('Sample')] # Remove the Sample Size Rows from the main dataset
        tbl = pd.merge(tbl, tblSS, on=[headingG, 'People'])
        #### Rename Columns
        tbl = tbl.rename(columns={'OBS_x':'Value','Year_x':'Year','Unit_x':'Unit', heading + '_x':heading, 'People_x':'People', 'OBS_y':'Sample Size'})
        tbl = tbl[['Year', heading, 'People', headingG, 'Sample Size', 'Value', 'Unit']]
        # Rename the Gender items to match standards
        tbl[headingG][tbl[headingG] == 'Male'] = 'M'
        tbl[headingG][tbl[headingG] == 'Female'] = 'F'
        tbl[headingG][tbl[headingG] == 'All'] = 'T'
        # Rename the items with a notes number attached
        tbl[heading][tbl[heading] == 'State Pension plus any IS/PC2,3'] = 'State Pension plus any IS/PC'
        tbl[heading][tbl[heading] == 'Non-state pensions4'] = 'Non-state pensions'
        tbl[heading][tbl[heading] == 'Disability benefits5'] = 'Disability benefits'
        tbl[heading][tbl[heading] == 'Other benefits6,7'] = 'Other benefits'
        tbl['People'] = tbl['People'].str.strip()
        tbl = tbl.rename(columns={'Year':'Period'})
        return tbl
    except Exception as e:
        return "Error for table 5_10: " + str(e)


#### There are several spreadsheets so look for the one you want, which in this case is Carers only
try:
    for i in scraper.distributions:
        if i.title == 'Carers data tables (XLS)':
            print(i.title)
            sheets = i
            break
except Exception as e:
         print(e.message, e.args)

#### Convert to a DataBaker object
try:
    sheets = sheets.as_databaker()
except Exception as e:
    print(e.message, e.args)

try:
    tbl1 = extract_sheet_5_1_and_5_2_and_5_8([t for t in sheets if t.name == '5_1'][0], 'Year', 1)
    tbl2 = extract_sheet_5_1_and_5_2_and_5_8([t for t in sheets if t.name == '5_2'][0], 'Age', 2)
    tbl3 = extract_sheet_5_3_and_5_6([t for t in sheets if t.name == '5_3'][0], 3)
    tbl4 = extract_sheet_5_4_and_5_7([t for t in sheets if t.name == '5_4'][0], 4)
    tbl5 = extract_sheet_5_5([t for t in sheets if t.name == '5_5'][0])
    tbl6 = extract_sheet_5_3_and_5_6([t for t in sheets if t.name == '5_6'][0], 6)
    tbl7 = extract_sheet_5_4_and_5_7([t for t in sheets if t.name == '5_7'][0], 7)
    tbl8 = extract_sheet_5_1_and_5_2_and_5_8([t for t in sheets if t.name == '5_8'][0], 'Age', 8)
    tbl9 = extract_sheet_5_9([t for t in sheets if t.name == '5_9'][0])
    tbl10 = extract_sheet_5_10([t for t in sheets if t.name == '5_10'][0])
except Exception as e:
    print(e.message, e.args)
#tbl4

# +
#### Set up the folder path for the output files
from pathlib import Path

out = Path('out')
out.mkdir(exist_ok=True, parents=True)
# -

#### Output the files
tbl1.drop_duplicates().to_csv(out / ('observations_5_1.csv'), index = False)
tbl2.drop_duplicates().to_csv(out / ('observations_5_2.csv'), index = False)
tbl3.drop_duplicates().to_csv(out / ('observations_5_3.csv'), index = False)
tbl4.drop_duplicates().to_csv(out / ('observations_5_4.csv'), index = False)
tbl5.drop_duplicates().to_csv(out / ('observations_5_5.csv'), index = False)
tbl6.drop_duplicates().to_csv(out / ('observations_5_6.csv'), index = False)
tbl7.drop_duplicates().to_csv(out / ('observations_5_7.csv'), index = False)
tbl8.drop_duplicates().to_csv(out / ('observations_5_8.csv'), index = False)
tbl9.drop_duplicates().to_csv(out / ('observations_5_9.csv'), index = False)
tbl10.drop_duplicates().to_csv(out / ('observations_5_10.csv'), index = False)

# +
scraper.dataset.family = 'disability'
#scraper.dataset.license = 'http://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/'

with open(out / 'dataset.trig', 'wb') as metadata:
    metadata.write(scraper.generate_trig())
# -

csvw = CSVWMetadata('https://gss-cogs.github.io/family-disability/reference/')
#schema = CSVWMetadata('https://github.com/GSS-Cogs/family-disability/reference/')
csvw.create(out / 'observations_5_1.csv', out / 'observations_5_1.csv-schema.json')
csvw.create(out / 'observations_5_2.csv', out / 'observations_5_2.csv-schema.json')
csvw.create(out / 'observations_5_3.csv', out / 'observations_5_3.csv-schema.json')
csvw.create(out / 'observations_5_4.csv', out / 'observations_5_4.csv-schema.json')
csvw.create(out / 'observations_5_5.csv', out / 'observations_5_5.csv-schema.json')
csvw.create(out / 'observations_5_6.csv', out / 'observations_5_6.csv-schema.json')
csvw.create(out / 'observations_5_7.csv', out / 'observations_5_7.csv-schema.json')
csvw.create(out / 'observations_5_8.csv', out / 'observations_5_8.csv-schema.json')
csvw.create(out / 'observations_5_9.csv', out / 'observations_5_9.csv-schema.json')
csvw.create(out / 'observations_5_10.csv', out / 'observations_5_10.csv-schema.json')


