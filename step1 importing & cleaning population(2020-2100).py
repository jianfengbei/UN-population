import os
os.chdir('/Users/jianfengbei/Google Drive/2020 study/2020 Python codes/00 United Nation population data')

import pandas as pd
import numpy as np
#data download from web before importing: https://population.un.org/wpp/Download/Files/2_Indicators%20(Probabilistic%20Projections)/UN_PPP2019_Output_PopTot.xlsx
pop_projection='UN_PPP2019_Output_PopTot.xlsx'
df2100=pd.read_excel(pop_projection, sheet_name='Median', skiprows=16, header=0, index_col=None)

# drop useless columns:'Index', 'Variant', 'Notes','Unnamed: 6'
df2100.drop(['Index','Variant','Notes','Unnamed: 6'],axis='columns',inplace=True)

       #show all the columns - setting
pd.set_option('display.max_columns',None)

       #change column names:'Region, subregion, country or area', 'Unnamed: 4' 
df2100.columns
df2100.columns=['country_name', 'country_code', 'Type', 2020, 2025, 2030, 2035, 2040, 2045, 2050, 2055, 2060, 2065, 2070, 2075, 2080, 2085, 2090, 2095, 2100]
df2100.head()

       #add continent variable
continent_dict={947: 'Africa', 922: 'Asia', 1830: 'Latin America and the Caribbean', 927: 'Oceania', 917: 'Europe', 918: 'Northern America'}
df2100['continent']=''
for code,country in continent_dict.items():
    df2100.iloc[df2100[df2100['country_code'] == code].index[0], -1]=country

       # seperate region, subregion data from country or area:
region2100=df2100[df2100.Type!='Country/Area']
region2100=region2100[region2100[2100]!='...']
region2100.drop('continent',axis='columns',inplace=True)
region2100.columns
region2100.columns=['region_name', 'region_code', 'Type', 2020, 2025, 2030, 2035, 2040, 2045, 2050, 2055, 2060, 2065, 2070, 2075, 2080, 2085, 2090, 2095, 2100]
             #reset index
region2100=region2100.reset_index(drop=True)
region2100.head()

       #for df2100: keep only if 'Type'=='Country/Area'
country2100=df2100[df2100.Type=='Country/Area']
country2100.Type.unique() 
country2100.drop('Type',axis='columns',inplace=True)
country2100.head()
       #reset index
country2100=country2100.reset_index(drop=True)
country2100.head()

       #move 'continent' column to after 'country_name'
country2100=country2100[['country_name', 'country_code', 'continent', 2020, 2025, 2030, 2035, 2040, 2045, 2050, 2055, 2060, 2065, 2070, 2075, 2080, 2085, 2090, 2095, 2100]]

       #cleaning data types
column=country2100.columns[2:-2]
for name in column:
    country2100[name]=country2100[name].astype('float')
country2100.dtypes

column=region2100.columns[3:]
for name in column:
    region2100[name]=region2100[name].astype('float')
region2100.dtypes

       #save files
country2100.to_csv('country2100.csv')
region2100.to_csv('region2100.csv')
