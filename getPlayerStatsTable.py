# Import libraries
from bs4 import BeautifulSoup
import requests
import pandas as pd

from getAwardsVotingTable import * 

# Function that scrapes any NBA Player Stats table from any year and type
def getPlayerStatsTable(year,stat_type,drop_duplicates=True):
    stat_type_list = ['totals', 'per_game', 'per_minute', 'per_poss', 'advanced', 'play-by-play', 'shooting', 'adj_shooting']
    stat_type_names = ['Player Totals', 'Player Per Game', 'Player Per 36 Min', 'Player Per 100 Poss', 'Player Advanced', 'Player Play-by-Play', 'Player Shooting', 'Player Adjusted Shooting']
    stat_type_dict = dict(zip(stat_type_list, stat_type_names))

    if stat_type not in stat_type_list:
        raise NameError(stat_type+' is not a valid stat type.')

    url = f"https://www.basketball-reference.com/leagues/NBA_{year}_{stat_type}.html"

    # Request url data
    req = requests.get(url)

    # Check request status
    # If 200 then correct
    req_status = req.status_code

    # Use beautiful soup to organize the HTML into a data structure that is workable for Python
    if (stat_type == 'adj_shooting'):
        table_src = req.text.split('<div class="table_container" id="div_adj-shooting">')[1].split('</table>')[0] + '</table>'
        soup = BeautifulSoup(table_src, 'html.parser')
    else:
        soup = BeautifulSoup(req.text, 'html.parser')

    # Find the HTML table
    table = soup.find('table')    
    table_body = table.find('tbody')
    table_header = table.find('thead')

    # Extract the data from the HTML header
    headers = []
    for col in table_header.find_all('tr'):
        col_data = []
        for cell in col.find_all('th'):

            cell_text = cell.getText()

            if (cell_text == 'Tm'):
                cell_text = 'Team'

            if (cell_text == '\xa0'):
                cell_text = ''

            # Iterate colspan if found (ammount of columns the header spans)
            colspan = cell.get('colspan')
            
            if (colspan == None):
                col_data.append(cell_text)
            else:
                for span in range(0,int(colspan)):
                    col_data.append(cell_text)

        headers.append(col_data)

    # Change 'Rk' column to 'playerId'
    if (headers[-1][0] == 'Rk'):
        headers[-1][0] = 'playerId'

    # Correct headers if there's an overheader (2 rows in headers list)
    if (len(headers)>1):
        tuples = list(zip(*headers))
        for i in range(0,len(tuples)):
            if (tuples[i][0]==''):
                tuples[i] = tuples[i][1]
            else:
                tuples[i] = tuples[i][0] + ', ' + tuples[i][1]
        headers = tuples
    else:
        headers = headers[0]

    # Extract the data from the HTML table
    data = []
    for row in table_body.find_all('tr'):
        row_data = []
        for cell in row.find_all('td'):

            cell_text = cell.getText()

            # Insert playerId in first column if found
            player_id = cell.get('data-append-csv')
            if (player_id != None):
                row_data.insert(0,player_id)

            row_data.append(cell_text)

        data.append(row_data)

    # Convert data to Pandas DataFrame
    data_df = pd.DataFrame(data)
    data_df.columns = headers

    # Drop duplicates and save last team of player
    if (drop_duplicates):
        data_df_keep_first = data_df.drop_duplicates(subset='playerId',ignore_index=True)
        data_df_keep_last = data_df.drop_duplicates(subset='playerId',keep='last',ignore_index=True)

        data_df = data_df_keep_first
        data_df['Team'] = data_df_keep_last['Team']

    headers = [stat_type_dict[stat_type] + ', ' + s for s in headers]
    headers[0] = 'playerId'
    data_df.columns = headers

    # Return dataframe
    data_df = data_df.set_index('playerId')
    return data_df

def getFullPlayerStats(year):
    stat_type_list = ['per_game', 'totals', 'per_poss', 'advanced', 'play-by-play', 'shooting', 'adj_shooting']
    if (year<1997):
        stat_type_list = ['per_game', 'totals', 'per_poss', 'advanced', 'adj_shooting']
    allPlayerStats = []
    for i in range(0,len(stat_type_list)):
        allPlayerStats.append(getPlayerStatsTable(year,stat_type_list[i]))

    allPlayerStats.append(getAwardsVotingTable(year,'mvp'))

    return allPlayerStats