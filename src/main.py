import panel as pn
import data_visualizations

if __name__ == "__main__":

    # Which colleges produce the most WNBA players?
    p1, p2 = data_visualizations.college_charts()

    # Where are the international WNBA players from?
    m = data_visualizations.international_players_map()

    # Create deck
    deck = pn.Tabs(
        ("All Colleges", pn.panel(p1)),
        ("Colleges with 2+ Players", pn.panel(p2)),
        ("Where do WNBA players come from?", pn.panel(m)),
    )

    deck.save("../index.html", embed=True)
