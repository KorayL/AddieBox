import digitalio
import board
from PIL import Image, ImageDraw, ImageFont
from adafruit_rgb_display import ili9341

from gpiozero import Button, LED
import os

from git import Repo
import shutil

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

    if disp.rotation % 180 == 90:
        displayWidth = disp.height
        displayHeight = disp.width
    else:
        displayWidth = disp.width
        displayHeight = disp.height

    blackImage = Image.new("RGB", (displayWidth, displayHeight))
    # Display black before loop starts
    disp.image(blackImage)

    tiltSwitch = Button(17)
    button = Button(27)
    led = LED(22)

    fileData = fetch_data()
    lastState = 0       # 0: lid closed, 1: lid open
    fileNumber = 0
    cloneLoopCounter = 0
    while True:

        seenFiles = list(map(int, open("AddieBox/accessedFiles.txt", "r").read().split(",")))
        numberOfFilesPresent = len(os.listdir("Addie-Box-Data"))-2
        # Turn on led if there are unseen messages
        if len(seenFiles) < numberOfFilesPresent:
            led.on()
        else:
            led.off()

        if tiltSwitch.is_pressed:
            if not lastState:
                fileNumber = 0  # work with last uploaded file
                fileData = fetch_data()
                fileData[fileNumber].display(displayWidth, displayHeight, disp)
                update_seen_files(numberOfFilesPresent-fileNumber, seenFiles)
            if button.is_pressed:
                fileNumber += 1     # go to the second most recent file
                if fileNumber > len(fileData)-1:
                    fileNumber = 0
                fileData[fileNumber].display(displayWidth, displayHeight, disp)
                update_seen_files(numberOfFilesPresent-fileNumber, seenFiles)
            lastState = 1
        else:
            if lastState:
                disp.image(blackImage)
            lastState = 0

            # Update Data Files
            if cloneLoopCounter >= 500:
                shutil.rmtree("Addie-Box-Data")
                print("repo removed")
                Repo.clone_from("https://github.com/KorayL/Addie-Box-Data.git", "Addie-Box-Data")
                print("repo cloned")
                cloneLoopCounter = 0
            cloneLoopCounter += 1



def update_seen_files(fileNumber, seenFiles):
    if fileNumber not in seenFiles:
        seenFiles.append(fileNumber)
        seenFiles.sort()
        seenFilesFile = open("AddieBox/accessedFiles.txt", "w")
        # clear the document
        seenFilesFile.truncate(0)
        # change the int list to a str list, then convert it to a string and write it to the file
        seenFilesFile.write(",".join(list(map(str, seenFiles))))


def fetch_data():
    # Get text and image files to be used
    dataFiles = os.listdir("Addie-Box-Data")
    dataFiles.remove(".git")
    dataFiles.remove(".gitattributes")
    dataFiles.sort(reverse=True)

    # Create object list with type and possibly text attributes
    dataObjects = []
    for fileName in dataFiles:
        dataObjects.append(file_type(fileName))

    return dataObjects


def fit_string(string, draw):
    # splits string into a list of every word
    tokens = string.split()

    font = ImageFont.truetype("Questrial-Regular.ttf", 15)

    finalString = tokens[0]  # adds first word
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
        font = ImageFont.truetype("Questrial-Regular.ttf", 15)
        left, top, right, bottom = draw.textbbox((0, 0), finalString, font=font)
        width, height = right-left, bottom-top
        textAspectRatio = width/height
        print(textAspectRatio)
        if textAspectRatio < 4/3:
            pixelSizeAt15 = height
            maxPixels = 240
        else:
            pixelSizeAt15 = width
            maxPixels = 320

        fontSize = int((maxPixels*15)//pixelSizeAt15)
        font = ImageFont.truetype("Questrial-Regular.ttf", fontSize)
    else:
        fontSize = font.size

    # Center text
    left, top, right, bottom = draw.multiline_textbbox((0, 0), finalString, font=font)
    width, height = right - left, top-bottom
    x, y = 160 - 0.5 * width, 120 + 0.5 * height

    return finalString, (x, y), fontSize


class file_type:
    def __init__(self, file_name):
        name, extension = os.path.splitext(file_name)
        if extension == ".txt":
            self.type = "text"
            self.text = open(f"Addie-Box-Data/{file_name}").read()
        else:
            self.type = "image"
        self.name = file_name

    def display(self, width, height, disp):
        if self.type == "image":
            image = Image.open(f"Addie-Box-Data/{self.name}")
            disp.image(image)
        else:
            image = Image.new("RGB", (width, height))
            draw = ImageDraw.Draw(image)
            displayString, coordinates, fontSize = fit_string(self.text, draw)
            font = ImageFont.truetype("Questrial-Regular.ttf", fontSize)
            draw.text(coordinates, displayString, font=font, fill=(255, 255, 255))
            disp.image(image)


if __name__ == '__main__':
    main()
