import pandas as pd
from sklearn.cluster import DBSCAN

# 按 ${column_name} 进行聚类，返回的 df 包含聚类后的 column
def cluster(df, column_name='', eps=5, min_samples=1):
    X = df[[column_name]]

    db = DBSCAN(eps=eps, min_samples=min_samples).fit(X)

    df[column_name+'_cluster_db'] = db.labels_
    # df = df.sort_values(['cluster_db', column_name])

    # df.to_csv('data/example1.result.csv', index=False)

    # import numpy
    # labels = numpy.unique(df['cluster_db'].values)

    # import matplotlib.pyplot as plt
    # from matplotlib import colors as mcolors
    # colors = []
    # for color in mcolors.CSS4_COLORS:
    #     colors.append(color)

    # pd.plotting.scatter_matrix(df, figsize=(14, 8), s=100)
    # plt.show()

    return df
    print(df)
    print(df.groupby('cluster_db').mean())


# 合并’左、右‘两个维度的集群，同一个元素归属归属于那个较大的集群
# 例：word1
#   按’左‘维度，归属于集群 left_0，该集群元素个数为 4
#   按’右‘维度，归属于集群 right_0，该集群元素个数为 1
#   则 word1 归属于’左‘集群
#   设置 left_right_combine_cluster_db = combine_cluster_db_index ++
def combine_left_right_labels(df):
    left_groups = df.groupby('left_cluster_db').groups
    right_groups = df.groupby('right_cluster_db').groups
    # label -> combine_cluster_db
    # 例：{left_0 : 0, right_0 : 1}
    label_cluster_db_mapping = {}
    combine_cluster_db_index = 0
    combine_cluster_db_column = []
    for _, line in df.iterrows():
        left_cluster_db = line['left_cluster_db']
        right_cluster_db = line['right_cluster_db']
        left_group = left_groups[left_cluster_db]
        right_group = right_groups[right_cluster_db]

        if len(left_group) > len(right_group):
            label = 'left_'+str(left_cluster_db)
        else:
            label = 'right_'+str(right_cluster_db)

        if label_cluster_db_mapping.__contains__(label) == False:
            label_cluster_db_mapping[label] = combine_cluster_db_index
            combine_cluster_db_index += 1
        combine_cluster_db_column.append(label_cluster_db_mapping.get(label))
    df['left_right_combine_cluster_db'] = combine_cluster_db_column
    return df

import os
# 计算字段的归属位置，然后返回 df
def compute_location(df):

    # df = pd.read_csv(filepath)
    df = cluster(df, 'top')
    df = cluster(df, 'left', eps=30, min_samples=1)
    df['right'] = df['left'] + df['width']
    df = cluster(df, 'right', eps=10, min_samples=1)

    df = combine_left_right_labels(df)

# {
#   top_cluster : {
#     left_cluster : {
#       words: ${words},
#       left: ${left}
#     }
#   }
# }
    pre_data = {}
    for _, row in df.iterrows():
        top_cluster = row['top_cluster_db']
        left_cluster = row['left_right_combine_cluster_db']
        pre_data.setdefault(top_cluster, {})
        pre_data[top_cluster].setdefault(left_cluster, {})
        pre_data[top_cluster][left_cluster] = {
            "words" : row['words'],
            "left" : row['left']
        }

    column_count = 30
    column_name_initial_value = 1_000_000_000
    columns = [i for i in range(column_name_initial_value, column_name_initial_value+column_count)]
    data = []
    for _, value in pre_data.items():
        list = [''] * column_count
        for k, v in value.items():
            list[k] = v['words']
            columns[k] = v['left']   # 选用最后一行的左坐标，开头几行是文字标题坐标不太合适，比如：(人民幣百萬元，另有指明者除外)
        data.append(list)

    df = pd.DataFrame(data, columns=columns)

#   删除没有用到的 columns
    columns_drop = []
    for column_name in df.columns.values.tolist():
        if column_name >= column_name_initial_value:
            columns_drop.append(column_name)
    df = df.drop(columns_drop, axis=1)

#   按 column name 大小排序
    df = df.reindex(sorted(df.columns), axis=1)
    return df
    df.to_csv(os.path.splitext(filepath)[0] + '.result.csv', index=False)


from config import today_dir
import os
from load_json import load_json
if __name__ == '__main__':
    dir = os.path.join(today_dir(), 'tencent', 'active_user')
    for dir_path, dir_list, file_name_list in os.walk(dir):
        for file_name in file_name_list:
            file_path = os.path.join(dir_path, file_name)
            if os.path.splitext(file_path)[1] == '.json':
                print(f'process {file_path}')
                df = load_json(file_path)
                df = compute_location(df)
                df.to_csv(os.path.splitext(file_path)[0]+ '.csv', index=False)  