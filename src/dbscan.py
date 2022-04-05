import pandas as pd
from sklearn.cluster import DBSCAN



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


filepath = 'data/example1.csv'
df = pd.read_csv(filepath)
df = cluster(df, 'top')
df = cluster(df, 'left', eps=100, min_samples=5)



pre_data = {}
for index, row in df.iterrows():
    top_cluster = row['top_cluster_db']
    left_cluster = row['left_cluster_db']
    pre_data.setdefault(top_cluster, {})
    pre_data[top_cluster].setdefault(left_cluster, {})
    pre_data[top_cluster][left_cluster] = row['words']

data = []
for key, value in pre_data.items():
    list = [0] * 4
    for k, v in value.items():
        list[k] = v
    data.append(list)

df = pd.DataFrame(data)
df.to_csv('data/example1.result.csv', index=False)
