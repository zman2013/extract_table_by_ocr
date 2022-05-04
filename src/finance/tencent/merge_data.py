from operator import index

import sys
import os
DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
sys.path.insert(0, DIR)
print(DIR)
from config import today_dir
import pandas as pd

if __name__ == '__main__':
    file_names = ['cost_category.csv', 
        'income_category.csv', 
        'active_user.csv',
        'employee.csv']
    dir = today_dir()

    merged_df = pd.DataFrame({})
    for file_name in file_names:
        file_path = os.path.join(dir, file_name)
        df = pd.read_csv(file_path, index_col=0)
        merged_df = merged_df.append(df)
    
    print(merged_df)
    merged_df.to_csv(os.path.join(dir, os.path.splitext(os.path.basename(__file__))[0]+'.csv'))

