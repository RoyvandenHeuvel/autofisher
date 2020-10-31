from time import sleep

import mouse
import keyboard
from PIL import ImageChops
from pyautogui import Point, position
from pyscreenshot import grab
from win32con import VK_ESCAPE

from multiprocessing import Process, freeze_support

F3 = 'f3'
F4 = 'f4'

def prompt_corner_position(corner_name: str, key_name: str) -> Point:
    print(f'Mouseover the {corner_name} of the experience bar, then press {key_name}')
    while True:
        if keyboard.is_pressed(key_name):
            return position()

def prompt_experience_bar():
    while keyboard.is_pressed(F3):
        sleep(0.01)
    
    topLeft: Point = prompt_corner_position('top-left', F3)

    while keyboard.is_pressed(F3):
        sleep(0.01)

    bottomRight: Point = prompt_corner_position('bottom-right', F3)

    return (topLeft.x, topLeft.y, bottomRight.x, bottomRight.y)

def verify_selection(selected_box, confirm_key_name, reselect_key_name):
    image = grab(selected_box)
    image.show()

    print(f'Is this your experience bar? Press {confirm_key_name} to confirm, press {reselect_key_name} to make a new selection.')
    while True:
        if keyboard.is_pressed(confirm_key_name):
            return selected_box
        elif keyboard.is_pressed(reselect_key_name):
            return reselect_area()

def reselect_area():
    selection = prompt_experience_bar()
    return verify_selection(selection, F3, F4)

def main():
    selectionBox = verify_selection(prompt_experience_bar(), F3, F4)

    pollsPerSecond: int = 6
    frameRate: int = 60

    pollsBetweenClickGap: int = 5
    clicked = False
    pollsSinceClick: int = 0
    maxPollsSinceLastClick: int = 45

    print(f'Hold {F4} to pause the program, {F3} to unpause the program, and CTRL+C to stop the program.')

    while True:
        initialFrame = grab(selectionBox, False)

        sleep((pollsPerSecond / frameRate))

        secondaryFrame = grab(selectionBox, False)

        difference = ImageChops.difference(initialFrame, secondaryFrame)

        differenceBox = difference.getbbox()

        if (differenceBox is not None) and (not clicked) and (pollsSinceClick > pollsBetweenClickGap):
            print('Ooh, fishy!')
            mouse.click('right')
            pollsSinceClick = 0
            clicked = True
        elif pollsSinceClick > maxPollsSinceLastClick:
            print('Probably caught a boot...')
            mouse.click('right')
            pollsSinceClick = 0
            clicked = True
        else:
            clicked = False
            pollsSinceClick = pollsSinceClick + 1

        if keyboard.is_pressed('ctrl+c'):
            print('Stopping AutoFisher...')
            break

        if keyboard.is_pressed(F4):
            print(f'Pausing autofisher, press {F3} to unpause.')
            while not keyboard.is_pressed(F3):
                sleep(0.001)

if __name__ == "__main__":
    freeze_support()
    print('Starting AutoFisher...')
    Process(target=main).start()