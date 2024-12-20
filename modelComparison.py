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
from getPatterns import *

def getModelComparison(n,tst_id,y_predict,y_tst,tst_years): # y_predict is a list of y_predict values
    # predict_np is a list of NumPy arrays
    # Each element contains NumPy array, first column is playerId, second and third columns are predictions of regressor i
    predict_np = []
    for i in range(0,len(y_predict)):
        #y_predict[i] = np.transpose(np.array([y_predict[i]]))
        predict_np.append(np.hstack((tst_id,y_predict[i])))
    tst_np = np.hstack((tst_id,y_tst))

    # Get all prediction seasons years
    years_list = np.empty(0)
    for i in range(0,len(tst_years),2):
        years_aux = np.arange(tst_years[i],tst_years[i+1])
        years_list = np.append(years_list,years_aux)

    df_comparison = []

    # For each year
    for i in range(0,len(years_list)):
        # Set dataframe column names initial values
        df_columns = []

        # Get real voting shares sorted (desc)
        year_tst = tst_np[n*i:n*(i+1)]
        year_tst = year_tst[year_tst[:,2].argsort()[::-1]]

        # Add to comparison table
        year_comparison = year_tst

        # For each element of predict_np
        for j in range(0,len(predict_np)):
            # Sort element of predict_np by second column (1st votes %, desc)
            year_predict = predict_np[j]
            year_predict = year_predict[n*i:n*(i+1)]
            year_predict = year_predict[year_predict[:,2].argsort()[::-1]]

            # Add to comparison table
            year_comparison = np.hstack((year_predict,year_comparison))

            # Add column names
            df_columns.append('Regressor '+str(j)+ ' playerId')
            df_columns.append('Regressor '+str(j)+' 1st Place %')
            df_columns.append('Regressor '+str(j)+' Voting shares')

        # Convert comparison table to dataframe
        year_comparison = pd.DataFrame(np.copy(year_comparison))

        # Add last column names
        df_columns.append('Real playerId')
        df_columns.append('Real 1st Place %')
        df_columns.append('Real Voting Shares')

        year_comparison.columns = df_columns
        year_comparison.name = int(years_list[i])
        df_comparison.append(year_comparison)

    return df_comparison

def showModelComparison(df_comparison,top=10):
    for i in range(0,len(df_comparison)):
        print(df_comparison[i].name)
        print(df_comparison[i][:top])
        print('')

def saveModelComparison(df_comparison,top=10):
    np_save = np.empty((0,1+len(df_comparison[0].columns)))
    for i in range(0,len(df_comparison)):
        np_aux = df_comparison[i][:top]
        np_year = np.ones((top,1))*df_comparison[i].name
        np_aux = np.hstack((np_year,np_aux))
        np_save = np.vstack((np_save,np_aux))

    col_names = df_comparison[0].columns.values
    col_names = np.insert(col_names,0,'Year')

    df = pd.DataFrame(np_save)
    df.columns = col_names
    df.to_csv('data/testing.csv')
    return

def scoreModelComparison(df_comparison,top,printScore=True):
    top_score = []

    # For first year of the model comparison
    # Extract only playerId columns from single year model comparison (that are already sorted)
    singleYear_df = df_comparison[0]
    playerId_cols = [col for col in singleYear_df.columns if 'playerId' in col]
    singleYear_np = np.array(singleYear_df[playerId_cols])
    
    for i in range(0,len(top)):
        top_score.append(scoreSingleYearModelComparison(singleYear_np,top[i]))

    # For each following year year of the model comparison
    for year in range(1,len(df_comparison)):
        # Extract only playerId columns from single year model comparison (that are already sorted)
        singleYear_df = df_comparison[year]
        playerId_cols = [col for col in singleYear_df.columns if 'playerId' in col]
        singleYear_np = np.array(singleYear_df[playerId_cols])

        for i in range(0,len(top)):
            top_score[i] = np.vstack((top_score[i],scoreSingleYearModelComparison(singleYear_np,top[i])))

    score_matrix = np.zeros((len(top_score[0][0]),len(top_score)))

    for i in range(0,len(top_score)):
        score_matrix[:,i] = np.average(top_score[i],axis=0)

    # score_matrix row corresponds to accuracy of each model
    # score_matrix col corresponds to top n (top 1, top 3, etc)
    return score_matrix

def scoreSingleYearModelComparison(singleYear_np,top):
    # Save model columns in m and real columns in r
    m = singleYear_np[:top,:-1]
    r = singleYear_np[:top,-1]

    # Compare and score
    score = np.isin(m,r).sum(axis=0)

    # return score percentage
    return score/float(top)

def scoreMVP(df_comparison,pos=0):
    list_ret = []

    # Para cada comparación anual
    for i in range(len(df_comparison)):
        # Convertirla a numpy
        np_comparison = np.array(df_comparison[i])

        # Obtener el MVP real
        mvp_real = np_comparison[pos,-3]

        # Fijarse donde está el MVP real en mi predicción
        mvp_predict = np.where(np_comparison[:,0] == mvp_real)[0][0]

        list_ret.append(mvp_predict)

    list_ret = np.array(list_ret)
    unique, counts = np.unique(list_ret, return_counts=True)
    score = np.zeros(10)
    dict_counts = dict(zip(unique, counts))

    for i in range(len(score)):
        score_i = dict_counts.get(i)
        if (score_i != None):
            score[i] = score_i

    return score