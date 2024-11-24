import board
import digitalio
import time

import usb_hid
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS
from adafruit_hid.mouse import Mouse

kbd = Keyboard(usb_hid.devices)
mouse = Mouse(usb_hid.devices)
layout = KeyboardLayoutUS(kbd)

characters = [
    ["LC", "W", "RC", "SH"],
    ["A", "S", "D", "Q"],
    ["IL", "E", "IN", "LU"],
    ["LL", "SPACE", "LR", "LD"],
]

rowPins = [board.GP2, board.GP3, board.GP4, board.GP5]
rows = []
for pin in rowPins:
    row = digitalio.DigitalInOut(pin)
    row.direction = digitalio.Direction.OUTPUT
    row.value = False
    rows.append(row)

colPins = [board.GP6, board.GP7, board.GP8, board.GP9]
cols = []
for pin in colPins:
    col = digitalio.DigitalInOut(pin)
    col.direction = digitalio.Direction.INPUT
    col.pull = digitalio.Pull.DOWN
    cols.append(col)

keymap = {
    "1": [Keycode.ONE],
    "2": [Keycode.TWO],
    "3": [Keycode.THREE],
    "4": [Keycode.FOUR],
    "5": [Keycode.FIVE],
    "6": [Keycode.SIX],
    "7": [Keycode.SEVEN],
    "8": [Keycode.EIGHT],
    "9": [Keycode.NINE],
    "0": [Keycode.ZERO],
    "A": [Keycode.A],
    "B": [Keycode.B],
    "C": [Keycode.C],
    "D": [Keycode.D],
    "E": [Keycode.E],
    "F": [Keycode.F],
    "G": [Keycode.G],
    "H": [Keycode.H],
    "I": [Keycode.I],
    "J": [Keycode.J],
    "K": [Keycode.K],
    "L": [Keycode.L],
    "M": [Keycode.M],
    "N": [Keycode.N],
    "O": [Keycode.O],
    "P": [Keycode.P],
    "Q": [Keycode.Q],
    "R": [Keycode.R],
    "S": [Keycode.S],
    "T": [Keycode.T],
    "U": [Keycode.U],
    "V": [Keycode.V],
    "W": [Keycode.W],
    "X": [Keycode.X],
    "Y": [Keycode.Y],
    "Z": [Keycode.Z],
    "SPACE": [Keycode.SPACE],
    "LC": ["leftClick"],
    "RC": ["rightClick"],
    "IL": ["inventoryLast"],
    "IN": ["inventoryNext"],
    "LL": ["lookLeft"],
    "LR": ["lookRight"],
    "LU": ["lookUp"],
    "LD": ["lookDown"],
    "SH": [Keycode.SHIFT],
    "ESC": [Keycode.ESCAPE],
    "*": [Keycode.KEYPAD_ASTERISK],
    "#": [Keycode.SHIFT, Keycode.THREE],
}


def readKey():
    pressedKeys = []
    for i, row in enumerate(rows):
        row.value = True
        for j, col in enumerate(cols):
            if col.value:
                pressedKeys.append(characters[i][j])
        row.value = False

    return pressedKeys if pressedKeys else []


pressedKeys = set()

while True:
    currentKeys = set(readKey())

    newlyPressed = currentKeys - pressedKeys
    for key in newlyPressed:
        if key in keymap:
            if keymap[key] == ["leftClick"]:
                mouse.press(Mouse.LEFT_BUTTON)
            elif keymap[key] == ["rightClick"]:
                mouse.press(Mouse.RIGHT_BUTTON)
            elif keymap[key] == ["inventoryNext"]:
                mouse.move(wheel=-1)
            elif keymap[key] == ["inventoryLast"]:
                mouse.move(wheel=1)
            elif keymap[key] == ["lookLeft"]:
                mouse.move(x=-20)
            elif keymap[key] == ["lookRight"]:
                mouse.move(x=20)
            elif keymap[key] == ["lookUp"]:
                mouse.move(y=-20)
            elif keymap[key] == ["lookDown"]:
                mouse.move(y=20)
            else:
                for keycode in keymap[key]:
                    kbd.press(keycode)

    releasedKeys = pressedKeys - currentKeys
    for key in releasedKeys:
        if key in keymap:
            if keymap[key] == ["leftClick"]:
                mouse.release(Mouse.LEFT_BUTTON)
            elif keymap[key] == ["rightClick"]:
                mouse.release(Mouse.RIGHT_BUTTON)
            elif keymap[key] in (
                ["inventoryLast"],
                ["inventoryNext"],
                ["lookLeft"],
                ["lookRight"],
                ["lookUp"],
                ["lookDown"],
            ):
                pass
            else:
                for keycode in reversed(keymap[key]):
                    kbd.release(keycode)

    for key in currentKeys:
        if key in keymap:
            if keymap[key] == ["lookLeft"]:
                mouse.move(x=-20)
            elif keymap[key] == ["lookRight"]:
                mouse.move(x=20)
            elif keymap[key] == ["lookUp"]:
                mouse.move(y=-20)
            elif keymap[key] == ["lookDown"]:
                mouse.move(y=20)

    pressedKeys = currentKeys

    time.sleep(0.1)
