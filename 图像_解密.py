from PIL import Image

def deEncry(img, length):
    # 获取图片的宽和高
    width = img.size[0]
    height = img.size[1]
    # 计数
    count = 0
    # 结果文本，从图片中提取到的附加值（加密时附加在每个RGB通道后的二进制数值）
    wt = ""

    # 遍历图片
    for i in range(width):
        for j in range(height):
            # 获取像素点的值
            rgb = img.getpixel((i, j))

            # 提取R通道的附加值
            if count % 3 == 0:
                count += 1
                wt = wt + str(rgb[0] % 2)
                if count == length:
                    break

            # 提取G通道的附加值
            if count % 3 == 1:
                count += 1
                wt = wt + str(rgb[1] % 2)
                if count == length:
                    break

            # 提取B通道的附加值
            if count % 3 == 2:
                count += 1
                wt = wt + str(rgb[2] % 2)
                if count == length:
                    break
        if count == length:
            break
    return wt

def showImage(wt, img_width, img_height):
    str1 = []
    for i in range(0, len(wt), 8):
        # 以每8位为一组二进制，转换为十进制
        str1.append(int(wt[i:i + 8], 2))
    # 图片大于水印图片1个像素，便于对比
    img_out = Image.new("RGB", (img_width + 1, img_height + 1))
    flag = 0
    for m in range(0, img_width):
        for n in range(0, img_height):
            if flag == len(str1):
                break
            img_out.putpixel((m, n), (str1[flag], str1[flag + 1], str1[flag + 2]))
            flag += 3
        if flag == len(str1):
            break
    img_out.save("解密图片.png")
    img_out.show()


# 获取一下水印图片的宽和高，也就是解密的密钥
w_image = Image.open('watermark.png')#.convert('L')
image_width = w_image.size[0]
image_height = w_image.size[1]
length = image_width * image_height * 24

# 获取图片
img1 = Image.open('加密图片.png')
rgb_im1 = img1.convert('RGB')

wt = deEncry(rgb_im1, length)
showImage(wt, image_width, image_height)