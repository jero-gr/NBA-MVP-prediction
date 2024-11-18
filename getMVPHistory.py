# Import libraries
from bs4 import BeautifulSoup
import requests
import pandas as pd
import numpy as np

def getMVPHistory(save=True):
    url = 'https://www.basketball-reference.com/leagues/'

    # Request url data
    req = requests.get(url)

    # Use beautiful soup to organize the HTML into a data structure that is workable for Python
    soup = BeautifulSoup(req.text, 'html.parser')

    # Find the HTML table
    table = soup.find('table')

    # Extract the data from the HTML table
    data = []
    for row in table.find_all('tr'):
        row_data = []
        for cell in row.find_all(['th','td']):

            href = None

            # Find href
            cell_a = cell.find('a')
            if (cell_a != None):
                cell_data = cell_a.get('href')
            else:
                cell_data = cell.getText()
            
            # Append text and href
            row_data.append(cell_data)

        data.append(row_data)

    # Convert data to Pandas DataFrame
    data_df = pd.DataFrame(data[2:])
    data_df.columns = data[1]

    data_df['Season'] = data_df['Season'].str[-9:-5]
    data_df['Season'] = pd.to_numeric(data_df['Season'])
    data_df['Champion'] = data_df['Champion'].str[-13:-10]
    data_df['MVP'] = data_df['MVP'].str[11:-5]
    data_df['Rookie of the Year'] = data_df['Rookie of the Year'].str[11:-5]

    data_df = data_df[['Season','MVP']]
    data_df.set_index('Season',inplace=True)

    if (save):
        data_df.to_csv('data/MVPhistory.csv',index=True)

    return data_df

def getPlayerMVPCount(playerId,year):
    mvp_history = np.array(pd.read_csv('data/MVPHistory.csv'))
    return len(np.where((mvp_history[:,0] < year) & (mvp_history[:,1]==playerId))[0])

def getPlayerConsecutiveMVPs(playerId,year):
    mvp_history = np.array(pd.read_csv('data/MVPHistory.csv'))
    index = np.where(mvp_history[:,0]==year)[0][0]
    if (mvp_history[index+1,1] == playerId):
        if (mvp_history[index+2,1] == playerId):
            if (mvp_history[index+3,1] == playerId):
                return 3
            else:
                return 2
        else:
            return 1
    else:
        return 0
    
