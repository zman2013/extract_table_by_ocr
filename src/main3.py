'''
写一个 python function，要有详细的注解。
从一个文件加载 dataframe，命名为 df。
df 有四列，列头包含: '项目'和年份例如: 2022, 2021等。
项目列主要包含财务相关的条目名称，年份列包含对应的财务数据。
可以根据项目列的某一财务条目和年份组合来查询 df 中的数据。

参数: 文件路径，财务条目名称，年份
返回: 财务数据，如果财务数据不存在，返回不存在
'''
import pandas as pd

def load_dataframe(file_path):
    '''
    从文件中加载包含各个财务项和年份的DataFrame
    :param file_path: 文件路径
    :param finance_item: 搜索的财务条目名称(str)
    :param year: 搜索的年份(int)
    :return: 匹配到的财务数据，如果匹配失败，返回 "不存在"
    '''
    # 使用pandas读取csv文件, 命名为df
    df = pd.read_csv(file_path)

    return df

def get_finance_data(df, finance_item, year):
    '''
    :param df: 各个财务项和年份的DataFrame
    :param file_path: 文件路径
    :param finance_item: 搜索的财务条目名称(str)
    :param year: 搜索的年份(int)
    :return: 匹配到的财务数据，如果匹配失败，返回 "不存在"
    '''

    # 查询符合条件的财务数据
    query_result = df[(df['项目'] == finance_item)]

    # 如果结果为空
    if query_result.empty:
        return "不存在"
    else:
        return str(query_result.iloc[0][str(year)])

"""
下面是一组公式: 
    ['毛利总额=收入总额-销售成本总额',
    '单车价格=收入总额/车销量',
    '单车毛利=毛利总额/车销量',
    '毛利=毛利总额/收入总额',
    '销售、一般和管理费用=销售、一般和管理费用',
    '经营利润=毛利总额-营业费用总额',
    '经营利润率=经营利润/收入总额']

具体的数值来自于一个 dataframe，df 有四列，列头包含: '项目'和年份例如: 2022, 2021等。
查询数值的方式是根据项目列的某一财务条目和年份组合来查询 df 中的数据。

请写一个 python function 实现以下的功能:
    先根据公式生成 python 代码，然后执行生成的代码计算数值。

有详细注释。
"""
import pandas as pd
import math

def calculate_financial(formula, df, year):
    """
    根据给定的财务条目和年份，通过公式计算对应指标的结果。

    参数:
        df: pandas.DataFrame 类型，包含以下四列：'项目', '2022', '2021', '2020'
        financial_item: str 类型，要计算的财务条目名称
        year: str 类型，要查询的年份，比如 2022

    返回值:
        计算结果字典。
    """
    
    # 将 df 转换为字典格式方便后续查询
    data_dict = df.set_index('项目')[str(year)].to_dict()
    
    # 拼接公式字符串并执行计算
    for key in data_dict:
        value = data_dict[key]
        
        if type(key) != str and math.isnan(key):
            continue
        if type(value) != str and math.isnan(data_dict[key]):
            continue

        # print(f"key={key}, value={value}")
        value = str(value).replace(',','')
        if value.startswith('-'):
            value = value[1:]
        formula = formula.replace(key, value)

    print(formula)
    try:
        result = eval(formula)
    except Exception as e:
        print(f'计算失败:\n formula: {formula} \n {e}\n')
        return f'计算失败'
    
    
    return result

"""
写一段 python 代码，自动将下面的公式列表中的右侧公式展开，不将公式的内容替换为英文。
展开过程为：
    如果右侧公式中的一个条目为某个左侧条目时，将右侧的条目替换为相同左侧条目对应的右侧条目。
    例如：
    A=B-C
    F=A-D
    最终结果为：
    A=B-C
    F=B-C-D
"""
import re

def expand_formulas(formulas):
    # create a dict to store all left and right sides of the formulas
    formulas_dict = {}
    for formula in formulas:
        print(formula)
        left, right = formula.split("=")
        formulas_dict[left.strip()] = right.strip()

    # expand the formulas by replacing any references to other variables with their actual values
    for idx, formula in enumerate(formulas):
        left, right = formula.split("=")
        for var in re.findall('[\u4e00-\u9fa5a-zA-Z]+', right):
            print(f"var: {var} right: {right}")
            
            if var in formulas_dict:
                # replace the variable with its actual value
                right = right.replace(var, '(' + formulas_dict[var] + ')')
        # formulas[idx] = left + '=' + right
        formulas_dict[left] = right

    return formulas_dict


"""
已知有如下两个方法:
get_finance_data(df, finance_item, year)
calculate_financial(formula, df, year)

计算公式 formulas, formulas 是个 dict，key 是财务条目，value 是计算公式。

请编写一个 python function，可以查询指定财务条目的数据，写清注释。

1. 根据财务条目优先调用 get_finance_data；
2. 如果数据不存在，就找到财务条目的计算公式；
3. 如果找不到计算公式，就返回’不存在，且无计算公式‘；
4. 如果找到计算公式，就调用 calculate_financial 来计算数据。

返回值：
    value 或 '不存在'
"""
def query_finance_data(df, finance_item, year, formulas):
    # 先尝试从 df 中获取财务条目数据
    result = get_finance_data(df, finance_item, year)
    if result != '不存在':
        return result

    # 如果 df 中没有数据，则尝试查找公式并计算
    try:
        formula = formulas[finance_item]
    except KeyError:
        return '不存在'
    
    if finance_item == '研发费用占比':
        pass

    result = calculate_financial(formula, df, year)
    return result


"""
已知有如下方法：
def query_finance_data(df, finance_item, year, formulas)

计算公式 formulas, formulas 是个 dict，key 是财务条目，value 是计算公式。

请编写一个 python function，可以根据财务条目列表查询指定年份的财务数据，写清注释。

参数：dataframe、财务条目列表、年份列表（长度为 n）

执行步骤：
1. 遍历年份列表，选定一个年份
2. 在选定年份的条件下，遍历财务列表
3. 依次对每个财务条目调用 query_finance_data，获得财务数据
4. 最后生成一个 dataframe，包含 n+1 列，第一列是财务条目列表，后面是每一年的财务数据

"""
import pandas as pd

def fetch_finance_data(dataframe, finance_items, years):
    """
    根据财务条目列表查询指定年份的财务数据
    
    参数：
    dataframe：数据源，类型为 pandas.DataFrame，包含至少三列：日期、财务条目、数据。
    finance_items：要查询的财务条目列表。
    years：要查询的年份列表，长度为n。
    
    返回值：
    一个包含 n+1 列的 pandas.DataFrame。
    第一列是财务条目列表，后面是每一年的财务数据，行数等于财务条目列表的长度。

    """
    # 构建结果 DataFrame
    result = pd.DataFrame({"finance_items": finance_items})

    # 遍历年份列表
    for year in years:
        finance_data = []
        # 遍历财务列表
        for finance_item in finance_items:
            # 调用方法 query_finance_data 查询财务数据
            value = query_finance_data(df, finance_item, year, formulas)

            # 如果查询到数据则将其记录到结果中
            finance_data.append(value)

        # 将该年份的财务数据作为新的一列添加到结果 DataFrame 中
        result[str(year)] = finance_data

    return result


	
"""
编写一个 python function 对 dataframe 进行预处理，合并四季度数据到一列。
遍历每一行，遍历每一个 year (来自参数 years):
    1. 如果存在列 '31-Dec-{year}'，就复制单元格到新的一列（名为 {year} );
    2. 如果存在列 'Q1-{year}' or 'Q2-{year}' or	'Q3-{year}' or 'Q4-{year}',
        就将四列的单元格内容转为 float (注意处理异常，打印 log, 并将结果设置为 0),
        然后相加，结果放在新的一列（列名为 {year})

参数：
    df: dataframe 包含多列，其中一列的名称为 '项目'
    years: string array

返回：
    修改之后的 dataframe
"""
import pandas as pd
from typing import List

def preprocess_dataframe(df: pd.DataFrame, years: List[str]) -> pd.DataFrame:
  
    # 检查输入参数是否正确
    if not isinstance(df, pd.DataFrame):
        raise ValueError('The input df is not a DataFrame')
    
    if '项目' not in df.columns:
        raise ValueError("The column '项目' does not exist in the input dataframe")
    
    if not all(isinstance(year, str) for year in years):
        raise ValueError('The input years should be a list of strings')
    
    for year in years:
        # create new column for year if it doesn't exist
        if year not in df.columns:
            df.insert(2, year, pd.NA)

    # 遍历每一行
    for index, row in df.iterrows():
        for year in years:
            
            # 检查列'31-Dec-{year}'是否存在，如果存在就复制单元格到新的一列（名为 {year} ）
            if f'31-Dec-{year[-2:]}' in df.columns and not pd.isna(row[f'31-Dec-{year[-2:]}']):
                df.loc[index, year] = row[f'31-Dec-{year[-2:]}']
            
            # 检查列 'Q1-{year}' or 'Q2-{year}' or	'Q3-{year}' or 'Q4-{year}' 是否存在
            elif any(f'Q{i}-{year}' in df.columns for i in range(1,5)):
                q_total = 0
                
                # 将四列的单元格内容转为 float ，并相加
                for i in range(1,5):
                    col_name = f'Q{i}-{year}'
                    if col_name in row.index:
                        value = row[col_name]
                        if isinstance(value, str):
                            try:
                                value = float(value.replace(',', ''))
                            except ValueError:
                                print(f'Error converting to float. Setting value to 0. row={index}, col={col_name}, {value}')
                                value = 0
                        elif isinstance(value, (int, float)):
                            pass
                        else:
                            print(f'Invalid type in column {col_name}. Setting value to 0. row={index}')
                            value = 0
                        q_total += value
                
                # 将结果放在新的一列（列名为 {year}），如果已经有值就不再设置新的值
                if pd.isna(row[year]):
                    df.loc[index, year] = q_total
    
    return df

formulas = [
    '单车价格=车辆销售收入/汽车销量',
    '车辆利润=车辆销售收入-车辆销售成本',
    '单车毛利=车辆利润/汽车销量',
    '毛利总额=收入总额-销售成本总额',
    '毛利率=毛利总额/收入总额',
    '经营利润=毛利总额-营业费用总额',
    '经营利润率=经营利润/收入总额',
    '研发费用占比=研发费用/收入总额',
    '销售、一般和管理费用占比=销售、一般和管理费用/收入总额',
    '流动资金=应收账款+存货+预付款项及其他流动资产-应付账款和应付票据-应付关联方款项-递延收益，流动-经营租赁负债，流动-预提费用及其他流动负债',
    '物业厂房机器等=房地产、厂房和设备净值+经营租赁权资产净值',
    '营运资产=流动资金+物业厂房机器等+无形资产净额',
    '净现金和短期可变现资产=现金及现金等价物+受限制现金+定期存款和短期投资',
    '需时间变现的投资性资产=0',
    '非营运资产=净现金和短期可变现资产+需时间变现的投资性资产+长期投资',
    '无形资产=无形资产净额'
    ]
formulas = expand_formulas(formulas)
print(formulas)


finance_items = [
'营运资产',
'流动资金',
'物业厂房机器等',
'无形资产',
'非营运资产',
'净现金和短期可变现资产',
'需时间变现的投资性资产',
'长期投资',
'其他非营运资产及债务',
'汽车销量',
'收入',
'车辆销售收入',
'其他销售和服务收入',
'收入总额',
'销售成本',
'车辆销售成本',
'其他销售和服务成本',
'销售成本总额',
'毛利总额',
'单车价格',
'单车毛利',
'毛利率',
'研发费用',
'研发费用占比',
'销售、一般和管理费用',
'销售、一般和管理费用占比',
'营业费用总额',
'经营利润',
'经营利润率',
'存货',
'人员',
'研发人员',
'生产人员',
'销售和营销人员',
'一般和行政管理人员',
'总计人员',
'门店',
'销售城市',
'零售中心',
'维修城市',
'维修中心及钣喷中心'
]

df = pd.read_csv('./data/xpeng-9868/xpeng-9868.finance.csv')
df = fetch_finance_data(df, finance_items, [2021, 2022])
xp_df = df.rename(columns={'2021':'xp-2021', '2022': 'xp-2022'})

df = pd.read_csv('./data/NIO-9866/NIO-9866.finance.csv')
df = fetch_finance_data(df, finance_items, [2021, 2022])
nio_df = df.rename(columns={'2021':'nio-2021', '2022': 'nio-2022'})

df = pd.read_csv('./data/LI-2015/LI-2015.finance.csv')
df = fetch_finance_data(df, finance_items, [2021, 2022])
li_df = df.rename(columns={'2021':'li-2021', '2022': 'li-2022'})

df = pd.read_csv('./data/tesla/tesla.finance.csv')
df = preprocess_dataframe(df, ['2021', '2022'])
df = fetch_finance_data(df, finance_items, ['2021', '2022'])
tesla_df = df.rename(columns={'2021':'tesla-2021', '2022': 'tesla-2022'})

df = pd.merge(xp_df, nio_df, on='finance_items')
df = pd.merge(df, li_df, on='finance_items')
df = pd.merge(df, tesla_df, on='finance_items')

# 保存更新后的 dataframe 到 csv 文件
df.to_csv('./data/finance.csv', index=False)
