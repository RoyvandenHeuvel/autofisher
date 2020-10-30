from time import sleep

import mouse
import keyboard
from PIL import ImageChops
from pyautogui import Point, position
from pyscreenshot import grab
from win32con import VK_ESCAPE

from multiprocessing import Process, freeze_support

def main():
    topLeft = None

    sleep(1)
    print("Left-click the top-left of experience bar.")
    while topLeft is None:
        if mouse.is_pressed(mouse.LEFT):
            topLeft = position()

    bottomRight = None

    sleep(2)
    print("Left-click the bottom-right of experience bar.")
    while bottomRight is None:
        if mouse.is_pressed(mouse.LEFT):
            bottomRight = position()

    selectionBox = (topLeft.x, topLeft.y, bottomRight.x, bottomRight.y)

    pollsPerSecond: int = 1
    frameRate: int = 60

    while True:
        initialFrame = grab(selectionBox, False)

        sleep((pollsPerSecond / frameRate))

        secondaryFrame = grab(selectionBox, False)

        difference = ImageChops.difference(initialFrame, secondaryFrame)

        differenceBox = difference.getbbox()

        if differenceBox is not None:
            print('Ooh, a fishy!')
            mouse.click('right')

        if keyboard.is_pressed('ctrl+c'):
            print('Stopping autofisher...')
            break

if __name__ == "__main__":
    freeze_support()
    print('Starting AutoFisher...')
    Process(target=main).start()