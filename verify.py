# coding: utf-8
# 17-10-5, created by tuitu

# 验证码破解
import io
import pytesseract
import requests
from PIL import Image, ImageDraw
from PIL import ImageEnhance, ImageFilter
from matplotlib import pyplot as plt
# import cnn

from clear import cut_all_char


def getPixel(image,x,y,G,N):
    L = image.getpixel((x,y))
    if L > G:
        L = True
    else:
        L = False

    nearDots = 0
    if L == (image.getpixel((x - 1,y - 1)) > G):
        nearDots += 1
    if L == (image.getpixel((x - 1,y)) > G):
        nearDots += 1
    if L == (image.getpixel((x - 1,y + 1)) > G):
        nearDots += 1
    if L == (image.getpixel((x,y - 1)) > G):
        nearDots += 1
    if L == (image.getpixel((x,y + 1)) > G):
        nearDots += 1
    if L == (image.getpixel((x + 1,y - 1)) > G):
        nearDots += 1
    if L == (image.getpixel((x + 1,y)) > G):
        nearDots += 1
    if L == (image.getpixel((x + 1,y + 1)) > G):
        nearDots += 1

    if nearDots < N:
        return image.getpixel((x,y-1))
    else:
        return None

    # 降噪
# 根据一个点A的RGB值，与周围的8个点的RBG值比较，设定一个值N（0 <N <8），当A的RGB值与周围8个点的RGB相等数小于N时，此点为噪点
# G: Integer 图像二值化阀值
# N: Integer 降噪率 0 <N <8
# Z: Integer 降噪次数
# 输出
#  0：降噪成功
#  1：降噪失败
def clearNoise(image,G,N,Z):
    draw = ImageDraw.Draw(image)

    for i in range(0,Z):
        for x in range(1,image.size[0] - 1):
            for y in range(1,image.size[1] - 1):
                color = getPixel(image,x,y,G,N)
                if color != None:
                    draw.point((x,y),color)

def handle(img, limit):

    # 灰度
    draw = ImageDraw.Draw(img)
    x, y = img.size
    for m in range(0, x):
        for n in range(0, y):
            if img.getpixel((m, n)) <= limit:
                draw.point((m, n), 1)
            else:
                draw.point((m, n), 255)

def emtpy(img, limit):
    # 灰度
    draw = ImageDraw.Draw(img)
    x, y = img.size
    for m in range(0, x):
        for n in range(0, y):
            if img.getpixel((m, n)) <= limit:
                draw.point((m, n), 255)
            else:
                draw.point((m, n), img.getpixel((m, n)))
fig = plt.figure()

# src = 'http://s.weibo.com' + '/ajax/pincode/pin?type=sass&ts=1507213207'
src = 'http://202.119.113.147/validateCodeAction.do?random=0.5122132709851999'

# 获得图片
raw_img = requests.get(src).content
data_stream = io.BytesIO(raw_img)

# image, 原始图片
image = Image.open(data_stream)
ax = fig.add_subplot(221)
ax.imshow(image)


imgry = image.convert('L')#图像加强，二值化
sharpness =ImageEnhance.Contrast(imgry)#对比度增强
sharp_img = sharpness.enhance(2.0)
clearNoise(sharp_img, 50, 1, 1)
ax = fig.add_subplot(222)
# sharp_img, 降噪图片
ax.imshow(sharp_img)


handle(sharp_img, 80)
ax = fig.add_subplot(223)
x = sharp_img
# x, 二值化图片
x.save('hello.png')
ax.imshow(x)

# z, 边缘增强图片
z = x.filter(ImageFilter.SMOOTH )
# z = z.filter(ImageFilter.EDGE_ENHANCE_MORE)
# handle(z, 200)
emtpy(z, 50)
ax = fig.add_subplot(224)
ax.imshow(z)

imgs = [image, sharp_img, x, z]

# 不指定语言
for i in imgs:
    vcode = pytesseract.image_to_string(i, config="--oem 0 -psm 7 ~/Python/weibo/validcode")
    print("vcode:", vcode, end='  ')
print('-------------------')

# 指定语言
for i in imgs:
    vcode = pytesseract.image_to_string(i, config="--oem 0 -psm 7 ~/Python/weibo/validcode")
    print("vcode:", vcode, end='  ')
print('-------------------')

# 不指定语言, 神经网络引擎
for i in imgs:
    vcode = pytesseract.image_to_string(i,config="--oem 1 -psm 7 ~/Python/weibo/validcode")
    print("vcode:", vcode, end='  ')
print('-------------------')

# 不指定语言, 混合引擎
for i in imgs:
    vcode = pytesseract.image_to_string(i,config="--oem 2 -psm 7 ~/Python/weibo/validcode")
    print("vcode:", vcode, end='  ')
print('-------------------')

vcode = cnn.detect(z)
print("vcode:", vcode, end='  ')
print('-------------------')
plt.show()
plt.close()
# z.save('hello.png')
# chars = cut_all_char(x)
#
# cs = plt.figure()
# i = 1
# x.show()
# for c in chars:
#     plane = cs.add_subplot(int(str(22) + str(i)))
#     plane.imshow(c)
#     i += 1
#
# plt.show()