import requests
from bs4 import BeautifulSoup
import json
import pandas as pd

def scrape_player_data():
    url = 'https://www.wnba.com/players?team=all&position=all&show-historic-players=false'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    soup = json.loads((soup.find('script', id='__NEXT_DATA__', type='application/json').text))
    player_data = soup['props']['pageProps']['allPlayersData']
    
    return etl_player_data(player_data)

def scrape_standings():
    url = 'https://www.wnba.com/standings'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    soup = json.loads((soup.find('script', id='__NEXT_DATA__', type='application/json').text))
    standings = (soup['props']['pageProps']['standingsRowsData'])

    return etl_standings(standings)

def etl_player_data(list):
    updated_list = []
    for player in list:
        # before
        # print(player)

        # removing unneccessary data
        player = player[:15]
        player.pop(12)
        player.pop(8)
        player.pop(5)
        player.pop(4)
        player.pop(3)
        player.pop(0)

        # updating format for team name
        if player[2] == None:
            player.append(None)
        else:
            team_name = player[2] + ' ' + player[3]
            player.append(team_name)
        player.pop(3)
        player.pop(2)

        # fix consistency errors
        if player[5].isspace() or player[5] == '-' or not player[5]:
            player[5] = None

        # after
        # print(player)
        updated_list.append(player)

    df = pd.DataFrame(updated_list, columns = ['Last Name', 'First Name', 'Number', 'Position', 'Height', 'College', 'Country', 'Team'])
    return df

def etl_standings(list):
    updated_list = []
    for dict in list:
        # before
        # print(dict)
        updated_dict = {}
        updated_dict['Rank'] = dict['PlayoffRank']
        updated_dict['Team'] = dict['TeamCity'] + ' ' + dict['TeamName']
        updated_dict['Conference'] = dict['Conference']
        updated_dict['Total Wins'] = dict['WINS']
        updated_dict['Total Losses'] = dict['LOSSES']

        #after
        #print(updated_dict)
        updated_list.append(updated_dict)

    df = pd.DataFrame.from_dict(updated_list)
    return df