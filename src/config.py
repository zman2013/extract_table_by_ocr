APP_ID = ''
API_KEY = ''
SECRECT_KEY = ''

root_dir = './data/'
import datetime
import os
def today_dir():
    today = datetime.datetime.today().date()
    date_format = today.strftime('%Y%m%d')
    dir = root_dir + date_format + "/"
    if not os.path.exists(dir):
        os.makedirs(dir)
    return dir
