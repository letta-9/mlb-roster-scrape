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

# page = requests.get('https://www.mlb.com/prospects')
# souped = Soup(page.content, "html.parser")
# imgs = souped.find_all("img", {"class": "headshot-img headshot-img--xs"})

# img_link_list = []

# for img in imgs:
#     imgLink = img.attrs.get('src')
#     img_link_list += [imgLink]

# print(img_link_list)




# names = souped.find_all("div", {"class": "prospect-headshot__name"})

# for name in names:
#     name = name.text.strip()

# print(name)



# <img class="headshot-img headshot-img--xs" src="https://img.mlbstatic.com/mlb-photos/image/upload/v1/people/691016/headshot/silo/current" alt="Photo headshot of Tyler Soderstrom" data-testid="player-headshot" srcset="https://img.mlbstatic.com/mlb-photos/image/upload/v1/people/691016/headshot/silo/current, https://img.mlbstatic.com/mlb-photos/image/upload/v1/people/691016/headshot/silo/current 2x, https://img.mlbstatic.com/mlb-photos/image/upload/v1/people/691016/headshot/silo/current 3x" onerror="this.onerror=null;this.src='https://content.mlb.com/images/headshots/current/168x168/generic.png';this.srcset='https://content.mlb.com/images/headshots/current/168x168/generic.png';">

# for li in souped.select('img:-soup-contains("2021") + ul li'):
#     print(li.text)