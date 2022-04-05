import json 
import pandas as pd

list = []
with open('data/example1.json') as json_file:
    data = json.load(json_file)

    words_result = data['words_result']

    for word in words_result:
        list.append([word['words'], 
            word['location']['top'],
            word['location']['left'],
            word['location']['width'],
            word['location']['height'],
            ])

    df = pd.DataFrame(list, columns=['words', 'top', 'left', 'width', 'height'])
    df.to_csv('data/example1.csv', index=False)