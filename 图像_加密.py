from PIL import Image

def plus(str):
    # 返回指定长度的字符串，原字符串右对齐，前面填充0。
    return str.zfill(8)

def getCode(img):
    str = ""
    # 获取到水印的宽和高进行遍历
    for i in range(img.size[0]):
        for j in range(img.size[1]):
            # 获取水印的每个像素值
            rgb = img.getpixel((i, j))
            # 将像素值转为二进制后保存
            str = str + plus(bin(rgb[0]).replace('0b', ''))
            str = str + plus(bin(rgb[1]).replace('0b', ''))
            str = str + plus(bin(rgb[2]).replace('0b', ''))
    return str

def encry(img, code):
    # 计数
    count = 0
    # 二进制像素值的长度，可以认为要写入图像的文本长度，提取（解密）时也需要此变量
    codeLen = len(code)
    print(codeLen)
    # 获取到图像的宽、高进行遍历
    for i in range(img.size[0]):
        for j in range(img.size[1]):
            # 获取到图片的每个像素值
            data = img.getpixel((i, j))

            # 如果计数器等于长度，代表水印写入完成
            if count == codeLen:
                break

            # 将获取到的RGB数值分别保存
            r = data[0]
            g = data[1]
            b = data[2]

            """
            下面是像素值替换，通过取模2得到最后一位像素值（0或1），
            然后减去最后一位像素值，在将code的值添加过来
            """

            r = (r - r % 2) + int(code[count])
            count += 1
            if count == codeLen:
                img.putpixel((i, j), (r, g, b))
                break

            g = (g - g % 2) + int(code[count])
            count += 1
            if count == codeLen:
                img.putpixel((i, j), (r, g, b))
                break

            b = (b - b % 2) + int(code[count])
            count += 1
            if count == codeLen:
                img.putpixel((i, j), (r, g, b))
                break

            # 每3次循环表示一组RGB值被替换完毕，可以进行写入
            if count % 3 == 0:
                img.putpixel((i, j), (r, g, b))
    img.save('加密图片.png')


# 获取图像对象
img1 = Image.open('carrier.png')
img2 = Image.open('watermark.png')#.convert('L')

# 将图像转换为RGB通道，才能分别获取R,G,B的值
rgb_im1 = img1.convert('RGB')
print(rgb_im1.size)
rgb_im2 = img2.convert('RGB')
print(rgb_im2.size)

# 将水印的像素值转为文本
code = getCode(rgb_im2)

# 将水印写入图像
encry(rgb_im1, code)