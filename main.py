# Raspberry_Pi_Pico_ePaper_Si7021
# Example code for Raspberry Pi Pico with 4.2" b/w/r ePaper and Si7021 
# Thanks to
# https://github.com/mcauser/micropython-waveshare-epaper
# https://github.com/ayoy/micropython-waveshare-epd

from machine import Pin, SPI, I2C
import epaper4in2b #import ePaper 4.2" b/w/r
import si7021 #import SI7021
import utime #import timer
import font24 #import font

COLORED = 1
UNCOLORED = 0
w = 400
h = 300

#SPI pins
dc = Pin(12)
cs = Pin(13)
rst = Pin(11)
busy = Pin(10)

# SPI
spi=SPI(0)
spi=SPI(0,100_000)
spi=SPI(0,100_000,polarity=1,phase=1)

# ePaper
epd = epaper4in2b.EPD(spi, cs, dc, rst, busy) # Init ePaper | CLK GP6, MOSI GP7
epd.init()

# I2C
i2c = I2C(0, scl=Pin(9), sda=Pin(8), freq=200000)       # Init GP8 & GP9 (default I2C0)
temp_sensor = si7021.Si7021(i2c)

print('Si7021 Temperature: {value}'.format(value=temp_sensor.temperature))
print('Si7021 Humidity: {value}'.format(value=temp_sensor.relative_humidity))

# create frames
fb_size = int(w * h / 8)
frame_black = bytearray(fb_size)
frame_red = bytearray(fb_size)

epd.clear_frame(frame_black, frame_red)

# write strings to the buffer
epd.display_string_at(frame_black, 20, 10, "Raspberry Pi Pico", font24, COLORED)
epd.display_string_at(frame_black, 20, 40, "ePaper and Si7021", font24, COLORED)
epd.display_string_at(frame_black, 20, 100, "Temperature: {value}".format(value=str(round(temp_sensor.temperature,2))), font24, COLORED)
epd.display_string_at(frame_black, 20, 130, "Humidity: {value}".format(value=str(round(temp_sensor.relative_humidity,2))), font24, COLORED)

epd.display_string_at(frame_red, 20, 160, "@chiptronCZ", font24, COLORED)

# display the frame
epd.display_frame(frame_black, frame_red)

#sleep
epd.sleep()

#repeat after 60s
utime.sleep(60)
