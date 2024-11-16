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

# Scrape tables from 2004-05 to 2023-24
'''for year in range(2005,2025):
    scrapeAllTables(year)
'''

'''yearlyPatterns_x, yearlyPatterns_y = getYearlyPatterns(year,n)

print(yearlyPatterns_x)
print(yearlyPatterns_y)'''