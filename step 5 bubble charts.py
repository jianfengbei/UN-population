#check directory
import os
#os.getcwd()
os.chdir('/Users/jianfengbei/Google Drive/2020 study/2020 Python codes/00 United Nation population data')

import pandas as pd
import numpy as np
import plotly.offline as py
import plotly.graph_objs as go
import plotly.express as px
from plotly.figure_factory import create_table

#import data
gapminder = pd.read_csv('df1950_2100.csv',index_col=0)
gapminder.columns
gapminder.columns=['country_name', 'year', 'life_expectancy', 'gdp', 'continent', 'population']

       #show all the columns - setting
pd.set_option('display.max_columns',None)

gapminder.sort_values(['country_name','continent','year'],inplace=True)


#bubble charts: 
fig=px.scatter(gapminder,x='gdp', y='life_expectancy',color='continent',
           size='population',size_max=60,hover_name='country_name',animation_frame='year',
           animation_group='country_name',log_x=True, range_x=[40,100000],range_y=[25,90],
           labels=dict(population='Population',gdp='GDP per Capita', life_expectancy='Life Expectancy'))
fig.show()

