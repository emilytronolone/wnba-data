from bokeh.io import show
from bokeh.plotting import figure
from bokeh.layouts import column
import web_scraper
from math import pi
from bokeh.transform import factor_cmap
from bokeh.palettes import plasma
from bokeh.models import ColumnDataSource

# all colleges
player_data_df = web_scraper.scrape_player_data()
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

show(column(p1, p2))
# print(colleges.nlargest(5, 'Count').to_html())