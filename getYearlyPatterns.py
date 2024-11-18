# Import libraries
import pandas as pd
import numpy as np

# Import functions from other files
from getPlayerStatsTable import *
from getAwardsVotingTable import * 
from mergeTables import * 
from getSeasonSummaryTable import *
from normalizeTable import *
from joinPlayerTeam import *
from scrapeAllTables import *
from filterColumns import *
from getMVPHistory import *

# Get top n patterns from year according to criteria
def getYearlyPatterns(year,n,criteria='MPG'):

    ### Player stats ###
    # Load/get player stats
    playerStats = pd.read_csv(f'data/{year}playerStats.csv')

    # Set 'playerId' column as index
    playerStats = playerStats.set_index('playerId')

    # Filter irrelevant columns
    playerStats = filterPlayerColumns(playerStats)

    # Rename 'Player Per Game, Team' column to 'Team'
    playerStats.columns = ['Team' if x=='Player Per Game, Team' else x for x in playerStats.columns]

    ### Team stats ###
    # Load/get team stats
    teamStats = pd.read_csv(f'data/{year}seasonSummary.csv')

    # Set 'Team' column as index
    teamStats = teamStats.set_index('Team')

    # Filter irrelevant columns
    teamStats = filterTeamColumns(teamStats)

    # Calculate win percentage
    teamStats['Team Advanced, W'] = teamStats['Team Advanced, W']/(teamStats['Team Advanced, W']+teamStats['Team Advanced, L'])

    ### Joined stats ###
    # Join player and team stats and set NaN values to 0
    joinedStats = joinPlayerTeam(playerStats,teamStats).fillna(0)

    ### Normalize all joined stats columns excluding specific ones ###
    # Define columns to exclude
    cols_to_exclude = ['Player Per Game, Player', 'Team', 'Team Advanced, L']

    # Drop excluded columns
    joinedStats = joinedStats.drop(columns=cols_to_exclude)

    # Sort by minutes played per game and keep top n
    joinedStats = joinedStats.sort_values('Player Per Game, MP',ascending=False)
    joinedStats = joinedStats.head(n)

    # Normalize columns and separate pattern input and output
    joinedStats_x = joinedStats.drop(columns=['MVP, Voting, First', 'MVP, Voting, Share'])
    joinedStats_x = normalizeTable(joinedStats_x)    

    joinedStats_y = joinedStats[['MVP, Voting, First', 'MVP, Voting, Share']].copy()
    joinedStats_y['MVP, Voting, First'] = normalizeTable(joinedStats_y['MVP, Voting, First'],'sum').values

    # Calculate MVP History columns ('MVP, count', 'MVP, consecutive')
    players = list(joinedStats.index.values)
    mvpHistoryColumns = np.zeros((n,2))
    for p in range(0,n):
        playerId = players[p]
        mvpHistoryColumns[p,0] = getPlayerMVPCount(playerId,year)
        mvpHistoryColumns[p,1] = getPlayerConsecutiveMVPs(playerId,year)

    mvpHistoryColumns = pd.DataFrame(mvpHistoryColumns)
    #mvpHistoryColumns = normalizeTable(mvpHistoryColumns)
    mvpHistoryColumns.columns = ['MVP, count', 'MVP, consecutive']
    mvpHistoryColumns.index = joinedStats_x.index

    joinedStats_x = joinedStats_x.join(mvpHistoryColumns)

    joinedStats = joinedStats_x.join(joinedStats_y)

    ### Return values as dataframes
    return joinedStats