# Import libraries
import pandas as pd
from sklearn.preprocessing import MinMaxScaler

def normalizeTable(df,type='minmax'):
    # Convert all table elements to float
    df = df.astype(float)

    if(type == 'minmax'):
        scaler = MinMaxScaler()
        df_normalized = pd.DataFrame(scaler.fit_transform(df), columns=df.columns,index=df.index)
    return df_normalized