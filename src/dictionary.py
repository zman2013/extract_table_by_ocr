# 创建一个初始化 function, 初始化一个 map，里面初始化一对 (key, value)
def init_map(key, value):
    my_map = {key: value}
    return my_map

# prompt: 创建一个方法，将 map 保存到文件中
def save_map_to_file(map_obj, file_path):
    """
    This method saves a dictionary object to a file.
    :param map_obj: The map or dictionary object to be saved.
    :param file_path: The path and filename where the data is to be saved.
    :return: None
    """
    try:
        with open(file_path, 'w') as file:
            for key, value in map_obj.items():
                file.write(f"{key}: {value}\n")
        print("Data saved successfully!")
    except Exception as e:
        print(f"Error saving data to file: {str(e)}")

# prompt: 创建一个 function，从文件中加载数据到 map 中，并返回 map
def load_data_from_file(file_path):
    data_map = {}
    try:
        with open(file_path, 'r') as file:
            for line in file:
                key, value = line.split(":") # assuming each line has format "key:value"
                data_map[key.strip()] = value.strip()
    except FileNotFoundError:
        return data_map
    else:
        return data_map

# prompt：创建一个 function，从 map 查询 key 对应的 value，如果不存在返回 None。写好注解
def get_value_from_map(key: str, my_map: dict) -> str or None:
    """
    从map查询对应key的value，如果不存在返回None

    :param key: 要查询的键值
    :type key: str
    :param my_map: 查询的map
    :type my_map: dict
    :return: 查询到返回对应的value，否则返回None
    :rtype: str or None
    """
    
    if key in my_map:
        return my_map[key]
    else:
        return None