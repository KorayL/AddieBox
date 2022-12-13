import digitalio
import board
from PIL import Image, ImageDraw
from adafruit_rgb_display import ili9341

from gpiozero import Button

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

blankImage = Image.new("RGB", (240, 320))
blank = ImageDraw.Draw(blankImage)
blank = blank.rectangle((0, 0, 240, 320), fill = (0, 0, 0))

tiltSwitch = Button(17)

while True:
    print(f"Is tiled? {tiltSwitch.is_pressed}")
    if tiltSwitch.is_pressed:
        disp.image(image)
    else:
        disp.image(blank)
