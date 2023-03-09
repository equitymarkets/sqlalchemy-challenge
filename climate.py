#!/usr/bin/env python
# coding: utf-8

# In[210]:


get_ipython().run_cell_magic('javascript', '', 'IPython.OutputArea.prototype._should_scroll = function(lines) {\n    return false;\n}')


# In[211]:


get_ipython().run_line_magic('matplotlib', 'inline')
from matplotlib import style
style.use('fivethirtyeight')
import matplotlib.pyplot as plt


# In[212]:


import numpy as np
import pandas as pd
import datetime as dt
from datetime import datetime, timedelta 


# # Reflect Tables into SQLAlchemy ORM

# In[213]:


# Python SQL toolkit and Object Relational Mapper
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect, types


# In[214]:


# create engine to hawaii.sqlite
engine = create_engine("sqlite:///Resources/hawaii.sqlite")


# In[215]:


# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(autoload_with=engine)


# In[216]:


# View all of the classes that automap found
Base.classes.keys()


# In[217]:


# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station


# In[218]:


# Create our session (link) from Python to the DB
session = Session(engine)
session


# # Exploratory Precipitation Analysis

# In[219]:


most_recent = datetime.strptime(session.query(func.max(Measurement.date))    .scalar(), '%Y-%m-%d').date()
print(most_recent)


# In[220]:


earliest = datetime.strptime(session.query(func.max(Measurement.date))    .scalar(), '%Y-%m-%d').date() - dt.timedelta(days=365)
print(earliest)


# In[221]:


import matplotlib.dates as mdates
# Design a query to retrieve the last 12 months of precipitation data and plot the results. 
# Starting from the most recent data point in the database. 


# Calculate the date one year from the last date in data set.

# Perform a query to retrieve the data and precipitation scores
year_precipitation = session.query(Measurement.date, Measurement.prcp)    .filter(Measurement.date >= datetime.strptime(session.query(func.max(Measurement.date))    .scalar(), '%Y-%m-%d').date() - dt.timedelta(days=365)).all()

# Save the query results as a Pandas DataFrame and set the index to the date column
data_plot_df = pd.DataFrame(year_precipitation, columns=['date', 'precipitation'])
data_plot_df.set_index('date', inplace = True)

# Sort the dataframe by date
data_plot_df = data_plot_df.sort_values('date')

# Use Pandas Plotting with Matplotlib to plot the data
ax = data_plot_df.plot(figsize=(10,6), x_compat=True)
plt.xticks(rotation = 90)
x_tick_set = [0, 250, 500, 750, 1000, 1250, 1500, 1750, 2000, 2250]
plt.xticks(x_tick_set)
plt.xlabel("Date")
plt.ylabel("Inches")

plt.show()

##################################################################minor=True


# In[222]:


# Use Pandas to calcualte the summary statistics for the precipitation data
data_plot_df.describe()


# # Exploratory Station Analysis

# In[223]:


# Design a query to calculate the total number stations in the dataset
total_stations = session.query(Measurement.station).distinct().count()

print(total_stations)


# In[224]:


# Design a query to find the most active stations (i.e. what stations have the most rows?)
# List the stations and the counts in descending order.
most_active_stations = sorted(session.query(Measurement.station, func.count(Measurement.station)).                         group_by(Measurement.station).all(), key = lambda x: x[1], reverse=True)

print(most_active_stations)


# In[225]:


most_active_station_id = most_active_stations[0][0]

print(most_active_station_id)


# In[226]:


lowest = session.query(Measurement.station).filter(Measurement.station == most_active_station_id).with_entities(func.min(Measurement.tobs)).all()[0][0]
highest = session.query(Measurement.station).filter(Measurement.station == most_active_station_id).with_entities(func.max(Measurement.tobs)).all()[0][0]
average = session.query(Measurement.station).filter(Measurement.station == most_active_station_id).with_entities(func.avg(Measurement.tobs)).all()[0][0]
print(f"The lowest temperature recorded was {lowest}. The highest temperature recorded was {highest}. The average temperature was {average}")


# In[227]:


# Using the most active station id
# Establish the bins 
# Query the last 12 months of temperature observation data for this station and plot the results as a histogram
year_temperature = session.query(Measurement.date, Measurement.tobs)    .filter(Measurement.date >= datetime.strptime(session.query(func.max(Measurement.date))    .scalar(), '%Y-%m-%d').date() - dt.timedelta(days=365))    .filter(Measurement.station == most_active_station_id).all()
temp_plot_df = pd.DataFrame(year_temperature, columns=['date', 'temperature'])
temp_plot_df.plot.hist(by=None, bins=12, figsize=(10,6))
plt.xlabel("Temperature")
plt.ylabel("Frequency")
plt.show()


# # Close session

# In[228]:


# Close Session
session.close()

