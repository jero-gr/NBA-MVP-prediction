# Import libraries
import pandas as pd

# Function that left joins a dataframe with playerId indexing and a dataframe with Team indexing
def joinPlayerTeam(player_df,team_df):
    return player_df.join(team_df, on='Team', lsuffix='_Player', rsuffix='_Tm')