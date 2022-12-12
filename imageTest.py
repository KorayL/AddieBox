import digitalio
import board
from PIL import Image, ImageDraw, ImageFont
from adafruit_rgb_display import ili9341

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

image = Image.new("RGB", (320, 240))
font = ImageFont.truetype(r"Comfortaa_Regular.ttf", 15)
draw = ImageDraw.Draw(image)

draw.text((0, 0), "This is a test", font=font, fill=(255, 255, 255))

disp.Image(image)