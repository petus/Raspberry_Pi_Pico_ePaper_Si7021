# https://github.com/mcauser/micropython-waveshare-epaper

import epaper4in2b
from machine import Pin, SPI, I2C
import si7021 #import SI7021
import utime #import timer
import font24

COLORED = 1
UNCOLORED = 0

dc = Pin(12)
cs = Pin(13)
rst = Pin(11)
busy = Pin(10)

spi=SPI(0)
spi=SPI(0,100_000)
spi=SPI(0,100_000,polarity=1,phase=1)

e = epaper4in2b.EPD(spi, cs, dc, rst, busy)
e.init()

i2c = I2C(0, scl=Pin(9), sda=Pin(8), freq=200000)       # Inicializace GP8 & GP9 (default I2C0)
temp_sensor = si7021.Si7021(i2c)

print('Si7021 Teplota: {value}'.format(value=temp_sensor.temperature))
print('Si7021 Vlhkost: {value}'.format(value=temp_sensor.relative_humidity))

w = 400
h = 300

# use a frame buffer
# 400 * 300 / 8 = 15000 - thats a lot of pixels
#import framebuf
#buf = bytearray(w * h // 8)
#fb = framebuf.FrameBuffer(buf, w, h, framebuf.MONO_HLSB)
#black = 0
#white = 1
#fb.fill(white)

#fb.text('Raspberry Pi Pico, ePaper and Si7021',30,10,black)
#fb.text('Temperature: {value}'.format(value=str(round(temp_sensor.temperature,2))),30,30, black)
#fb.text('Humidity: {value}'.format(value=str(round(temp_sensor.relative_humidity,2))),30,50, black)
#e.display_frame(buf)

fb_size = int(w * h / 8)
frame_black = bytearray(fb_size)
frame_red = bytearray(fb_size)

e.clear_frame(frame_black, frame_red)

# write strings to the buffer
e.display_string_at(frame_black, 20, 10, "Raspberry Pi Pico", font24, COLORED)
e.display_string_at(frame_black, 20, 40, "ePaper and Si7021", font24, COLORED)
e.display_string_at(frame_red, 20, 100, "Temperature: {value}".format(value=str(round(temp_sensor.temperature,2))), font24, COLORED)
e.display_string_at(frame_red, 20, 130, "Humidity: {value}".format(value=str(round(temp_sensor.relative_humidity,2))), font24, COLORED)
# display the frame
e.display_frame(frame_black, frame_red)

e.sleep()

utime.sleep(60)