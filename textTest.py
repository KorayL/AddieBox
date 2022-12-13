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
    rotation=90,
    cs=cs_pin,
    dc=dc_pin,
    rst=reset_pin,
    baudrate=BAUDRATE,
)

fontName = "Comfortaa_Regular.ttf"
image = Image.new("RGB", (320, 240))
font = ImageFont.truetype(fontName, 15)
draw = ImageDraw.Draw(image)

# string = "In the loveliest town of all, where the houses were white and high and the elms trees were green and higher than the houses, where the front yards were wide and pleasant and the back yards were bushy and worth finding out about, where the streets sloped down to the stream and the stream flowed quietly under the bridge, where the lawns ended in orchards and the orchards ended in fields and the fields ended in pastures and the pastures climbed the hill and disappeared over the top toward the wonderful wide sky, in this loveliest of all towns Stuart stopped to"
string = "Koray's Screen Works!"
tokens = string.split()

finalString = tokens[0]  # adds first word
rightBound = font.getlength(finalString)  # gets length of first word (px)
start = 0  # initialize start character index of current line

# Adds line returns to finalString so it fits on screen
for i, word in zip(range(1, len(tokens)), tokens[1:]):  # iterate through tokens with index i
    # get length of current line
    rightBound = font.getlength(f"{finalString[start:]} {word}")
    if rightBound > 320:
        finalString = f"{finalString}\n{word}"
        # start is moved to index before the start of final word in string
        start = len(finalString) - len(word)
        rightBound = 0
    else:
        finalString = f"{finalString} {word}"


# Scale text to fill screen if finalString is one line
if "\n" not in finalString:
    pixelSize = font.getlength(finalString)
    i = 1
    while pixelSize <= 320:
        i += 1
        font = ImageFont.truetype(fontName, 15 + i)
        pixelSize = font.getlength(finalString)
    font = ImageFont.truetype(fontName, 15+i-1)

# Center text
left, top, right, bottom = draw.multiline_textbbox((0, 0), finalString, font=font)
width, height = right-left, top-bottom
x, y = 160-0.5*width, 120+0.5*height

draw.text((x, y), finalString, font=font, fill=(0, 0, 0))

disp.image(image)
