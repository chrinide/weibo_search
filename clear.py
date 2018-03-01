# coding: utf-8
# 17-10-6, created by tuitu

# 验证码图片降噪
from PIL import Image,ImageDraw

from PIL import Image,ImageDraw,ImageChops
import os

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

def cut_one_char(image):
    # 再次降噪
    # N = 4
    # clear_noise(image,4)

    CharWidth=25
    CharHeight=26
    Width,Height=image.size
    # 找出image上出现黑点的第一列
    x = find_first_column(image)

    # 第一行
    # 左上右下,左 <= x < 右
    box = (x,0,x+CharWidth,Height)
    image2 = crop_white(image,box)
    y = find_first_row(image2)

    # 切割出一个字符
    box = (x,y,x+CharWidth,y+CharHeight)
    image_char = crop_white(image,box)

    # 剩下的图片
    if x+CharWidth > Width:
        image_residue = None
    else:
        box = (x+CharWidth,0,Width,Height)
        image_residue = crop_white(image,box)
    return [image_char,image_residue]

# 没有字符W的情况下,切割的都比较好.
# 出现W的概率为1-(1-1/36)^4≈10.66%
# 这样一来准确率无法超过90%
# 这里处理4个字符的情况
def cut_all_char(image):
    image_char1,image = cut_one_char(image)
    image_char2,image = cut_one_char(image)
    image_char3,image = cut_one_char(image)
    image_char4,image = cut_one_char(image)
    return [image_char1,image_char2,image_char3,image_char4]

# 如果box超出原图范围,默认会以黑色填充
# 因此为了让图片超出部分以白色填充,进行反色处理,最后再反色回来
def crop_white(image,box):
    # 255 - old
    image = ImageChops.invert(image)
    image = image.crop(box)
    return ImageChops.invert(image)

# 找出image上出现黑点的第一列
def find_first_column(image):
    Width,Height=image.size
    for x in range(Width):
        for y in range(Height):
            if image.getpixel( (x,y) ) == 0:
                return x
    # 如果没有黑点,返回第一列
    return 0

# 找出image上出现黑点的第一行
def find_first_row(image):
    Width,Height=image.size
    for y in range(Height):
        for x in range(Width):
            if image.getpixel( (x,y) ) == 0:
                return y
    # 如果没有黑点,返回第一行
    return 0
