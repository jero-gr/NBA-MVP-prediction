# Import libraries
from bs4 import BeautifulSoup
import requests
import pandas as pd

# Function that scrapes any NBA Player Stats table from any year and type
def getPlayerStatsTable(year,stat_type,drop_duplicates=True):
    stat_type_list = ['totals', 'per_game', 'per_minute', 'per_poss', 'advanced', 'play-by-play', 'shooting', 'adj_shooting']

    if stat_type not in stat_type_list:
        raise NameError(stat_type+' is not a valid stat type.')

    url = f"https://www.basketball-reference.com/leagues/NBA_{year}_{stat_type}.html"

    # Request url data
    req = requests.get(url)

    # Check request status
    # If 200 then correct
    req_status = req.status_code

    # Use beautiful soup to organize the HTML into a data structure that is workable for Python
    soup = BeautifulSoup(req.text, 'html.parser')

    # Find the HTML table
    table_body = soup.find('tbody')
    table_header = soup.find('thead')

    # Extract the data from the HTML header
    headers = []
    for col in table_header.find_all('tr'):
        col_data = []
        for cell in col.find_all('th'):

            cell_text = cell.getText()
            if (cell_text == 'Tm'):
                cell_text = 'Team'

            # Iterate colspan if found (ammount of columns the header spans)
            colspan = cell.get('colspan')
            if (colspan != None):
                for span in range(0,int(colspan)):
                    col_data.append(cell_text)
            else:
                col_data.append(cell_text)

        headers.append(col_data)

    # Change 'Rk' column to 'playerId'
    if (headers[-1][0] == 'Rk'):
        headers[-1][0] = 'playerId'

    # Correct headers if there's an overheader (2 rows in headers list)
    if (len(headers)>1):
        headers = [i + j for i, j in zip(headers[0], headers[1])]
    else:
        headers = headers[0]

    # Extract the data from the HTML table
    data = []
    for row in table_body.find_all('tr'):
        row_data = []
        for cell in row.find_all('td'):

            # Append playerId if found
            player_id = cell.get('data-append-csv')
            if (player_id != None):
                row_data.append(player_id)

            row_data.append(cell.getText())

        data.append(row_data)

    # Convert data to Pandas DataFrame
    headers_df = pd.DataFrame(headers)
    data_df = pd.DataFrame(data)
    data_df.columns = headers

    # Drop duplicates and save last team of player
    if (drop_duplicates):
        data_df_keep_first = data_df.drop_duplicates(subset='playerId',ignore_index=True)
        data_df_keep_last = data_df.drop_duplicates(subset='playerId',keep='last',ignore_index=True)
        data_df = data_df_keep_first
        data_df['Team'] = data_df_keep_last['Team']

    # Return dataframe
    return data_df.set_index('playerId')