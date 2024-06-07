import numpy as np
import PIL.Image as Image

# 读取图片的像素信息
picture = Image.open('carrier.png').convert('L')
pic_data = np.array(picture)

# 读取要隐写的文件
with open('secret.txt', encoding="utf-8") as file:
    secrets = file.read()

# 将图片拷贝一份，作为最终的图片数据
im_data = np.array(picture.copy()).ravel().tolist()

def cover_lsb(bin_index, data):
    '''
    :param bin_index:  当前字符的ascii的二进制
    :param data: 取出数组像素的八个数值
    :return: LSB隐写后的字符
    '''
    for i in range(len(secrets)):
        # 拿到第i个数据,转换成二进制
        data = im_data[i * 8: (i + 1) * 8]
        data_int = lsb_decode(data)
        # 找到最低位
        res_data.append(int(data_int, 2))

pic_idx = 0
# 采用LSB隐写技术，横向取数据，每次取8个数据，改变8个像素最低位
res_data = []
for i in range(len(secrets)):
    # 拿到隐写文件的字符ascii数值, 并转换为二进制,填充成八位
    index = ord(secrets[i])
    bin_index = bin(index)[2:].zfill(8)
    # 对数据进行LSB隐写，替换操作
    res = cover_lsb(bin_index, im_data[pic_idx * 8: (pic_idx + 1) * 8])
    pic_idx += 1
    res_data += res
# 对剩余未填充的数据进行补充填充，防止图像无法恢复
res_data += im_data[pic_idx * 8:]

# 将新生成的文件进行格式转换并保存，此处一定保存为不压缩的png文件
new_im_data = np.array(res_data).astype(np.uint8).reshape((pic_data.shape))
res_im = Image.fromarray(new_im_data)
res_im.save('res_encode.png')
