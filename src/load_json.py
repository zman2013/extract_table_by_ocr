import json 
import pandas as pd
import os

# 读取 json 返回 df
def load_json(filepath):
    with open(filepath) as json_file:
        data = json.load(json_file)

        words_result = data['words_result']

        list = []
        for word in words_result:
            list.append([word['words'], 
                word['location']['top'],
                word['location']['left'],
                word['location']['width'],
                word['location']['height'],
                ])

        df = pd.DataFrame(list, columns=['words', 'top', 'left', 'width', 'height'])
        return df
        df.to_csv(os.path.splitext(filepath)[0] + '.csv', index=False)