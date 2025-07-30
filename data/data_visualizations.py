from bokeh.io import show
from bokeh.plotting import figure
from bokeh.layouts import column
from math import pi
from bokeh.transform import factor_cmap
from bokeh.palettes import plasma
from bokeh.models import ColumnDataSource
from bokeh.plotting import figure, show
import web_scraper
import data_analysis
import pandas as pd

player_data_df = web_scraper.scrape_player_data()

def college_data():
       # all colleges
       colleges = player_data_df.groupby(['College'])['College'].count().reset_index(name='Count')
       x_values = colleges['College'].to_list()
       y_values = colleges['Count'].to_list()
       source = ColumnDataSource(data=dict(x_values = x_values, y_values = y_values))

       p1 = figure(x_range = x_values, height = 500, width = 1000, toolbar_location = None, title = "All Colleges")
       p1.vbar(x = 'x_values', top = 'y_values', width = 1, source = source,
              fill_color=factor_cmap('x_values', palette=plasma(68), factors=x_values))
       p1.xaxis.major_label_orientation = pi/4
       p1.xgrid.grid_line_color = None
       p1.y_range.start = 0
       p1.y_range.end = 17

       # colleges where players > 1
       colleges = colleges[colleges['Count'] > 1]
       x_values = colleges['College'].to_list()
       y_values = colleges['Count'].to_list()
       source = ColumnDataSource(data=dict(x_values = x_values, y_values = y_values))
       
       p2 = figure(x_range = x_values, height = 500, width = 1000, toolbar_location = None, title = "Colleges with 2+ Players")
       p2.vbar(x = 'x_values', top = 'y_values', width = 1, source = source,
              fill_color=factor_cmap('x_values', palette=plasma(28), factors=x_values))
       p2.xaxis.major_label_orientation = pi/4
       p2.xgrid.grid_line_color = None
       p2.y_range.start = 0
       p2.y_range.end = 17

       return p1, p2

def international_players_map():

       # country coordinates not including USA
       centroids = data_analysis.csv_to_df('countries.csv')
       international = player_data_df.groupby(['Country'])['Country'].count().reset_index(name='Count')
       international = pd.merge(centroids, international, on='Country', how='inner')

       # hover data
       tooltips = ("GeeksForGeeks")

       # Creating Map object
       m = figure(title='World Map', x_range=(-12000000, 9000000),
              y_range=(-1000000, 7000000), x_axis_type='mercator', 
              y_axis_type='mercator', tooltips=tooltips)

       # Adding title
       m.add_tile("CartoDB Positron", retina=True)

       # Circling the coordinates.
       x = international['latitude'].to_list()
       print(x)
       y = international['longitude'].to_list()

       # source = ColumnDataSource(data=dict(lat=latitude, lon=longitude))

       # m.scatter(x, y, size=5, fill_color="blue", fill_alpha=0.8)
       m.circle(x=-100833, y=5211172, size=15, color='red')
       # m.circle(x=-100833, y=3086289, size=15, color='blue')
       # m.circle(x=-9754910, y=5142738, size=15, color='orange')
       # m.circle(x=1999900, y=12738, size=15, color='green')
       # m.circle(x=-7100000, y=-2425502, size=15, color='black')

       # Displaying the Map using show function
       return m

if __name__ == '__main__':

       # Which colleges produce the most WNBA players?
       g1, g2 = college_data()

       # Where are the international WNBA players from?
       g3 = international_players_map()

       show(column(g1, g2, g3))