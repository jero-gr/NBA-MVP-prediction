# Import libraries
import pandas as pd
import time
from datetime import datetime

# Import functions from other files
from getPlayerStatsTable import *
from getAwardsVotingTable import * 
from mergeTables import * 
from getSeasonSummaryTable import *
from normalizeTable import *
from joinPlayerTeam import *

def scrapeAllTables(year):

    # record start time
    start = time.time()
    print(datetime.fromtimestamp(start), f'{year} Scraping started')

    # Stat types
    stat_type_list = ['totals', 'per_game', 'per_minute', 'per_poss', 'advanced', 'play-by-play', 'shooting', 'adj_shooting']

    # Award types
    award_list = ['mvp','roy','dpoy','smoy','mip','clutch_poy','leading_all_nba','leading_all_defense','leading_all_rookie','coy']

    # Team stat types
    team_stat_type_list = ['per_game', 'totals', 'per_poss', 'advanced', 'shooting']

    # Get player stats (Player Stats)
    print(datetime.fromtimestamp(time.time()), 'Getting player stats')
    fullPlayerStats = getFullPlayerStats(year)

    # Get team stats (Season Summary)
    print(datetime.fromtimestamp(time.time()), 'Getting team stats')
    fullSeasonSummary = getFullSeasonSummary(year)

    # Merge all player stats
    playerStats = mergeTables(fullPlayerStats,repeat_columns=True)

    # Merge all team stats
    seasonSummary = mergeTables(fullSeasonSummary,repeat_columns=True)
    
    # save to csv
    print(datetime.fromtimestamp(time.time()), 'Saving to .csv')
    playerStats.to_csv(f'data/{year}playerStats.csv')
    seasonSummary.to_csv(f'data/{year}seasonSummary.csv')

    # record end time
    end = time.time()

    # print exec
    print(datetime.fromtimestamp(end), f'{year} Scraping finished')
    print("Time of execution: ",(end-start), "s")
    
    return