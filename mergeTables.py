# Import libraries
import pandas as pd

# Function that merges n tables based on index
def mergeTables(tables,repeat_columns=False):
    df = tables[0]
    for i in range(1,len(tables)):
        df2 = tables[i]

        if (repeat_columns):
            cols_to_use = df2.columns
        else:
            cols_to_use = df2.columns.difference(df.columns)

        df = pd.merge(df,df2[cols_to_use],how='left',left_index=True,right_index=True)
    return df