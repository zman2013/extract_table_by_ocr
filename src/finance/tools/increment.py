from operator import index

import sys
import os
DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
sys.path.insert(0, DIR)
print(DIR)
from config import today_dir
import pandas as pd
import numpy as np
import traceback

def f(x):
    try:
        
        return float(x)
    except Exception as e:
        traceback.print_exc()
        return x

if __name__ == '__main__':
    file_name = 'merge_data.csv'
    file_path = os.path.join(today_dir(), file_name)
    df = pd.read_csv(file_path, index_col=0)
    df_pct = pd.DataFrame({})
    for index, row in df.iterrows():
        row_float = row.str.replace(',', '').astype(float)
        df_pct = df_pct.append(row_float)
    # df.iloc[0].str.replace(',', '').astype(float) #.select_dtypes(include=['float64']) #.pct_change(axis='columns', periods=-1)
    df_pct = df_pct.pct_change(axis='columns', periods=-1)
    
    for index, row in df_pct.iterrows():
        print(index)
        # df_pct.style.format({
        #     str(column): "{:.1}%"
        # })
        row = row.map("{:.1%}".format)
        # data = [index+'%']
        # for v in row.tolist():
        #     data.append(v)
        df_pct.loc[str(index)+'%'] = row
        df_pct = df_pct.drop(index=index)
    df_pct = df_pct.append(df)
    df_pct = df_pct.sort_index()
    print(df_pct)
    df_pct.to_csv(os.path.join(today_dir(), os.path.splitext(os.path.basename(__file__))[0]+'.csv'))
    