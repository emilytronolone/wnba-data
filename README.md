# WNBA Data Visualizations

## Project Overview

This repository provides interactive visualizations based on [WNBA Player Data](https://www.wnba.com/players?team=all&position=all&show-historic-players=false) with future plans to explore [WNBA Team Standings Data](https://www.wnba.com/standings).

This project analyzes WNBA player data to answer questions such as:
- Which colleges produce the most WNBA players?
- Which colleges have produced multiple WNBA players?
- Where do international WNBA players come from?

---

## Tech

- **Web Scraping:**  
  BeautifulSoup
- **Analysis:**  
  Python (pandas)
- **Visualizations:**  
  Bokeh
  Panel
- **VWeb Hostings:**  
  GitHub Pages

---

## Methodology

1. **Data Cleaning:**  
   - Standardized college and country names.
   - Merged player data with country centroids for mapping.

2. **Aggregation:**  
   - Counted the number of players per college.
   - Identified colleges with more than one WNBA player.
   - Counted international players by country.

3. **Visualization:**  
   - Used Bokeh for interactive bar charts and maps.
   - Combined visualizations into a Panel dashboard with tabs (slide-show interface).
   - Exported the dashboard as a static HTML file for GitHub Pages.

---

## Visualizations

1. **All Colleges:**  
   Bar chart showing the number of WNBA players from each college.

2. **Colleges with 2+ Players:**  
   Bar chart highlighting colleges that have produced more than one WNBA player.

3. **Where do WNBA players come from?**  
   Interactive world map showing the countries represented by international WNBA players.

---

## How to View

Visit [emilytronolone.github.io/wnba-data/](https://emilytronolone.github.io/wnba-data/) to view the interactive dashboard.

---

## How to Reproduce

1. **Clone the repository:**
   ```
   git clone https://github.com/yourusername/wnba-data.git
   cd wnba-data
   ```

2. **Install dependencies:**
   ```
   pip install -r requirements.txt
   ```

3. **Run the visualization script:**
   ```
   python data/data_visualizations.py
   ```

4. **Open the generated HTML file:**
   - The dashboard will be saved as index.html.
   - You can open this file locally or push it to GitHub Pages for online viewing.