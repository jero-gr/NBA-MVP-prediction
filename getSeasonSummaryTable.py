# Import libraries
from bs4 import BeautifulSoup
import requests
import pandas as pd

# Function that scrapes any NBA Season Summary table from any year and stat type
def getSeasonSummaryTable(year,stat_type,team='team'):
    stat_type_list = ['per_game', 'totals', 'per_poss', 'advanced', 'shooting']
    stat_type_names = ['Team Per Game', 'Team Totals', 'Team Per 100 Poss', 'Team Advanced', 'Team Shooting']
    stat_type_dict = dict(zip(stat_type_list, stat_type_names))

    if stat_type not in stat_type_list:
        raise NameError(stat_type+' is not a valid stat type.')
    
    url = f"https://www.basketball-reference.com/leagues/NBA_{year}.html"

    # Request url data
    req = requests.get(url)

    # Check request status
    # If 200 then correct
    req_status = req.status_code

    # Use beautiful soup to organize the HTML into a data structure that is workable for Python
    soup = BeautifulSoup(req.text, 'html.parser')

    div_id = 'all_'+stat_type+'_team'
    if (stat_type != 'advanced'):
        div_id += '-opponent'

    soup_id = soup.find('div', {'id': div_id})

    if (stat_type != 'advanced'):
        div_team_id = 'div_'+stat_type+'-'+team
        soup_team = soup.find('div', {'id': div_team_id})
    else:
        soup_team = soup_id
    
    # Find the HTML table
    table_body = soup_team.find('tbody')
    table_header = soup_team.find('thead')

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

    # Change 'Team' column to 'TeamName'
    if (headers[-1][1] == 'Team'):
        headers[-1][1] = 'TeamName'

    # Change 'Rk' column to 'Team'
    if (headers[-1][0] == 'Rk'):
        headers[-1][0] = 'Team'

    # Correct headers if there's an overheader (2 rows in headers list)
    '''if (len(headers)>1):
        headers = [i + j for i, j in zip(headers[0], headers[1])]
    else:
        headers = headers[0]'''

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

            # Append teamAbbrev if found
            if (cell.a):
                teamId = cell.a.get('href')
                teamId = teamId[7:10]
                row_data.insert(0,teamId)

            row_data.append(cell.getText())

        data.append(row_data)

    # Convert data to Pandas DataFrame
    data_df = pd.DataFrame(data)
    data_df.columns = headers
    data_df = data_df.set_index('Team')

    headers = data_df.columns
    headers = [stat_type_dict[stat_type] + ', ' + s for s in headers]
    data_df.columns = headers

    # Return dataframe
    return data_df

def getFullSeasonSummary(year):
    team_stat_type_list = ['per_game', 'totals', 'per_poss', 'advanced', 'shooting']
    allSeasonSummary = []
    for i in range(0,len(team_stat_type_list)):
        allSeasonSummary.append(getSeasonSummaryTable(year,team_stat_type_list[i]))
    return allSeasonSummary