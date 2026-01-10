from bokeh.plotting import figure
from bokeh.transform import factor_cmap
from bokeh.palettes import plasma
from bokeh.models import ColumnDataSource
from bokeh.plotting import figure
from bokeh.embed import components
from bokeh.models import LabelSet
from bokeh.models import CustomJSTickFormatter
import math
import web_scraper as web_scraper
import pandas as pd
import numpy as np


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

    # # custom palette
    # pink_palette = [
    #     "#ffe6f2",
    #     "#ffc9e4",
    #     "#f9a1cd",
    #     "#ff87c3",
    #     "#ff67b3",
    #     "#ff4ea7",
    #     "#ff2492",
    #     "#FF0080",
    # ]
    # # repeat or trim the palette to match the number of bars
    # palette = (pink_palette * ((len(x_values) // len(pink_palette)) + 1))[
    #     : len(x_values)
    # ]

    # p1: all colleges
    p1 = figure(
        x_range=x_values,
        height=600,
        width=max(1000, 18 * len(x_values)),
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
            "x_values",
            palette=plasma(len(x_values)),
            factors=x_values,
            # "x_values",
            # palette=palette,
            # factors=x_values,
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
        width=max(1000, 18 * len(x_values)),
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

    # country centroids
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


def average_height_team():
    # average height per team
    player_data_df["Height_in"] = player_data_df["Height"].apply(
        lambda x: int(x.split("-")[0]) * 12 + int(x.split("-")[1])
    )
    avg_height = player_data_df.groupby("Team")["Height_in"].mean().reset_index()
    avg_height = avg_height.sort_values(by="Height_in", ascending=False)

    x_values = avg_height["Team"].to_list()
    y_values = avg_height["Height_in"].to_list()

    # Labels as inches rounded to 2 decimal places
    labels = [f'{h:.2f}"' for h in y_values]

    source = ColumnDataSource(
        data=dict(x_values=x_values, y_values=y_values, labels=labels)
    )

    tooltips = [
        ("Team", "@x_values"),
        ("Average Height (inches)", "@labels"),
    ]

    p = figure(
        x_range=x_values,
        height=600,
        width=max(1000, 100 * len(x_values)),
        toolbar_location=None,
        title="Average Height per Team",
        tooltips=tooltips,
    )

    # Set y-axis ticks at every inch between min and max heights
    min_tick = int(np.floor(min(y_values)))
    max_tick = int(np.ceil(max(y_values)))
    p.yaxis.ticker = list(range(min_tick, max_tick + 1))

    # Format y-axis as feet'inches''
    p.yaxis.formatter = CustomJSTickFormatter(
        code="""
        var feet = Math.floor(tick / 12);
        var inches = Math.round(tick - feet * 12);
        if (inches == 12) {
            feet += 1;
            inches = 0;
        }
        return feet + "'" + " " + inches + "''";
    """
    )

    # Scatter plot
    p.scatter(
        x="x_values",
        y="y_values",
        size=10,
        source=source,
        color="#ff4ea7",
        alpha=0.8,
    )

    p.line(
        x="x_values",
        y="y_values",
        source=source,
        line_width=2,
        color="#b30059",
        alpha=0.7,
    )

    labels_set = LabelSet(
        x="x_values",
        y="y_values",
        text="labels",
        level="glyph",
        x_offset=-18,
        y_offset=8,
        source=source,
        text_font_size="12px",
        text_color="#b30059",
    )
    p.add_layout(labels_set)

    p.xaxis.major_label_orientation = math.pi / 4
    p.xgrid.grid_line_color = None
    p.y_range.start = min(y_values) - 0.5
    p.y_range.end = max(y_values) + 0.5

    return p
