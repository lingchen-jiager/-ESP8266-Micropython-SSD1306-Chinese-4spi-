# ESP8266-Micropython-SSD1306-Chinese （4spi）
在ESP8266上用Micropython使用SSD1306库用spi方式驱动oled显示中文.
使用的是7针的oled模块，默认使用4spi方式驱动。
# esp8266和oled模块连线
![image](https://user-images.githubusercontent.com/48639047/223399730-16849fcf-e5ca-4a99-b155-50e0630063f9.png)

#### 文件介绍

##### 1.example.py

运用本仓库中的方法实现oled显示的一个示例。

会显示一行字:天气多云

##### 2.font.py
如果你使用下文中提到的draw_chinese()方法来显示中文，则将这个文件传入esp8266。

一个存储字模的字典模块，字模为`pctolcd2002`软件生成的，具体配置在`字模.jpg`图片中.


```python
0x00,0x3F,0x01,0x01,0x01,0x01,0xFF,0x01,0x02,0x02,0x04,0x04,0x08,0x10,0x20,0xC0,
0x00,0xF8,0x00,0x00,0x00,0x00,0xFE,0x00,0x80,0x80,0x40,0x40,0x20,0x10,0x08,0x06,天0
```

然后通过一个python程序进行格式化处理

```python
def single_word(i):
    lattice = i[:-2]  # 获取数据
    word = i[-2:-1]  # 获取文本
    print(word)
    try:
        # 进行编码
        utf = word.encode('utf-8')
        byte_utf = 0x00
        byte_utf |= utf[0] << 16
        byte_utf |= utf[1] << 8
        byte_utf |= utf[2]
        # 进行数据保存
        result = '{}:\n  [{}], #{}\n'.format(hex(byte_utf), lattice, word)
        print(result)

    except IndexError:
        print(word)
if __name__ == '__main__':
    signle_word('''0x00,0x3F,0x01,0x01,0x01,0x01,0xFF,0x01,0x02,0x02,0x04,0x04,0x08,0x10,0x20,0xC0,
0x00,0xF8,0x00,0x00,0x00,0x00,0xFE,0x00,0x80,0x80,0x40,0x40,0x20,0x10,0x08,0x06,天0''')
```

得到结果，将结果作为字典的键值对放入`font.py`中

```py
0xe5a4a9:  [0x00,0x3F,0x01,0x01,0x01,0x01,0xFF,0x01,0x02,0x02,0x04,0x04,0x08,0x10,0x20,0xC0,
0x00,0xF8,0x00,0x00,0x00,0x00,0xFE,0x00,0x80,0x80,0x40,0x40,0x20,0x10,0x08,0x06,], #天
```

##### 3.font_new.py
如果你使用下文中提到的draw_chinese_fast()方法来显示中文，则将这个文件传入esp8266。

同样是字模模块，对`font.py`内的字模进行进一步处理，使用不同的方法进行显示

处理方法如下：

```python
byte3 = {
  0xe998b5:
  [0x00,0x7C,0x44,0x4B,0x48,0x50,0x49,0x49,0x44,0x44,0x44,0x6B,0x50,0x40,0x40,0x40,
0x40,0x40,0x40,0xFE,0x80,0xA0,0x20,0xFC,0x20,0x20,0x20,0xFE,0x20,0x20,0x20,0x20,], #阵
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
```

处理结果：

```python
{15308981: b'\x00\x40\x7c\x40\x44\x40\x4b\xfe\x48\x80\x50\xa0\x49\x20\x49\xfc\x44\x20\x44\x20\x44\x20\x6b\xfe\x50\x20\x40\x20\x40\x20\x40\x20'}
```

这样就得到了`font_new.py`中的内容


##### 4.ssd1306a.py

​	模块主要内容为micropython的ssd1306.py官方源码，然后添加显示中文的功能，加上一个a与官方模块进行区分，显示中文有两种方法

​	方法一：

​		利用官方模块的`pixel`方法进行像素的填充

```python
def draw_chinese(self,ch_str,x_axis,y_axis):
      offset_=0
      y_axis=y_axis*16#中文高度一行占8个
      x_axis=(x_axis*16)#中文宽度占16个
      for k in ch_str:
        code = 0x00#将中文转成16进制编码
        data_code = k.encode("utf-8")
        code |= data_code[0]<<16
        code |= data_code[1]<<8
        code |= data_code[2]		  
        print(hex(code))
        byte_data=font.byte2.get(code)
        for y in range(0,16):
          a_=bin(byte_data[y]).replace('0b','')
          while len(a_)<8:
            a_='0'+a_				  
          b_=bin(byte_data[y+16]).replace('0b','')
          while len(b_)<8:
            b_='0'+b_
          for x in range(0,8):
            self.pixel(x_axis+x-offset_,y+y_axis,int(a_[x]))#文字的上半部分
            self.pixel(x_axis+x+8-offset_,y+y_axis,int(b_[x]))#文字的下半部分

        offset_+=16
```

​	方法二：

​		观察到整个SSD1306类继承自`framebuf.FrameBuffer`，所以可通过创建`framebuf`并通过`FrameBuffer`类中的`blit`方法进行缓冲区写入

```python
def draw_chinese_fast(self,ch_str,x_axis,y_axis):
      offset_=0
      y_axis=y_axis*16#中文高度一行占8个
      x_axis=(x_axis*16)#中文宽度占16个
      for k in ch_str:
        code = 0x00#将中文转成16进制编码
        data_code = k.encode("utf-8")
        code |= data_code[0]<<16
        code |= data_code[1]<<8
        code |= data_code[2]		  
        
        try:
          byte_data=font_new.byte2.get(code)
          byte = bytearray(byte_data)
          buf = framebuf.FrameBuffer(byte,16,16,framebuf.MONO_HLSB)
          self.blit(buf,x_axis+offset_,y_axis)
        except:
          print(code)
        
        offset_+=16
```

总结，直接进行缓冲区写入速度非常快，可以保证实时刷新oled显示

