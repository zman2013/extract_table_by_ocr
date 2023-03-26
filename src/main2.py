import os

# This function returns a list of all files located in the given directory path 
# and its subdirectories 
def list_files(directory):
    # Initialize an empty list to store the file paths
    file_list = []
    
    # Recursively search for files in the given directory and its subdirectories using the os.walk() method
    for root, dirs, files in os.walk(directory):
        # Iterate over each file in the current directory level and append its full path to the list
        for name in files:
            file_list.append(os.path.join(root, name))
    
    # Return the final list of file paths
    return file_list

import pandas as pd
# 写一个 function，参数是文件路径列表，加载其中 .csv 格式的文件数据，存储在 dataframe 中
# 写好注释
def load_csv_files(file_list):
    """
    读取文件路径列表中CSV格式的文件，将数据存储在一个DataFrame对象中
    
    参数:
        file_list: 文件路径列表
        
    返回:
        DataFrame: 所有CSV文件的数据以及其它类型文件被忽略，返回一个DataFrame对象
    """
    # 创建一个空的 Pandas DataFrame 对象
    df = pd.DataFrame()
    
    for file_path in file_list:
        # 检查文件是否是CSV格式，并且过滤掉文件 finance.csv 
        if not file_path.endswith('.csv') or 'finance.csv' in os.path.basename(file_path):
            continue
        
        # 读取文件，并将内容添加到 DataFrame 中
        print('file_path %s', file_path)
        df_temp = pd.read_csv(file_path)    # 检查文件是否为空，如果为空抛出异常，异常中包含文件名
        if df_temp.empty:
            print(f"{file_path} is empty. SKIP")
            
        for index, row in df_temp.iterrows():
            val = row[0]
            if isinstance(val, str) and (val.endswith(':') or val.endswith('：')):
                # 去掉结尾的字符
                df_temp.iat[index, 0] = val[:-1]
        
        df = pd.concat([df, df_temp], ignore_index=True)
    
    return df

# 写一个 python function，参数是 dataframe 和 文件路径
# 判断文件是否为 csv 格式，如果不是 csv 格式抛出异常
# 否则加载文件内容，并将 dataframe 的数据也添加到文件中
# 并对同一列相同的行进行合并
# 写好注释
def add_dataframe_to_csv(dataframe, file_path):
    """
    This function loads data from a csv file and a dataframe. Merges rows with same value in a certain column.
    
    Args:
    - dataframe: pandas DataFrame object
    - file_path: str, file path of the csv file to be loaded
    
    Returns:
    - None
    
    Raises:
    - ValueError: if the file extension is not csv
    
    """
    # 检查文件是否为 csv 格式
    if file_path.endswith('.csv') == False:
        raise ValueError("Only csv files are accepted")

    # 检查文件 file_path 是否为空
    # 如果为空，打印日志，并创建空的 DataFrame
    # 如果不为空，加载文件内容到 df 中
    if os.path.getsize(file_path) > 0:
        df = pd.read_csv(file_path)
    else:
        print(f"File {file_path} is empty. Init a DataFrame object.")
        df = pd.DataFrame()

    # 将传入的 dataframe 添加到已有数据中
    df=df.append(dataframe)

    # dataframe 去重
    # 如果不同行第一列的内容一样，进行去重
    df.drop_duplicates(subset=df.columns[0], keep='last', inplace=True)

    # 保存更新后的 dataframe 到 csv 文件
    df.to_csv(file_path, index=False)


# 写一个 python main 接收两个命令行参数，分别是文件夹路径和文件路径
# 其中文件夹路径必选，文件路径可选
# 如果文件路径参数不存在，就在文件夹下创建文件，名文:finance.csv
import sys
import os

def main(directory_path, dictionary, file_path=None):
    """
    A function that takes a directory path and an optional file path as arguments.
    If the file path argument is not given, it creates a CSV file named finance.csv in the directory path.
    If the file path argument is given, it checks if the file is in CSV format. If it's not, it raises an exception.
    If it's a CSV file, it loads its content, adds the data to the dataframe along with the existing data and merges the rows with same column value.

    Parameters:
    directory_path (str): Path of the directory where the csv file will be created or updated.
    file_path (str, optional): Path of the csv file to update. Defaults to None.

    Returns:
    None
    """

    # If file path is not provided, create a finance.csv file in the directory
    if file_path is None:
        last_folder_name = os.path.basename(os.path.normpath(directory_path))
        file_path = os.path.join(directory_path, last_folder_name+'.finance.csv')

        if not os.path.exists(file_path):
            with open(file_path, 'w') as f:
                pass

    file_list = list_files(directory_path)
    df = load_csv_files(file_list)
    # 翻译财报条目为简体中文
    [df, missed_keys] = translate_to_simplified_chinese(df, dictionary)
    print(f"未能翻译的条目如下: \n\n")
    for key in missed_keys:
        print(key)
    add_dataframe_to_csv(df, file_path)

# prompt: 定义一个 function，参数是: dataframe，dictionary。
# dictionary 是个 key/value 的map。
# dataframe 第一列的内容是字符串，遍历第一列所有的单元，将单元内容作为 key，查询 dictionary 中的值 value。
# 如果 value 不存在，就使用默认值 N/A。
# 最后将 value 作为第二列插入到 dataframe 中。
## 将第一列翻译为简体中文（美股、港股的财报都不是简体中文的）
## 翻译为简体中文，可以统一术语
def translate_to_simplified_chinese(dataframe, dictionary, default_value='N/A'):
    """
    This function takes a dataframe and a dictionary as parameters. The dictionary is a key/value map.
    The first column of the dataframe contains strings. For each cell in the first column, this function
    will use its contents as a key to look up the corresponding value in the dictionary. If the value does
    not exist in the dictionary, then the default value specified (which defaults to 'N/A') will be used
    instead. The resulting values will be added as a new column to the dataframe.
    """
    new_column = []
    missed_keys = []
    for _index, row in dataframe.iterrows():
        key = row[0]
        if key in dictionary:
            value = dictionary[key]
        else:
            value = default_value
            missed_keys.append(key)
            
        new_column.append(value)
    dataframe.insert(1, '项目', new_column)
    return [dataframe, missed_keys]


from dictionary import load_data_from_file 

if __name__ == "__main__":
    try:
#        directory_path = sys.argv[1]
        directory_path = 'data/tesla'
        file_path = sys.argv[2] if len(sys.argv) > 2 else None
        print("start")
        dictionary = load_data_from_file('src/dictionary.dict')
        main(directory_path, dictionary, file_path)
    except Exception as e:
        # 打印详细的堆栈信息
        import traceback
        print(traceback.format_exc())
        print("Usage: python script.py [directory_path] [file_path]")
