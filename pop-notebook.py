#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
#import matplotlib.pyplot as plt
#%matplotlib inline
import geopandas as gpd
from bokeh.io import show, output_notebook
from bokeh.plotting import figure
from bokeh.palettes import viridis
from bokeh.models import ColumnDataSource, FactorRange, Legend
from bokeh.models.tools import HoverTool
import json
from bokeh.io import show
from bokeh.models import (CDSView, ColorBar, ColumnDataSource,CustomJS, CustomJSFilter, GeoJSONDataSource, HoverTool,LinearColorMapper, Slider)
from bokeh.layouts import column, row, widgetbox
from bokeh.palettes import brewer
from bokeh.plotting import figure
# set up output file as first thing
#output_notebook()
from bokeh.io.doc import curdoc
from bokeh.layouts import widgetbox, row, column

#matplotlib style options
#plt.style.use('ggplot')
#plt.rcParams['figure.figsize'] = (15, 5)
#plt.style.use('ggplot')
#plt.rcParams['figure.figsize'] = (15, 5)


# In[2]:


#load data
df_demo = pd.read_csv("Demographic_Data.csv")

#Finding the population for each state
State_pop = df_demo.groupby('State')['TotalPop'].sum()

#Merging the population to df4
df_demo = df_demo.merge(State_pop, on=['State'], how='left')

#Finding the population ratio for each county
df_demo['Pop_ratio']=df_demo['TotalPop_x']/df_demo['TotalPop_y']

#Removing the total state population
df_demo = df_demo.drop(['TotalPop_y'], axis=1)


# In[3]:


#Defining the columns that needs to be normalized with state ratio
ratio_columns = ['Hispanic','White', 'Black', 'Native', 'Asian', 'Pacific',
       'Income', 'Poverty', 'ChildPoverty', 'Professional', 'Service', 'Office', 'Construction',
       'Production', 'Drive', 'Carpool', 'Transit', 'Walk', 'OtherTransp',
       'WorkAtHome', 'MeanCommute', 'Employed', 'PrivateWork', 'PublicWork',
       'SelfEmployed', 'FamilyWork', 'Unemployment']

#Normalizing the columns
df5=pd.DataFrame(df_demo['State'])
for column in df_demo[ratio_columns]:
    df5[column] = df_demo[column]*df_demo['Pop_ratio']

#merging the normalized columns with df4
df_demo = df_demo[['TotalPop_x','Men','Women']]
df_demo = pd.concat([df_demo, df5], axis=1)

#finding all info for each state
df_demo = df_demo.groupby('State').sum()


# In[4]:


#Resets index 
df_demo = df_demo.reset_index()
#drop alaska, hawaii and puerto rico in order to have a better visualization
df_demo = df_demo.loc[~df_demo.State.isin(['Alaska', 'Hawaii', 'Puerto Rico'])]
#Resets index 
df_demo = df_demo.reset_index(drop=True)


# In[5]:


#Men and Women distribution for each state
df_demo['Men_p'] = df_demo.Men/(df_demo.Men+df_demo.Women)
df_demo['Women_p'] = df_demo.Women/(df_demo.Men+df_demo.Women)


# In[6]:


#Make dataframes for bar plots
Income_bar = df_demo[['State','Income']].sort_values(by=['Income'],ascending=False)
Poverty_bar = df_demo[['State','Poverty']].sort_values(by=['Poverty'],ascending=False)
Unemployment_bar = df_demo[['State','Unemployment']].sort_values(by=['Unemployment'],ascending=False)
TotalPop_bar = df_demo[['State','TotalPop_x']].sort_values(by=['TotalPop_x'],ascending=False)


# In[7]:


# Read in shapefile and examine data
contiguous_usa = gpd.read_file('cb_2018_us_state_20m/cb_2018_us_state_20m.shp')
#sort the values based on state name
contiguous_usa = contiguous_usa.sort_values(by=['NAME'])
#Rename the state column
contiguous_usa.rename(columns = {'NAME':'State'}, inplace = True)    


# In[8]:


#merging the demographic data with the shapefile data                          
df_demo = contiguous_usa.merge(df_demo, on=['State'], how='left')
df_demo = df_demo.loc[~df_demo['State'].isin(['Alaska', 'Hawaii','Puerto Rico'])]


# In[9]:


#Input GeoJSON source that contains features for plotting
geosource = GeoJSONDataSource(geojson = df_demo.to_json())


# In[11]:


# Define color palettes
palette = brewer['BuGn'][8]
palette = palette[::-1] # reverse order of colors so higher values have darker colors
# Instantiate LinearColorMapper that linearly maps numbers in a range, into a sequence of colors.
color_mapper = LinearColorMapper(palette = palette, low = df_demo.TotalPop_x.min(), high = df_demo.TotalPop_x.max())

# Create figure object.
p = figure(title = 'Demographic Data (colored after population)', 
           plot_height = 600 ,
           plot_width = 950, 
           toolbar_location = 'below',
           tools = "pan, wheel_zoom, box_zoom, reset")
p.xgrid.grid_line_color = None
p.ygrid.grid_line_color = None
# Add patch renderer to figure.
states = p.patches('xs','ys', source = geosource,
                   fill_color = {'field' :'TotalPop_x',
                                 'transform' : color_mapper},
                   line_color = 'gray', 
                   line_width = 0.25, 
                   fill_alpha = 1)

# Create hover tool
p.add_tools(HoverTool(renderers = [states],
                      tooltips = [('State','@State'),
                                  ('Average Income','$@Income{0.00 a}'),
                                  ('Poverty','@Poverty%'),
                                  ('Unemployment','@Unemployment%'),
                                  ('Population','@TotalPop_x{0.00 a}'),
                                  ('Gender','Men(@Men_p%),  Women(@Women_p%)'),
                                  ('Race','Hispanic(@Hispanic%),  White(@White%)'),
                                  ('','Black(@Black%),  Native(@Native%)'),
                                  ('','Asian(@Asian%),  Pacific(@Pacific%)'),]))
#layout = column(p)
curdoc().clear()
curdoc().add_root(p)


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




