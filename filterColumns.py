# Import libraries
import pandas as pd
import itertools

# Define relevant columns, keep them and discard the others

def filterPlayerColumns(df):

    indexPlayer = 'playerId'

    colsPlayerPerGame = ['Player Per Game, Player', 'Player Per Game, Age', 'Player Per Game, Team', 
                        'Player Per Game, G', 'Player Per Game, MP', 'Player Per Game, FG', 'Player Per Game, FGA',
                        'Player Per Game, FG%', 'Player Per Game, 3P', 'Player Per Game, 3PA',
                        'Player Per Game, 3P%', 'Player Per Game, 2P', 'Player Per Game, 2PA',
                        'Player Per Game, 2P%', 'Player Per Game, eFG%', 'Player Per Game, FT',
                        'Player Per Game, FTA', 'Player Per Game, FT%', 'Player Per Game, ORB',
                        'Player Per Game, DRB', 'Player Per Game, TRB', 'Player Per Game, AST',
                        'Player Per Game, STL', 'Player Per Game, BLK', 'Player Per Game, TOV',
                        'Player Per Game, PF', 'Player Per Game, PTS']

    '''colsPlayerTotals = ['Player Totals, MP', 'Player Totals, FG', 'Player Totals, FGA', 'Player Totals, 3P',
                        'Player Totals, 3PA', 'Player Totals, 2P', 'Player Totals, 2PA', 'Player Totals, FT',
                        'Player Totals, FTA', 'Player Totals, ORB', 'Player Totals, DRB', 'Player Totals, TRB',
                        'Player Totals, AST', 'Player Totals, STL', 'Player Totals, BLK', 'Player Totals, TOV',
                        'Player Totals, PF', 'Player Totals, PTS', 'Player Totals, Trp-Dbl']'''
    
    colsPlayerTotals = ['Player Totals, Trp-Dbl']

    '''colsPlayerPer36Min = ['Player Per 36 Min, FG', 'Player Per 36 Min, FGA', 'Player Per 36 Min, 3P', 'Player Per 36 Min, 3PA',
                        'Player Per 36 Min, 2P', 'Player Per 36 Min, 2PA', 'Player Per 36 Min, FT', 'Player Per 36 Min, FTA',
                        'Player Per 36 Min, ORB', 'Player Per 36 Min, DRB', 'Player Per 36 Min, TRB','Player Per 36 Min, AST',
                        'Player Per 36 Min, STL', 'Player Per 36 Min, BLK', 'Player Per 36 Min, TOV', 'Player Per 36 Min, PF',
                        'Player Per 36 Min, PTS']'''

    colsPlayerPer100Poss = ['Player Per 100 Poss, FG', 'Player Per 100 Poss, FGA', 'Player Per 100 Poss, 3P', 'Player Per 100 Poss, 3PA', 
                            'Player Per 100 Poss, 2P', 'Player Per 100 Poss, 2PA', 'Player Per 100 Poss, FT', 'Player Per 100 Poss, FTA',
                            'Player Per 100 Poss, ORB', 'Player Per 100 Poss, DRB', 'Player Per 100 Poss, TRB', 'Player Per 100 Poss, AST',
                            'Player Per 100 Poss, STL', 'Player Per 100 Poss, BLK', 'Player Per 100 Poss, TOV', 'Player Per 100 Poss, PF',
                            'Player Per 100 Poss, PTS', 'Player Per 100 Poss, ORtg', 'Player Per 100 Poss, DRtg']

    colsPlayerAdvanced = ['Player Advanced, PER', 'Player Advanced, TS%', 'Player Advanced, 3PAr', 'Player Advanced, FTr',
                        'Player Advanced, ORB%', 'Player Advanced, DRB%', 'Player Advanced, TRB%', 'Player Advanced, AST%',
                        'Player Advanced, STL%', 'Player Advanced, BLK%', 'Player Advanced, TOV%', 'Player Advanced, USG%',
                        'Player Advanced, OWS', 'Player Advanced, DWS', 'Player Advanced, WS', 'Player Advanced, WS/48',
                        'Player Advanced, OBPM', 'Player Advanced, DBPM', 'Player Advanced, BPM', 'Player Advanced, VORP']

    '''colsPlayerPlayByPlay = [ 'Player Play-by-Play, Position Estimate, PG%', 'Player Play-by-Play, Position Estimate, SG%',
                            'Player Play-by-Play, Position Estimate, SF%', 'Player Play-by-Play, Position Estimate, PF%',
                            'Player Play-by-Play, Position Estimate, C%', 'Player Play-by-Play, +/- Per 100 Poss., OnCourt',
                            'Player Play-by-Play, +/- Per 100 Poss., On-Off', 'Player Play-by-Play, Turnovers, BadPass',
                            'Player Play-by-Play, Turnovers, LostBall', 'Player Play-by-Play, Fouls Committed, Shoot',
                            'Player Play-by-Play, Fouls Committed, Off.', 'Player Play-by-Play, Fouls Drawn, Shoot',
                            'Player Play-by-Play, Fouls Drawn, Off.', 'Player Play-by-Play, Misc., PGA',
                            'Player Play-by-Play, Misc., And1', 'Player Play-by-Play, Misc., Blkd']'''
    
    colsPlayerPlayByPlay = [ 'Player Play-by-Play, +/- Per 100 Poss., OnCourt', 'Player Play-by-Play, +/- Per 100 Poss., On-Off']

    '''colsPlayerShooting = ['Player Shooting, Dist.', 'Player Shooting, % of FGA by Distance, 0-3',
                        'Player Shooting, % of FGA by Distance, 3-10', 'Player Shooting, % of FGA by Distance, 10-16',
                        'Player Shooting, % of FGA by Distance, 16-3P', 'Player Shooting, % of FGA by Distance, 3P',
                        'Player Shooting, FG% by Distance, 0-3', 'Player Shooting, FG% by Distance, 3-10',
                        'Player Shooting, FG% by Distance, 10-16', 'Player Shooting, FG% by Distance, 16-3P',
                        'Player Shooting, FG% by Distance, 3P', "Player Shooting, % of FG Ast'd, 2P",
                        "Player Shooting, % of FG Ast'd, 3P", 'Player Shooting, Dunks, %FGA', 'Player Shooting, Dunks, #',
                        'Player Shooting, Corner 3s, %3PA', 'Player Shooting, Corner 3s, 3P%',
                        'Player Shooting, Heaves, Att.', 'Player Shooting, Heaves, #']'''
    
    colsPlayerShooting = ['Player Shooting, Dist.', 'Player Shooting, % of FGA by Distance, 0-3',
                        'Player Shooting, % of FGA by Distance, 3-10', 'Player Shooting, % of FGA by Distance, 10-16',
                        'Player Shooting, % of FGA by Distance, 16-3P', 'Player Shooting, % of FGA by Distance, 3P',
                        'Player Shooting, FG% by Distance, 0-3', 'Player Shooting, FG% by Distance, 3-10',
                        'Player Shooting, FG% by Distance, 10-16', 'Player Shooting, FG% by Distance, 16-3P',
                        'Player Shooting, FG% by Distance, 3P', "Player Shooting, % of FG Ast'd, 2P",
                        "Player Shooting, % of FG Ast'd, 3P", 'Player Shooting, Dunks, %FGA', 'Player Shooting, Dunks, #',
                        'Player Shooting, Corner 3s, %3PA', 'Player Shooting, Corner 3s, 3P%']

    colsPlayerAdjShooting = ['Player Adjusted Shooting, Player Shooting %, TS',
                            'Player Adjusted Shooting, Player Shooting %, FTr',
                            'Player Adjusted Shooting, Player Shooting %, 3PAr',
                            'Player Adjusted Shooting, FG Add',
                            'Player Adjusted Shooting, TS Add']

    colsPlayerMVP = ['MVP, Voting, Share']

    cols_player = list(itertools.chain(colsPlayerPerGame, colsPlayerTotals, colsPlayerPer100Poss, colsPlayerAdvanced,
                                       colsPlayerPlayByPlay, colsPlayerShooting, colsPlayerAdjShooting, colsPlayerMVP))
    
    return(df[cols_player])

def filterTeamColumns(df):
    # For team stats
    index_team = 'Team'
    cols_team = ['Team Advanced, W', 'Team Advanced, L', 'Team Advanced, MOV', 'Team Advanced, SOS', 'Team Advanced, SRS', 
                'Team Advanced, ORtg', 'Team Advanced, DRtg', 'Team Advanced, NRtg']
    return(df[cols_team])
    