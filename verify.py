# coding: utf-8
# 17-10-5, created by tuitu
import requests
import pytesseract
import io
from PIL import Image,ImageEnhance

src = 'http://s.weibo.com' + '/ajax/pincode/pin?type=sass&ts=1507213207'
raw_img = requests.get(src).content
data_stream = io.BytesIO(raw_img)
image = Image.open(data_stream)
image.show()
# imgry = image.convert('L')#图像加强，二值化
# sharpness =ImageEnhance.Contrast(imgry)#对比度增强
# sharp_img = sharpness.enhance(2.0)
vcode = pytesseract.image_to_string(image, lang="eng", config="-psm 7 validcode")
print("vcode:", vcode)
