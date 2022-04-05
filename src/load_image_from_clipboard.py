from PIL import ImageGrab
import os

# 从剪贴板获取图片内容
def loadImage():
    tmp_image_path = 'tmp.png'
    im = ImageGrab.grabclipboard()
    # Encode your PIL Image as a JPEG without writing to disk
    # buffer = io.BytesIO()
    # im.save(buffer, format='JPEG', quality=75)
    # return buffer.getbuffer()

    im.save(tmp_image_path,'PNG')
    img_open = open(tmp_image_path, 'rb')
    # 读取图片
    img_read = img_open.read()
    # 删除图片
    os.remove(tmp_image_path)

    return img_read
