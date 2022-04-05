from aip import AipOcr
from config import APP_ID, API_KEY, SECRECT_KEY
import time
import requests
from load_image_from_clipboard import loadImage

client = AipOcr(APP_ID, API_KEY, SECRECT_KEY)
client.setConnectionTimeoutInMillis(30_000)
client.setSocketTimeoutInMillis(30_000)


def asyncRecognitionTable():
    image = loadImage()
    # image.save('somefile.png','PNG')

    res_image = client.tableRecognitionAsync(image)
    print(res_image)
    request_id = res_image['result'][0]['request_id']

    # 获取结果
    options = {}
    options["result_type"] = "excel" # json or excel(default)
    result = client.getTableRecognitionResult(request_id, options)
    # 处理状态是“已完成”，获取下载地址
    while result['result']['ret_msg'] != '已完成':  
        time.sleep(2)  # 暂停2秒再刷新
        result = client.getTableRecognitionResult(request_id)  
    download_url = result['result']['result_data']
    print(download_url)
    # 获取表格数据
    excel_data = requests.get(download_url)
        # 根据图片名字命名表格名称
    xlsx_name = request_id + ".xlsx"  
    # 新建excel文件
    xlsx = open(xlsx_name, 'wb')  
    # 将数据写入excel文件并保存
    xlsx.write(excel_data.content)
    print('finished')

if __name__ == '__main__':
    asyncRecognitionTable()