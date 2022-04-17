APP_ID = '25901073'
API_KEY = '9C6Cmu3HY7O7iL5Xpmv0F4aT'
SECRECT_KEY = 'KqPlOS694THHZ02tN9k7j90ojxasELxu'

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
