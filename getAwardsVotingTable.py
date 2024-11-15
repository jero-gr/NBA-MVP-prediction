# Import libraries
from bs4 import BeautifulSoup
import requests
import pandas as pd

# Function that scrapes any NBA Awards table from any year and award

def getAwardsVotingTable(year,award):
    award_list = ['mvp','roy','dpoy','smoy','mip','clutch_poy','leading_all_nba','leading_all_defense','leading_all_rookie','all_coy']

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
    soup_award = soup.find('div', {'id': div_id})

    print(soup_award)
    
    # Find the HTML table
    table_body = soup_award.find('tbody')
    table_header = soup_award.find('thead')

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

    # Return dataframe
    return data_df.set_index('playerId')