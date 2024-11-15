# Import libraries
import pandas as pd

# Import functions from other files
from getPlayerStatsTable import *
from getAwardsVotingTable import * 
from mergeTables import * 

# Season
year = 2024

# Stat types
stat_type_list = ['totals', 'per_game', 'per_minute', 'per_poss', 'advanced', 'play-by-play', 'shooting', 'adj_shooting']

# Award types
award_list = ['mvp','roy','dpoy','smoy','mip','clutch_poy','leading_all_nba','leading_all_defense','leading_all_rookie','all_coy']

per_game_df = getPlayerStatsTable(year,'per_game')
advanced_df = getPlayerStatsTable(year,'advanced')
playbyplay_df = getPlayerStatsTable(year,'play-by-play')

df = mergeTables([per_game_df,advanced_df,playbyplay_df],repeat_columns=True)

print(df.columns)