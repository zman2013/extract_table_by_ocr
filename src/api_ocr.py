from aip import AipOcr
from config import APP_ID, API_KEY, SECRECT_KEY, today_dir


client = AipOcr(APP_ID, API_KEY, SECRECT_KEY)
client.setConnectionTimeoutInMillis(30_000)
client.setSocketTimeoutInMillis(30_000)


import json
def recognition(image, filepath):

    print('invoke aipOcr')
    res_image = client.accurate(image)
    print('result: %s' % res_image)

    print('write to file')
    with open(filepath, 'w') as file:
        file.write(json.dumps(res_image))
    print('finished')
    

if __name__ == '__main__':
    recognition(today_dir()+"1.json")