# %%
import random
from citipy import citipy
import numpy as np 
import pandas as pd 
import matplotlib.pyplot as plt 

import requests
from config import weather_api_key
from datetime import datetime
import time
from scipy.stats import linregress
# %%
# generate 1500 random latitude and longitude data as a list of tuples
lats = np.random.uniform(-90.0,90.0,size=1500)
lngs = np.random.uniform(-180.0,180.0,size=1500)

lats_lngs = zip(lats, lngs)
coordinates = list(lats_lngs)
print(coordinates[:11])

# %%
# use citipy module to get nearest city names
cities = list()
for coor in coordinates:
    cities_name = citipy.nearest_city(coor[0], coor[1]).city_name
    # ensure no any duplicate cities
    if cities_name not in cities:
        cities.append(cities_name)
print(cities[:10], 'Generate', len(cities))

# %%
# use OpenWeather API to request, get, parse JSON to retrieve weather data for each city.

# initial counters for log and sets
record_count = 1 
set_count = 1

city_data = list()
basic_url = "http://api.openweathermap.org/data/2.5/weather?units=imperial&APPID=" + weather_api_key

print('Beginning Data Retrieval     ')
print("-----------------------------")

# use enumerate() method to loop index and item simutanously 
for i, item in enumerate(cities):
    if i % 50 == 0 and i != 0 :
        record_count = 1  # initialize at every beginning of set
        set_count +=1 # increment set count
    # build URL for API call
    url = basic_url + '&q=' + item
    # Log the URL, record, and set numbers and the city.
    print(f'Processing Record {record_count} of Set {set_count} | {item}')
    # increment record count
    record_count +=1

    try: 
        js = requests.get(url).json()
        city_name = item
        city_country = js['sys']['country']
        city_UTCdate = js['dt']
        city_date = datetime.utcfromtimestamp(city_UTCdate).strftime('%Y-%m-%d %H:%M:%S')
        city_lat = js['coord']['lat']
        city_lon = js['coord']['lon']
        city_max_temp = js['main']['temp_max']
        city_humidity = js['main']['humidity']
        city_cload = js['clouds']['all']
        city_wind_speed = js['wind']['speed']
        # append as a list of dictionaries
        city_data.append({'City':city_name, 'Coounty':city_country, 'Date':city_date, 
                        'Lat':city_lat, 'Lng': city_lon,'Max Temp':city_max_temp,
                        'Humidity':city_humidity,'Cloudiness': city_cload,'Wind Speed':city_wind_speed})
    except:
        print("City not found. Skipping...")
        pass

# Indicate that Data Loading is complete
print('-------------------------------')
print('Data Retrieval Complete        ')
print('-------------------------------')

print(len(city_data))

# %%
# convert the list of dictionaries into DataFrame, and export to .csv file

unmod_city_data_df = pd.DataFrame(city_data)
city_data_df = unmod_city_data_df.rename(columns={'Coounty': 'Country'})
city_data_df.head()
city_data_df.to_csv(path_or_buf='weather_data/cities.csv', index_label='City_ID')

# %%
# 4 scatter plots, showcase weather parameter changing by latitude
# extract relevant fields(columns) as Series
lats_Series = city_data_df['Lat']
max_temp_Series = city_data_df['Max Temp']
humidity_Series = city_data_df['Humidity']
cloud_Series = city_data_df['Cloudiness']
wind_speed_Series = city_data_df['Wind Speed']

#show today's datetime in fig label
today = time.strftime('%x')
# %%
# build the 1st scatter plot for lat vs. Max Temp.
fig = plt.figure()
plt.scatter(lats_Series,max_temp_Series, 
            alpha=0.8, edgecolors='k', linewidths=1,marker='o', label='Cities' )
plt.title(f"City Latitude vs. Max Temperature " + today)
plt.xlabel("Latitude")
plt.ylabel('Max Temperature (F)')
plt.grid()
plt.savefig('weather_data/Fig1.png')
plt.show()

# %%
# build the 2nd scatter plot for lat vs. Humidity.
fig = plt.figure()
plt.scatter(lats_Series,humidity_Series, 
            alpha=0.8, edgecolors='k', linewidths=1,marker='o', label='Cities' )
plt.title(f"City Latitude vs. Humidity " + today)
plt.xlabel("Latitude")
plt.ylabel('Humidity (%)')
plt.grid()
plt.savefig('weather_data/Fig2.png')
#plt.legend()
plt.show()

# %%
# build the 3rd scatter plot for lat vs. Cloudiness.
fig = plt.figure()
plt.scatter(lats_Series,cloud_Series, 
            alpha=0.8, edgecolors='k', linewidths=1,marker='o', label='Cities' )
plt.title(f"City Latitude vs. Cloudiness (%) " + today)
plt.xlabel("Latitude")
plt.ylabel('Cloudiness (%)')
plt.grid()
plt.savefig('weather_data/Fig3.png')
plt.show()


# %%
# build the 4th scatter plot for lat vs. Wind Speed.
fig = plt.figure()
plt.scatter(lats_Series,wind_speed_Series, 
            alpha=0.8, edgecolors='k', linewidths=1,marker='o', label='Cities' )
plt.title(f"City Latitude vs. Wind Speed " + today)
plt.xlabel("Latitude")
plt.ylabel('Wind Speed (mph)')
plt.grid()
plt.savefig('weather_data/Fig4.png')
plt.show()

# %% [markdown]
# create a funtion with 5 variables, returns a combine plot of regree line and scatter
# Main process: 
# 1. retrieve 5 stats info by linregress() method 
# 2. use slope and alpha to get regression equation
# 3. list comprehension method to get each Y_expected value(in reg line) based by x_value
# 4. draw plot and scatter in same figure
# %%
def plot_linear_function(x_values, y_values,title, y_label, text_coordinates):
    (slope, intercept, r_value, p_value, std_err) = linregress(x_values,y_values)
    #step 2: Get the equation of the line. and R, P values
    line_eq_str = "y = " + str(round(slope,2)) + "x + " + str(round(intercept,2))
    correl_str = str(round(r_value,2))
    pvalue_str = str(p_value)
    #step 3: Calculate the regression line "y values" from the slope and intercept.
    regress_Y_values =[(x * slope + intercept) for x in x_values]
    #step 4:Create a scatter plot and plot the regression line.
    plt.scatter(x_values,y_values)
    plt.plot(x_values,regress_Y_values, color = 'r')
    plt.annotate(line_eq_str,xy= text_coordinates, fontsize =15, color = 'red')
    plt.xlabel('Latitude')
    plt.ylabel(y_label)
    plt.title(title)

    #plt.show()
    print(f'R_value is {correl_str}, and P_value is {pvalue_str}')
# %%
# seperate northern and southern hemisphere latitude
northern_hemi_df = city_data_df.loc[(city_data_df['Lat'] >= 0),:]

southern_hemi_df = city_data_df.loc[(city_data_df['Lat'] < 0),:]

northern_hemi_df.count()
southern_hemi_df.count()
# %%
# build the Northern hemisphere regression line and scatter plot for lat vs. Max Temp.
N_max_temp_x_Series = northern_hemi_df['Lat']
N_max_temp_y_Series = northern_hemi_df['Max Temp']
# call function: plot_linear_function 
plot_linear_function(N_max_temp_x_Series, 
                N_max_temp_y_Series, 
                'Linear Regression on the Northern Humisphere \n for Maximun Temperature',
                'Max Temp', (10,-40))
plt.savefig('weather_data/Regress_fig1.png')
plt.show()
# %%
# build the Southern hemisphere regression line and scatter plot for lat vs. Max Temp.
S_max_temp_x_Series = southern_hemi_df['Lat']
S_max_temp_y_Series = southern_hemi_df['Max Temp']
# call function: plot_linear_function 
plot_linear_function(S_max_temp_x_Series, 
                S_max_temp_y_Series, 
                '''Linear Regression on the Southern Humisphere 
                \n for Maximun Temperature''',
                'Max Temp', (-50,90))
plt.savefig('weather_data/Regress_fig2.png')
plt.show()
# %%
# build the Northern hemisphere regression line and scatter plot for lat vs. Humidity.
N_humidity_x_Series = northern_hemi_df['Lat']
N_humidity_y_Series = northern_hemi_df['Humidity']
# call function: plot_linear_function 
plot_linear_function(N_humidity_x_Series, 
                N_humidity_y_Series, 
                'Linear Regression on the Northern Humisphere \n for % Humidity',
                '% Humidity', (50,15))
plt.savefig('weather_data/Regress_fig3.png')
plt.show()

# %%
# build the Southern hemisphere regression line and scatter plot for lat vs. Humidity.
S_humidity_x_Series = southern_hemi_df['Lat']
S_humidity_y_Series = southern_hemi_df['Humidity']
# call function: plot_linear_function 
plot_linear_function(S_humidity_x_Series, 
                S_humidity_y_Series, 
                'Linear Regression on the Southern Humisphere \n for % Humidity',
                '% Humidity', (-55,10))
plt.savefig('weather_data/Regress_fig4.png')
plt.show()

# %%
# build the Northern hemisphere regression line and scatter plot for lat vs. Cloudiness.
N_Cloudiness_x_Series = northern_hemi_df['Lat']
N_Cloudiness_y_Series = northern_hemi_df['Cloudiness']
# call function: plot_linear_function 
plot_linear_function(N_Cloudiness_x_Series, 
                N_Cloudiness_y_Series, 
                'Linear Regression on the Northern Humisphere \n for % Cloudiness',
                '% Cloudiness', (10,50))
plt.savefig('weather_data/Regress_fig5.png')
plt.show()

# %%
# build the Southern hemisphere regression line and scatter plot for lat vs. Cloudiness.
S_Cloudiness_x_Series = southern_hemi_df['Lat']
S_Cloudiness_y_Series = southern_hemi_df['Cloudiness']
# call function: plot_linear_function 
plot_linear_function(S_Cloudiness_x_Series, 
                S_Cloudiness_y_Series, 
                'Linear Regression on the Southern Humisphere \n for % Cloudiness',
                '% Cloudiness', (-55,50))
plt.savefig('weather_data/Regress_fig6.png')
plt.show()

# %%
# build the Northern hemisphere regression line and scatter plot for lat vs. Wind Speed.
N_WindSpeed_x_Series = northern_hemi_df['Lat']
N_WindSpeed_y_Series = northern_hemi_df['Wind Speed']
# call function: plot_linear_function 
plot_linear_function(N_WindSpeed_x_Series, 
                N_WindSpeed_y_Series, 
                'Linear Regression on the Northern Humisphere \n for Wind Speed',
                'Wind Speed', (40,35))
plt.savefig('weather_data/Regress_fig7.png')
plt.show()

# %%
# build the Southern hemisphere regression line and scatter plot for lat vs. Wind Speed.
S_WindSpeed_x_Series = southern_hemi_df['Lat']
S_WindSpeed_y_Series = southern_hemi_df['Wind Speed']
# call function: plot_linear_function 
plot_linear_function(S_WindSpeed_x_Series, 
                S_WindSpeed_y_Series, 
                'Linear Regression on the Southern Humisphere \n for Wind Speed',
                'Wind Speed', (-50,20))
plt.savefig('weather_data/Regress_fig8.png')
plt.show()

# %%
