
#byte3里面是font.py里的文本，经过此程序处理可用于font_new.py
byte3 = {
    0xe5a4a9:
        [0x00, 0x3F, 0x01, 0x01, 0x01, 0x01, 0xFF, 0x01, 0x02, 0x02, 0x04, 0x04, 0x08, 0x10, 0x20, 0xC0,
         0x00, 0xF8, 0x00, 0x00, 0x00, 0x00, 0xFE, 0x00, 0x80, 0x80, 0x40, 0x40, 0x20, 0x10, 0x08, 0x06, ],  # 天

    0xe6b094:
        [0x10, 0x10, 0x3F, 0x20, 0x4F, 0x80, 0x3F, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
         0x00, 0x00, 0xFC, 0x00, 0xF0, 0x00, 0xF0, 0x10, 0x10, 0x10, 0x10, 0x10, 0x0A, 0x0A, 0x06, 0x02, ],  # 气

    0xe5a49a:
        [0x02, 0x02, 0x07, 0x08, 0x38, 0x04, 0x03, 0x0C, 0x71, 0x02, 0x0C, 0x32, 0x01, 0x01, 0x0E, 0x70,
         0x00, 0x00, 0xF0, 0x20, 0x40, 0x80, 0x40, 0x80, 0xF8, 0x08, 0x10, 0x20, 0x40, 0x80, 0x00, 0x00, ],  # 多

    0xe4ba91:
        [0x00, 0x3F, 0x00, 0x00, 0x00, 0x00, 0xFF, 0x02, 0x04, 0x04, 0x08, 0x10, 0x20, 0x7F, 0x20, 0x00,
         0x00, 0xF8, 0x00, 0x00, 0x00, 0x00, 0xFE, 0x00, 0x00, 0x00, 0x40, 0x20, 0x10, 0xF8, 0x08, 0x08, ],  # 云

    0xe8bdac:
        [0x20, 0x20, 0x20, 0xFD, 0x40, 0x50, 0x93, 0xFC, 0x10, 0x11, 0x1C, 0xF0, 0x50, 0x10, 0x10, 0x10,
         0x20, 0x20, 0x20, 0xFC, 0x20, 0x40, 0xFE, 0x40, 0x80, 0xFC, 0x04, 0x88, 0x50, 0x20, 0x10, 0x10, ],  # 转

    0xe699b4:
        [0x00, 0x00, 0x7B, 0x48, 0x49, 0x48, 0x4B, 0x78, 0x49, 0x49, 0x49, 0x49, 0x79, 0x49, 0x01, 0x01,
         0x20, 0x20, 0xFE, 0x20, 0xFC, 0x20, 0xFE, 0x00, 0xFC, 0x04, 0xFC, 0x04, 0xFC, 0x04, 0x14, 0x08, ],  # 晴
              }
         #在第一种数据创建的方法，创建第二种数据，用framebuf显示中文的数据
keys = byte3.keys()
value = byte3.values()
#获取数据的键值对
#print(keys,value)
dict_new = {}
#由于使用字模生成器生成的字模数据，这个数据将字模分为两个部分，先显示汉字的左半部分，然后是右半部分
#然而在第二种用blit显示，不会一半一半的显示，而是直接将整个汉字写入缓冲区，因此需要进行处理
for key in keys:
    l1 = []
    l2 = []
    print(key)
    byte_list = byte3[key]
    s = ''
    n = 0
    print(len(byte_list))
    for i in byte_list:
        if n < 16:
            l1.append(i)
        else:
            l2.append(i)
        n += 1
    l3 = []

    # print(l1, l2)
    for i in range(len(l1)):
        l3.append(l1[i])
        l3.append(l2[i])
    #print(l3)

    for i in l3:
        temp = hex(i)
        temp = temp[1:]
        #print(len(temp))
        if len(temp) < 3:
            temp = temp[0] + '0' + temp[1]
        temp = '\\' + temp
        #print(temp)
        s += temp
    s = 'b\'' + s + '\''
    print(s)
    dict_new[key] = s

print(dict_new)

new_str_dict = str(dict_new).replace('\\\\','\\')
new_str_dict = new_str_dict.replace("\"",'')
print(new_str_dict)