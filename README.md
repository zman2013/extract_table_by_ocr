# 功能说明
    通过 ocr api 识别图片内容，然后通过 dbscan 算法聚类位置信息，最后生成 csv 表格
# 使用说明
    1. 修改 `src/config.py` 设置 APP_ID\APP_KEY\SECRET_KEY
    2. 使用剪贴板截图表格
    3. 运行 main.py
    4. 在当前目录下查找 data 文件夹下面的 .csv
    5. 预处理利润表
        tesla 利润表：
        1. 在'收入' 子项条目最后 + 'REVENUES'
        2. 在'成本' 子项条目最后 + 'COST'
        3. 在表头添加: 汽车销量
    6. 执行 main2.py directory，可以将 directory 下所有的 csv 文件合并为一个文件，并进行去重相关操作
        a. python src/main2.py data/LI-2015
        b. python src/main2.py data/NIO-9866
        c. python src/main2.py data/xpeng-9868
        d. python src/main2.py data/tesla       // https://ir.tesla.com/#quarterly-disclosure
    7. 执行 main3.py，将理想、蔚来、小鹏、特斯拉的财务报表合并为一个文件
# 模块说明
## load_image_from_clipboard.py
    从剪贴板获取图片内容
## json_to_csv.py
    json 转换为 csv
## dbscan
    通过聚类算法生成 csv 文件
## api_ocr
    调用 ocr api 识别图片内容

# ocr api：
    https://cloud.baidu.com/product/ocr/general
    https://cloud.baidu.com/doc/OCR/s/7kibizyfm#%E9%80%9A%E7%94%A8%E6%96%87%E5%AD%97%E8%AF%86%E5%88%AB%EF%BC%88%E6%A0%87%E5%87%86%E7%89%88%EF%BC%89


# 翻译 prompt
将以下文字翻译成简体中文，以列表形式输出，第一列是原始文字，第二列是简体中文，去掉文字两端的单引号，去掉 nan。

{item list}