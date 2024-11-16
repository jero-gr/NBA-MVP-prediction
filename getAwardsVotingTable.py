# Import libraries
from bs4 import BeautifulSoup
import requests
import pandas as pd

# Function that scrapes any NBA Awards table from any year and award

def getAwardsVotingTable(year,award):
    award_list = ['mvp','roy','dpoy','smoy','mip','clutch_poy','leading_all_nba','leading_all_defense','leading_all_rookie','coy']
    award_names = ['MVP', 'ROY', 'DPOY', '6MOY','MIP','Clutch POY','All-NBA','All-Defense','All-Rookie','COY']
    award_dict = dict(zip(award_list, award_names))

    if award not in award_list:
        raise NameError(award+' is not a valid award type.')
    
    url = f"https://www.basketball-reference.com/awards/awards_{year}.html"

    # Request url data
    req = requests.get(url)

    # Check request status
    # If 200 then correct
    req_status = req.status_code

    # Use beautiful soup to organize the HTML into a data structure that is workable for Python
    soup = BeautifulSoup(req.text, 'html.parser')

    div_id = 'all_'+award
    soup_id = soup.find('table', {'id': award})
    
    # Find the HTML table
    table_body = soup_id.find('tbody')
    table_header = soup_id.find('thead')

    # Extract the data from the HTML header
    headers = []
    for col in table_header.find_all('tr'):
        col_data = []
        for cell in col.find_all('th'):

            # Iterate colspan if found (ammount of columns the header spans)
            colspan = cell.get('colspan')
            if (colspan != None):
                for span in range(0,int(colspan)):
                    col_data.append(cell.getText())
            else:
                col_data.append(cell.getText())

        headers.append(col_data)

    # Change 'Rk' column to 'playerId'
    '''if (headers[-1][0] == 'Rk' or headers[-1][0] == 'Rank'):
        headers[-1][0] = 'playerId'
    else:    
        headers[-1].insert(0, 'playerId')'''
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

            # Append playerId if found
            player_id = cell.get('data-append-csv')
            if (player_id != None):
                row_data.insert(0,player_id)

            row_data.append(cell.getText())

        data.append(row_data)

    # Convert data to Pandas DataFrame
    data_df = pd.DataFrame(data)
    data_df.columns = headers

    headers = [award_dict[award] + ', ' + s for s in headers]
    headers[0] = 'playerId'
    data_df.columns = headers

    # Return dataframe
    data_df = data_df.set_index('playerId')
    return data_df