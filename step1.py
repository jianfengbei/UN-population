#---United Nation Population Projection data

#step 1: importing population projection - 2020-2100

#-- population data: 2020-2100
#check directory
import os
#os.getcwd()
os.chdir('/Users/jianfengbei/Google Drive/2020 study/2020 Python codes/00 United Nation population data')

#download excel file
#pip install pandas
import pandas as pd
#data download from web before importing: https://population.un.org/wpp/Download/Files/2_Indicators%20(Probabilistic%20Projections)/UN_PPP2019_Output_PopTot.xlsx
pop_projection='UN_PPP2019_Output_PopTot.xlsx'

    #pre-import data0 to check data
import xlrd
data0=pd.ExcelFile(pop_projection)
data0.sheet_names
data0=data0.parse('Median')
       #show all the columns - setting
pd.set_option('display.max_columns',None)
print(data0)
print(data0.head(20)) # find out that the first 15 rows were all NaN. 

   #import data set using a simplier coding: 
df2100=pd.read_excel(pop_projection, sheet_name='Median', skiprows=16, header=0, index_col=None)

#clean data
df2100.head() #check dataframe
df2100.isnull() #check NaN
df2100.isnull().sum()

       #check all variables' unique values
unique={}
for col_name in df2100.columns:
    unique_name=df2100[col_name].unique()
    unique[col_name]=unique_name
for keys in unique.keys():
    print(keys,':',unique[keys])
       # drop useless columns:'Index', 'Variant', 'Notes','Unnamed: 6'
df2100.drop(['Index','Variant','Notes','Unnamed: 6'],axis='columns',inplace=True)
df2100.head()

       #show all the rows - setting
pd.set_option('display.max_rows',None)

       # seperate region, subregion data from country or area:
region2100=df2100[df2100.Type!='Country/Area']
region2100=region2100[region2100[2100]!='...']
#region2100.drop('Region, subregion, country or area',axis='columns',inplace=True)
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

       #change column names:'Region, subregion, country or area', 'Unnamed: 4' 
country2100.columns
country2100.columns=['country_name', 'country_code', 2020, 2025, 2030, 2035, 2040, 2045, 2050, 2055, 2060, 2065, 2070, 2075, 2080, 2085, 2090, 2095, 2100]
country2100.head()

       #reset index
country2100=country2100.reset_index(drop=True)
country2100.head()


#check data type
    #for country2100
country2100.dtypes  #check data type
       #check all variables' unique values
unique={}
for col_name in country2100.columns:
    unique_name=country2100[col_name].unique()
    unique[col_name]=unique_name
for keys in unique.keys():
    print(keys,':',unique[keys])
       #convert all other columns to float
column=country2100.columns[2:]
for name in column:
    country2100[name]=country2100[name].astype('float')
country2100.dtypes

    #for region2100
region2100.dtypes
unique={}
for col_name in region2100.columns:
    unique_name=region2100[col_name].unique()
    unique[col_name]=unique_name
for keys in unique.keys():
    print(keys,':',unique[keys])
       #convert all other columns to float
column=region2100.columns[3:]
for name in column:
    region2100[name]=region2100[name].astype('float')
region2100.dtypes

#save files
country2100.to_csv('country2100.csv')
region2100.to_csv('region2100.csv')

#EDA analysis on country2100: 
      #check histogram: 
import matplotlib.pyplot as plt
country2100=pd.read_csv('country2100.csv',index_col=0)
plt.hist(country2100[2020],bins=30)
plt.show()

#majority of the countries have population size below 200 million.
      #check percentile: 
import numpy as np
p25={}
p75={}
column=country2100.columns[2:]

for year in column:
    p25[year]=np.percentile(country2100[year],25)
    p75[year]=np.percentile(country2100[year],75)
     #convert Dictionary to a Pandas Series
pd.Series(p25)
pd.Series(p75)
     # or convert Dictionary to a Pandas dataframe
percentile={'p25':p25,'p75':p75}
percentile=pd.DataFrame(percentile)
percentile.mean()
    #p25_mean~=500; p75_mean~=30000

     # calculate countries in fixed population range: 
below_500={}
between={}
above_30000={}
for year in column:
    below_500[year]=np.sum(country2100[year]<500)
    above_30000[year]=np.sum(country2100[year]>=30000)
    between[year]=235-below_500[year]-above_30000[year]

country_count={'below 500':below_500,'between 500 and 30,000':between,'above 30,000':above_30000}
country_count=pd.DataFrame(country_count)

     # what are the countries having 'below 500' in 2020 and 2100, respectively: 

country2100['below_2020']=country2100[2020]<500
country2100['below_2100']=country2100[2100]<500
country_below=country2100.loc[:,['country_name',2020,2100,'below_2020','below_2100']]
#country_below.drop('below',axis='columns',inplace=True)
country_below['false']=(country_below['below_2020']==0) & (country_below['below_2100']==0)
country_below['below_below']=(country_below['below_2020']==1) & (country_below['below_2100']==1)
country_below['below_above']=(country_below['below_2020']==1) & (country_below['below_2100']==0)
country_below['above_below']=(country_below['below_2020']==0) & (country_below['below_2100']==1)

country_below[country_below['below_below']==1].loc[:,['country_name',2020,2100]]
country_below[country_below['below_above']==1].loc[:,['country_name',2020,2100]]
country_below[country_below['above_below']==1].loc[:,['country_name',2020,2100]]

#conclusion 1: majority of the coutnries having populations below 500K in 2020 will remain small population size in 2100. 
#conclusion 2: two countries' population falling into 'below 500K' in 2100 have less than 100K decrease: Maldives, Montenegro
#conclusion 3: five countries' poulation jumping out of 'below 500K' in 2100 will double or triple their population size:
               #Mayotte,Sao Tome and Principe,Belize,French Guiana,Vanuatu

#below is practice: 
    # calculate back the number of countries below, between, and above
def count_entries(df,col_name):
    """"return a dictionary with counts of occurrences as value for each key."""
    country_count={}
    col=df[col_name]
    for entry in col:
        if entry in country_count.keys():
            country_count[entry]+=1
        else:
            country_count[entry]=1
    return country_count

count_entries(country_below,'below_2020')
count_entries(country_below,'below_2100')

#plotting the two decreasing countries
country2100=country2100.iloc[:,:-3]
import matplotlib.pyplot as plt
year=country2100.columns[2:].astype('float')

country2100[country2100['country_name']=='Maldives'] #checkf index
country2100[country2100['country_name']=='Montenegro']

drop_countries=country2100.iloc[[86,214],:]
drop_countries=drop_countries.set_index('country_name')
drop_countries.drop('country_code',axis='columns',inplace=True)

plt.plot(year, drop_countries.iloc[0],linestyle='--')
plt.plot(year, drop_countries.iloc[1],linestyle='--')

plt.xlabel('year')
plt.ylabel('predicted population')
plt.legend(drop_countries.index)
plt.show()

#plotting the five increasing countries:Mayotte,Sao Tome and Principe,Belize,French Guiana,Vanuatu
country2100[country2100['country_name']=='Mayotte'] #checkf index
country2100[country2100['country_name']=='Sao Tome and Principe']
country2100[country2100['country_name']=='Belize']
country2100[country2100['country_name']=='French Guiana']
country2100[country2100['country_name']=='Vanuatu']

increase_countries=country2100.iloc[[9,28,137,152,165],:]
increase_countries=increase_countries.set_index('country_name')
increase_countries.drop('country_code',axis='columns',inplace=True)

for index in range(len(increase_countries)):
    plt.plot(year, increase_countries.iloc[index],linestyle='--')
plt.xlabel('year')
plt.ylabel('predicted population')
plt.legend(increase_countries.index)
plt.show()

## plotting regional plots
***


##animate plots: 
《next level course》

