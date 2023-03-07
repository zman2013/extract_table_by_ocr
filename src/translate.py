import openai
from config import OPENAI_API_KEY

# Load your API key from an environment variable or secret management service
openai.api_key = OPENAI_API_KEY
print(f"api_key: {OPENAI_API_KEY}")

# 定义一个 function，调用 openai 的 api 将文字翻译为简体中文
def translate_to_chinese(text):
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo", 
        messages=[{"role": "user", "content": f"translate the following text into Simplified Chinese:\n\"{text}\""}]
        )
    content = completion.choices[0].message.content
    # content 是个字符串，删除 content 两端的空白字符
    content = content.strip()
    if content.startswith('"') and content.endswith('"'):
        content = content[1:-1]
    return content

if __name__ == '__main__':
    print('start')
    print('#%s#'% translate_to_chinese('負债').strip())
    print('#%s#'% translate_to_chinese('經營租賃負債的即期部分'))