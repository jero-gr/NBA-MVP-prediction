# Import libraries
import pandas as pd
import time

# Import functions from other files
from getPlayerStatsTable import *
from getAwardsVotingTable import * 
from mergeTables import * 
from getSeasonSummaryTable import *
from normalizeTable import *
from joinPlayerTeam import *
from getTables import *

# record start time
start = time.time()

# Season
year = 2024

# Stat types
stat_type_list = ['totals', 'per_game', 'per_minute', 'per_poss', 'advanced', 'play-by-play', 'shooting', 'adj_shooting']

# Award types
award_list = ['mvp','roy','dpoy','smoy','mip','clutch_poy','leading_all_nba','leading_all_defense','leading_all_rookie','coy']

# Team stat types
team_stat_type_list = ['per_game', 'totals', 'per_poss', 'advanced', 'shooting']

fullPlayerStats = getFullPlayerStats(year)
fullSeasonSummary = getFullSeasonSummary(year)

playerStats = mergeTables(fullPlayerStats,repeat_columns=True)
seasonSummary = mergeTables(fullSeasonSummary,repeat_columns=True)

# record end time
end = time.time()

print(playerStats)
print(seasonSummary)

# print exec
print("Time of execution: ",
      (end-start), "s")

# save to csv
playerStats.to_csv('playerStats.csv')
seasonSummary.to_csv('seasonSummary.csv')