from operator import concat
from urllib import request
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

    response = requests.get('https://www.fangraphs.com/prospects/the-board/2022-in-season-prospect-list/scouting-position?sort=-1,1&pageitems=100&pg=0&type=2')
    soup = Soup(response.text, 'lxml')
    tables = soup.find(text='Hit')

    for row in tables.find_all("tr")[1:]:
        print([cell.get_text(strip=True) for cell in row.find_all("td")])

    data = tables[5]
    rows = soup.find_all('tr', attrs = {'class':'the-board-data','class': 'team-unpublished'})

    def parse_row(row):
        return [str(x.string) for x in row.find_all('td')]

    list_of_parsed_rows = [parse_row(row) for row in rows]
    data_df = DataFrame(list_of_parsed_rows)

    print(tables)

    players_df = pd.concat([players_df, data_df])

players_df = players_df.dropna()
players_df.rename(columns = {0:'name'}, inplace=True)
players_df = players_df['name'].str.lower()
players_df = players_df.str.replace('[^\w\s]','')
players_df = players_df.str.normalize('NFKD').str.encode('ascii', errors='ignore').str.decode('utf-8')

players_df.to_csv('mlb_list.csv', index=False)
