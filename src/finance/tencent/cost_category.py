# 遍历文件夹
# 加载 csv
# 查看是否有 index = 收入總额
# 获取指定行、从指定单元格获取时间
# 添加到汇总的 dataframe

number_mapping = {
    '零': '0',
    '一': '1',
    '二': '2',
    '三': '3',
    '四': '4',
    '五': '5',
    '六': '6',
    '七': '7',
    '八': '8',
    '九': '9',
    '年': ''
}
def convert_chinese_year(year):
    for char in year:
        year = year.replace(char, number_mapping[char])
    return int(year)

if __name__ == '__main__':
    import sys
    import os
    DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
    sys.path.insert(0, DIR)
    print(DIR)

    import pandas as pd
    import re
    
    from config import today_dir

    merge_json = {}
    years = []
    for dir, sub_dirs, file_names in os.walk(today_dir()):
        for file_name in file_names:
            file_path = os.path.join(dir, file_name)
            if os.path.splitext(file_path)[1] == '.csv':
                print(f'process {file_path}')
                df = pd.read_csv(file_path)
                first_column = df.iloc[:,0].tolist()
                if '收入成本總额' in first_column:  
                    print(f'good')
                    year = df.iloc[1, 2]
                    year = convert_chinese_year(year)
                    if not years.__contains__(year):
                        years.append(year)
                    # merge_df[year] = '0'
                    for _, row in df.iterrows():
                        label = row[0] # 增值服務/網絡廣告/..
                        label = re.sub('[\(\d\)*]', '', label) # 去掉(1), (2), ..
                        if label != '0' and label != '':
                            label = label + '_成本'
                            if label not in merge_json:
                                merge_json[label] = {}
                            merge_json[label][year] = row[1]
    # 转为 dataframe
    years.sort()
    years.sort(reverse=True)
    column_names = [0]
    for year in years:
        column_names.append(year)
    data = []
    for k, v in merge_json.items():
        row = [k]
        for year in years:
            if v.__contains__(year):
                row.append(v[year])
            else:
                row.append(0)
        data.append(row)
    df = pd.DataFrame(data, columns=column_names)
    file_name = os.path.splitext(os.path.basename(__file__))[0]
    df.to_csv(os.path.join(today_dir(), file_name + '.csv'), index=False)
                            

                