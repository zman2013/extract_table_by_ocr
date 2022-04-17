from compute_location import compute_location
from load_image_from_clipboard import load_image_from_clipboard
from api_ocr import recognition
from load_json import local_json
from compute_location import compute_location
from config import today_dir
import os

if __name__ == '__main__':
    filepath = today_dir() + '1.csv'
    image = load_image_from_clipboard()
    recognition(image, filepath)
    df = local_json(filepath)
    df = compute_location(df)
    df.to_csv(os.path.splitext(filepath)[0]+ '.csv', index=False)    
