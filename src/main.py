from compute_location import compute_location
from load_image_from_clipboard import load_image_from_clipboard
from api_ocr import recognition
from load_json import local_json
from compute_location import compute_location
from config import today_dir
import os
import time

if __name__ == '__main__':
    timestr = time.strftime('%H:%M:%S', time.localtime(time.time()))
    filepath = today_dir() + timestr + '.json'
    image = load_image_from_clipboard()
    recognition(image, filepath)
    df = local_json(filepath)
    df = compute_location(df)
    df.to_csv(os.path.splitext(filepath)[0]+ '.csv', index=False)    
