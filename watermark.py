# coding:utf-8
from PIL import Image, ImageChops
import os


# 为图像嵌入水印
def addWaterMark(pic, mark, marked):
    # 读取载体图像
    img = Image.open(pic).convert("RGB")
    width, height = img.size  # 载体图像大小

    # 读取水印图像
    img_mark = Image.open(mark).convert("RGB")
    img_mark = img_mark.resize((width, height))  # 缩放水印图像大小

    # 处理图像中的源数据
    img = img.point(lambda i: (int(i >> 2)) << 2)
    img_mark = img_mark.point(lambda i: round(i / 85))

    # 将图像数据转化成list
    img_pixels = list(img.getdata())
    mark_pixels = list(img_mark.getdata())

    # 嵌入水印信息
    new_pixels = []
    for index in range(len(img_pixels)):
        # 处理RGB三个通道的分量
        pixel_temp = []
        for i in range(3):
            pixel_temp.append(img_pixels[index][i] + mark_pixels[index][i])
        new_pixels.append(tuple(pixel_temp))

    # 创建新图像
    image_new = Image.new("RGB", (width, height))
    image_new.putdata(data=new_pixels)
    # 保存加水印后的图像
    image_new.save(marked)
    return


# 提取并检测水印, 检测用于测试水印是否成功嵌入
def testWaterMark(pic, mark, decode):
    # 读取已经嵌入水印的图像
    img = Image.open(pic).convert("RGB")
    width, height = img.size  # 读取图像大小

    # 读取原本的水印图像
    img_mark = Image.open(mark).convert("RGB")
    img_mark = img_mark.resize((width, height))  # 缩放水印大小

    # 提取水印
    img_get = img.point(lambda i: (i & 3) * 85)
    # 保存提取出的水印
    img_get.save(decode)
    # 正常应该得到的水印（原始水印先做/85再做*85）
    img_mark = img_mark.point(lambda i: round(i / 85) * 85)

    # 检测水印是否成功嵌入
    print(equal(img_get, img_mark))
    return


# 检测提取出的水印是否和预想中的水印有差别
def equal(im1, im2):
    return ImageChops.difference(im1, im2).getbbox() is None


# 测试用
if __name__ == '__main__':
    print("Please input the path of the picture...")
    pic_path=input()
    name, category = os.path.splitext(pic_path)  # 分解文件扩展名
    pic_path="./static/images/"+pic_path
    marked_path="./static/images/"+name+"_marked.png"
    decode_path = "./static/images/" + name + "_decode.png"
    print("Please input the path of the picture...")
    mark_path = "./static/images/" + input()
    img_mark = Image.open(mark_path).convert("RGB")
    mark_path = "./static/images/" + name + "_mark.png"
    img_mark.save(mark_path)
    addWaterMark(pic_path, mark_path, marked_path)
    testWaterMark(marked_path, mark_path, decode_path)
