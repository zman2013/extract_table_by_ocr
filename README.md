# 功能说明
    通过 ocr api 识别图片内容，然后通过 dbscan 算法聚类位置信息，最后生成 csv 表格
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