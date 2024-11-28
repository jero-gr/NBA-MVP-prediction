# Import libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Import scikit
from sklearn.ensemble import RandomForestRegressor
from sklearn.datasets import make_classification
from sklearn.neural_network import MLPRegressor

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
from getPatterns import *
from modelComparison import *

np.set_printoptions(suppress=True)

# Generate patterns
year_start = 1980
year_end = 2025
n = 100
'''
savePatterns(n=n,year_A=year_start,year_B=year_end)'''


# Load patterns
df = pd.read_csv('data/patterns.csv')

# Convert patterns to NumPy
df = df.fillna(0)
mat_pat = np.array(df)

# Extract playerId
playerId = mat_pat[:,0]
playerId = np.transpose(np.array([playerId]))

# Create testing and training sets
trn_years = [1980, 2010]
tst_years = [2010, 2025]

trn_index = getPatternsIndexes(n,year_start,trn_years)
tst_index = getPatternsIndexes(n,year_start,tst_years)

x_trn = mat_pat[trn_index,1:-2]
y_trn = mat_pat[trn_index,-2:]

x_tst = mat_pat[tst_index,1:-2]
y_tst = mat_pat[tst_index,-2:]


### Training ###
'''
### MLP 50, logistic
print('MLP 50,')
score = np.zeros(10)
for prueba in range(0,10):
    reg = []
    reg.append(MLPRegressor(hidden_layer_sizes=(50,),early_stopping=False,activation='logistic').fit(x_trn,y_trn))

    ### Testing ###
    y_predict = []
    for i in range(0,len(reg)):
        y_predict.append(reg[i].predict(x_tst))

    tst_id = playerId[tst_index]

    comparison_df = getModelComparison(n,tst_id,y_predict,y_tst,tst_years)
    #showModelComparison(comparison_df,top=3)
    #saveModelComparison(comparison_df,top=5)
    #top = [1,2,3,4,5]
    #score = scoreModelComparison(comparison_df,top)

    x = ['1','2','3','4','5','6','7','8','9','10']
    score += scoreMVP(comparison_df)

print(score)

### MLP 50, default
print('MLP 50,activation=default')
score = np.zeros(10)
for prueba in range(0,10):
    reg = []
    reg.append(MLPRegressor(hidden_layer_sizes=(50,),early_stopping=False).fit(x_trn,y_trn))

    ### Testing ###
    y_predict = []
    for i in range(0,len(reg)):
        y_predict.append(reg[i].predict(x_tst))

    tst_id = playerId[tst_index]

    comparison_df = getModelComparison(n,tst_id,y_predict,y_tst,tst_years)
    #showModelComparison(comparison_df,top=3)
    #saveModelComparison(comparison_df,top=5)
    #top = [1,2,3,4,5]
    #score = scoreModelComparison(comparison_df,top)

    x = ['1','2','3','4','5','6','7','8','9','10']
    score += scoreMVP(comparison_df)

print(score)

### MLP 50,10
print('MLP 50,10 default')
score = np.zeros(10)
for prueba in range(0,10):
    reg = []
    reg.append(MLPRegressor(hidden_layer_sizes=(50,10),early_stopping=False).fit(x_trn,y_trn))
    
    ### Testing ###
    y_predict = []
    for i in range(0,len(reg)):
        y_predict.append(reg[i].predict(x_tst))

    tst_id = playerId[tst_index]

    comparison_df = getModelComparison(n,tst_id,y_predict,y_tst,tst_years)
    #showModelComparison(comparison_df,top=3)
    #saveModelComparison(comparison_df,top=5)
    #top = [1,2,3,4,5]
    #score = scoreModelComparison(comparison_df,top)

    x = ['1','2','3','4','5','6','7','8','9','10']
    score += scoreMVP(comparison_df)

print(score)

'''
### Random Forest
print('Random Forest, n_estimators=100, max_depth=20')
score = np.zeros(10)
for prueba in range(0,10):
    print(prueba+1,' de ',10)
    reg = []
    reg.append(RandomForestRegressor(n_estimators=100,max_depth=20).fit(x_trn,y_trn))
    
    ### Testing ###
    y_predict = []
    for i in range(0,len(reg)):
        y_predict.append(reg[i].predict(x_tst))

    tst_id = playerId[tst_index]

    comparison_df = getModelComparison(n,tst_id,y_predict,y_tst,tst_years)

    x = ['1','2','3','4','5','6','7','8','9','10']
    score += scoreMVP(comparison_df)

print(score)

'''
score = scoreMVP(comparison_df,pos=1)
print(score)

score = scoreMVP(comparison_df,pos=2)
print(score)'''

#plt.bar(x,(score/np.sum(score))*100)
#plt.show()
