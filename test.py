import digitalio
import board
from PIL import Image, ImageDraw
from adafruit_rgb_display import ili9341

import RPi.GPIO as gpio

cs_pin = digitalio.DigitalInOut(board.CE0)
dc_pin = digitalio.DigitalInOut(board.D25)
reset_pin = digitalio.DigitalInOut(board.D24)

# Config for display baudrate (default max is 24mhz):
BAUDRATE = 24000000

spi = board.SPI()
disp = ili9341.ILI9341(
    spi,
    rotation=180,
    cs=cs_pin,
    dc=dc_pin,
    rst=reset_pin,
    baudrate=BAUDRATE,
)

image = Image.open("AddieBox/slope.jpg")
disp.image(image)

gpio.setmode(gpio.BCM)
gpio.setup(17, gpio.OUT)
gpio.output(17, gpio.HIGH)
