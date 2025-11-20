from bokeh.io import show
from bokeh.plotting import figure
from bokeh.layouts import column
from bokeh.transform import factor_cmap
from bokeh.palettes import plasma
from bokeh.models import ColumnDataSource, Scatter
from bokeh.plotting import figure, show
from bokeh.embed import components
import math
import web_scraper
import data_analysis
import pandas as pd

player_data_df = web_scraper.scrape_player_data()

def get_component(plot):
    return components(plot)

R =  6378137.0
def lon2x(lon):
    return math.radians(lon) * R
def lat2y(lat):
    return math.log(math.tan(math.pi / 4 + math.radians(lat) / 2)) * R

def college_charts():
       # all colleges
       colleges = player_data_df.groupby(['College'])['College'].count().reset_index(name='Count')
       x_values = colleges['College'].to_list()
       y_values = colleges['Count'].to_list()
       source = ColumnDataSource(data=dict(x_values = x_values, y_values = y_values))

       p1 = figure(x_range = x_values, height = 500, width = 1000, toolbar_location = None, title = "All Colleges")
       p1.vbar(x = 'x_values', top = 'y_values', width = 1, source = source,
              fill_color=factor_cmap('x_values', palette=plasma(68), factors=x_values))
       p1.xaxis.major_label_orientation = math.pi/4
       p1.xgrid.grid_line_color = None
       p1.y_range.start = 0
       p1.y_range.end = 17

       # colleges where players > 1
       colleges = colleges[colleges['Count'] > 1]
       x_values = colleges['College'].to_list()
       y_values = colleges['Count'].to_list()
       source = ColumnDataSource(data=dict(x_values = x_values, y_values = y_values))
       
       sorted_x = sorted(x_values, key=lambda x: y_values[x_values.index(x)], reverse = True)
       p2 = figure(x_range = sorted_x, height = 500, width = 1000, toolbar_location = None, title = "Colleges with 2+ Players")
       p2.vbar(x = 'x_values', top = 'y_values', width = 1, source = source,
              fill_color=factor_cmap('x_values', palette=plasma(28), factors=sorted_x))
       p2.xaxis.major_label_orientation = math.pi/4
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
       m = figure(title='World Map', x_range=(-9000000, 15000000),
              y_range=(-1000000, 7000000), x_axis_type='mercator', 
              y_axis_type='mercator', tooltips=tooltips)

       # Adding tile
       m.add_tile("CartoDB Positron", retina=True)

       # Circling the coordinates.
       x = international['longitude'].to_list()
       y = international['latitude'].to_list()

       # source = ColumnDataSource(dict(x = x, y = y))
       # print(lon2x(x[0]), lat2y(y[0]))
       m.scatter(x = lon2x(x[0]), y = lat2y(y[0]), size=5, fill_color="blue")
       # m.circle(x = x[0], y = y[0], size=15, color='red')
       # m.circle(x=-100833, y=3086289, size=15, color='blue')
       # m.circle(x=-9754910, y=5142738, size=15, color='orange')
       # m.circle(x=1999900, y=12738, size=15, color='green')
       # m.circle(x=-7100000, y=-2425502, size=15, color='black')

       return m

if __name__ == '__main__':

       # Which colleges produce the most WNBA players?
       g1, g2 = college_charts()

       # Where are the international WNBA players from?
       g3 = international_players_map()

       show(column(g1, g2, g3))
