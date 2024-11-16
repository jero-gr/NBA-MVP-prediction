# Import libraries
import pandas as pd
from sklearn.preprocessing import MinMaxScaler

def normalizeTable(df,type='max'):
    # Convert all table elements to float
    df = df.astype(float)

    # 1 es el máximo de cada columna, 0 es 0
    if(type == 'max'):
        df_normalized = df / df.max()
    
    # 1 es el máximo de cada columna, 0 es el mínimo de cada columna
    if(type == 'minmax'):
        scaler = MinMaxScaler()
        df_normalized = pd.DataFrame(scaler.fit_transform(df), columns=df.columns,index=df.index)

    return df_normalized