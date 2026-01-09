from bokeh.plotting import figure
from bokeh.transform import factor_cmap
from bokeh.palettes import plasma
from bokeh.models import ColumnDataSource
from bokeh.plotting import figure
from bokeh.embed import components
import math
import web_scraper as web_scraper
import pandas as pd


R = 6378137  # radius of the Earth in meters
player_data_df = web_scraper.scrape_player_data()


def get_component(plot):
    return components(plot)


def lon2x(lon):
    return math.radians(lon) * R


def lat2y(lat):
    return math.log(math.tan(math.pi / 4 + math.radians(lat) / 2)) * R


def college_charts():
    # all colleges
    colleges = (
        player_data_df.groupby(["College"])["College"].count().reset_index(name="Count")
    )

    # combine first and last name into a single "Player" column
    player_data_df["Player"] = (
        player_data_df["First Name"] + " " + player_data_df["Last Name"]
    )

    # get player names for each college
    college_players = (
        player_data_df.groupby("College")["Player"]
        .apply(
            lambda x: ",<br>".join(
                [", ".join(x[i : i + 3]) for i in range(0, len(x), 3)]
            )
        )
        .reset_index(name="Players")
    )

    colleges = colleges.merge(college_players, on="College", how="left")
    x_values = colleges["College"].to_list()
    y_values = colleges["Count"].to_list()
    players = colleges["Players"].to_list()
    source = ColumnDataSource(
        data=dict(x_values=x_values, y_values=y_values, players=players)
    )
    tooltips = [
        ("College", "@x_values"),
        ("Players", "@players{safe}"),
        ("Count", "@y_values"),
    ]

    # p1: all colleges
    p1 = figure(
        x_range=x_values,
        height=600,
        width=18 * len(x_values),
        toolbar_location=None,
        title="All Colleges",
        tooltips=tooltips,
    )
    p1.vbar(
        x="x_values",
        top="y_values",
        width=1,
        source=source,
        fill_color=factor_cmap(
            "x_values", palette=plasma(len(x_values)), factors=x_values
        ),
    )
    p1.xaxis.major_label_orientation = math.pi / 4
    p1.xgrid.grid_line_color = None
    p1.y_range.start = 0
    p1.y_range.end = max(y_values) + 1

    # p2: colleges where players > 1
    colleges = colleges[colleges["Count"] > 1]
    x_values = colleges["College"].to_list()
    y_values = colleges["Count"].to_list()
    players = colleges["Players"].to_list()
    source = ColumnDataSource(
        data=dict(x_values=x_values, y_values=y_values, players=players)
    )

    sorted_x = sorted(x_values, key=lambda x: y_values[x_values.index(x)], reverse=True)
    p2 = figure(
        x_range=sorted_x,
        height=500,
        width=1000,
        toolbar_location=None,
        title="Colleges with 2+ Players",
        tooltips=tooltips,
    )
    p2.vbar(
        x="x_values",
        top="y_values",
        width=1,
        source=source,
        fill_color=factor_cmap(
            "x_values", palette=plasma(len(x_values)), factors=sorted_x
        ),
    )
    p2.xaxis.major_label_orientation = math.pi / 4
    p2.xgrid.grid_line_color = None
    p2.y_range.start = 0
    p2.y_range.end = max(y_values) + 1

    return p1, p2


def international_players_map():

    # country coordinates not including USA
    centroids = pd.read_csv("data/countries.csv")
    international = (
        player_data_df.groupby(["Country"])["Country"].count().reset_index(name="Count")
    )
    international = pd.merge(centroids, international, on="Country", how="inner")

    # hover data
    tooltips = [("Country", "@Country"), ("Players", "@Count")]

    # creating map object
    m = figure(
        title="World Map",
        x_axis_type="mercator",
        y_axis_type="mercator",
        width=1200,
        height=700,
        tooltips=tooltips,
    )

    # adding tile
    m.add_tile("CartoDB Positron", retina=True)

    # coordinates
    x = [lon2x(lon) for lon in international["longitude"]]
    y = [lat2y(lat) for lat in international["latitude"]]

    source = ColumnDataSource(
        data=dict(
            x=x, y=y, Country=international["Country"], Count=international["Count"]
        )
    )

    m.scatter(x="x", y="y", size=10, fill_color="red", source=source)

    return m
