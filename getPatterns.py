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
from getYearlyPatterns import *

def savePatterns(n=100,year_A=1980,year_B=2025):
    # Load data and create yearly patterns
    patterns = []
    for year in range(year_A,year_B):
        pat = getYearlyPatterns(year,n,criteria='MPG')
        patterns.append(pat)

    df = pd.concat(patterns,axis=0)
    df.to_csv("data/patterns.csv")

    return

def getPatternsIndexes(n,year_first,year_range):
    index_return = np.empty(0,dtype=int)

    for i in range(0,len(year_range),2):
        years = np.arange(year_range[i],year_range[i+1])
        index = np.empty(n*len(years),dtype=int)

        for j in range(0,len(years)):
            year = years[j]
            base_index = year-year_first
            base_index = base_index * n
            index[j*n:j*n+n] = np.arange(0,n)+base_index

        index_return = np.append(index_return,index)

    return index_return



