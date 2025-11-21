from bokeh.io import show
from bokeh.plotting import figure
from bokeh.layouts import column
from bokeh.transform import factor_cmap
from bokeh.palettes import plasma
from bokeh.models import ColumnDataSource
from bokeh.plotting import figure, show
from bokeh.embed import components
import math
import web_scraper
import data_analysis
import pandas as pd
import panel as pn

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
              fill_color=factor_cmap('x_values', palette=plasma(len(x_values)), factors=x_values))
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
              fill_color=factor_cmap('x_values', palette=plasma(len(x_values)), factors=sorted_x))
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
       tooltips = [("Country", "@Country"), ("Players", "@Count")]

       # Creating Map object
       m = figure(
              title='World Map',
              x_axis_type='mercator',
              y_axis_type='mercator',
              width=1200,
              height=700,
              tooltips=tooltips
       )

       # Adding tile
       m.add_tile("CartoDB Positron", retina=True)

       # Coordinates

       x = [lon2x(lon) for lon in international['longitude']]
       y = [lat2y(lat) for lat in international['latitude']]

       source = ColumnDataSource(data=dict(
              x=x,
              y=y,
              Country=international['Country'],
              Count=international['Count']
       ))

       m.scatter(x='x', y='y', size=10, fill_color="red", source=source)

       return m

if __name__ == '__main__':

       # Which colleges produce the most WNBA players?
       p1, p2 = college_charts()

       # Where are the international WNBA players from?
       m = international_players_map()

       # Create deck
       deck = pn.Tabs(
              ('All Colleges', pn.panel(p1)),
              ('Colleges with 2+ Players', pn.panel(p2)),
              ('Where do WNBA players come from?', pn.panel(m))
       )

       deck.save("../index.html", embed=True)