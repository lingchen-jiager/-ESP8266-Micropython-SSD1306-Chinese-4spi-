from machine import Pin,SPI
import ssd1306a
import font
hspi = SPI(1,baudrate=80000000,polarity=0,phase=0)
display = ssd1306a.SSD1306_SPI(128,64,hspi,Pin(5),Pin(4),Pin(16))
display.init_display()
#display.text('Hello,World',1,1)  #显示字
#display.draw_chinese_fast('天气多云转晴',2,0)
display.draw_chinese('天气多云转晴',2,0)
display.show()