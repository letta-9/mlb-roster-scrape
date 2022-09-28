from bs4 import BeautifulSoup as Soup
import requests
import pandas as pd
from pandas import DataFrame


teams = ['BOS', 'NYY', 'TBR', 'TOR', 'BAL', 'CHW', 'KCR', 'CLE', 'MIN', 'DET',
            'OAK', 'HOU', 'LAA', 'SEA', 'TEX', 'ATL', 'NYM', 'PHI', 'MIA', 'WSN',
            'STL', 'PIT', 'MIL', 'CHC', 'CIN', 'ARI', 'LAD', 'SFG', 'COL', 'SDP']

players = []
players_df = pd.DataFrame(players)

for x in teams:

    response = requests.get('https://www.baseball-reference.com/teams/BOS/2022-roster.shtml')
    soup = Soup(response.text, 'lxml')
    tables = soup.find_all('table')

    data = tables[0]
    rows = data.find_all('tr')

    def parse_row(row):
        return [str(x.string) for x in row.find_all('a')]

    list_of_parsed_rows = [parse_row(row) for row in rows]
    data_df = DataFrame(list_of_parsed_rows)

    players_df = pd.concat([players_df, data_df])

players_df = players_df.dropna()
players_df.rename(columns = {0:'name'}, inplace=True)
players_df = players_df['name'].str.lower()
players_df = players_df.str.replace('[^\w\s]','')
players_df = players_df.str.normalize('NFKD').str.encode('ascii', errors='ignore').str.decode('utf-8')

players_df.to_csv('mlb_list.csv', index=False)