import digitalio
import board
from PIL import Image, ImageDraw
from adafruit_rgb_display import ili9341

from gpiozero import Button
from time import sleep

def main():
    # Assign pin needed for SPI
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

    displayWidth = disp.width
    displayHeight = disp.height

    print(f"width: {displayWidth}\nheight: {displayHeight}")

    blackImage = Image.new("RGB", (displayWidth, displayHeight))

    tiltSwitch = Button(17)
    button = Button(27)

    while True:
        if tiltSwitch.is_pressed:
            pass
        else:
            disp.image(blackImage)
        sleep(1)        # Reduces load

def fit_string():
    pass

if __name__ == '__main__':
    main()
