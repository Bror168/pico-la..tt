import usb_hid
import time
import board
import digitalio
import storage

from adafruit_hid.keyboard import Keyboard
from keyboard_layout_win_sw import KeyboardLayout
from keycode_win_sw import Keycode

duckyCommands = {
    'WINDOWS': Keycode.WINDOWS, 'GUI': Keycode.GUI,
    'APP': Keycode.APPLICATION, 'MENU': Keycode.APPLICATION, 'SHIFT': Keycode.SHIFT,
    'ALT': Keycode.ALT, 'CONTROL': Keycode.CONTROL, 'CTRL': Keycode.CONTROL,
    'DOWNARROW': Keycode.DOWN_ARROW, 'DOWN': Keycode.DOWN_ARROW, 'LEFTARROW': Keycode.LEFT_ARROW,
    'LEFT': Keycode.LEFT_ARROW, 'RIGHTARROW': Keycode.RIGHT_ARROW, 'RIGHT': Keycode.RIGHT_ARROW,
    'UPARROW': Keycode.UP_ARROW, 'UP': Keycode.UP_ARROW, 'BREAK': Keycode.PAUSE,
    'PAUSE': Keycode.PAUSE, 'CAPSLOCK': Keycode.CAPS_LOCK, 'DELETE': Keycode.DELETE,
    'END': Keycode.END, 'ESC': Keycode.ESCAPE, 'ESCAPE': Keycode.ESCAPE, 'HOME': Keycode.HOME,
    'INSERT': Keycode.INSERT, 'NUMLOCK': Keycode.KEYPAD_NUMLOCK, 'PAGEUP': Keycode.PAGE_UP,
    'PAGEDOWN': Keycode.PAGE_DOWN, 'PRINTSCREEN': Keycode.PRINT_SCREEN, 'ENTER': Keycode.ENTER,
    'SCROLLLOCK': Keycode.SCROLL_LOCK, 'SPACE': Keycode.SPACE, 'TAB': Keycode.TAB,
    'BACKSPACE': Keycode.BACKSPACE,
    'A': Keycode.A, 'B': Keycode.B, 'C': Keycode.C, 'D': Keycode.D, 'E': Keycode.E,
    'F': Keycode.F, 'G': Keycode.G, 'H': Keycode.H, 'I': Keycode.I, 'J': Keycode.J,
    'K': Keycode.K, 'L': Keycode.L, 'M': Keycode.M, 'N': Keycode.N, 'O': Keycode.O,
    'P': Keycode.P, 'Q': Keycode.Q, 'R': Keycode.R, 'S': Keycode.S, 'T': Keycode.T,
    'U': Keycode.U, 'V': Keycode.V, 'W': Keycode.W, 'X': Keycode.X, 'Y': Keycode.Y,
    'Z': Keycode.Z, 'F1': Keycode.F1, 'F2': Keycode.F2, 'F3': Keycode.F3,
    'F4': Keycode.F4, 'F5': Keycode.F5, 'F6': Keycode.F6, 'F7': Keycode.F7,
    'F8': Keycode.F8, 'F9': Keycode.F9, 'F10': Keycode.F10, 'F11': Keycode.F11,
    'F12': Keycode.F12,
}

def convertLine(line):
    newline = []
    for key in filter(None, line.split(" ")):
        key = key.upper()
        command_keycode = duckyCommands.get(key, None)
        if command_keycode is not None:
            newline.append(command_keycode)
        elif hasattr(Keycode, key):
            newline.append(getattr(Keycode, key))
    return newline

def runScriptLine(line):
    for k in line:
        kbd.press(k)
    kbd.release_all()

def sendString(line):
    layout.write(line)

def parseLine(line):
    global defaultDelay
    if line.startswith("REM"):
        pass
    elif line.startswith("DELAY"):
        time.sleep(float(line[6:]) / 1000)
    elif line.startswith("STRING"):
        sendString(line[7:])
    elif line.startswith("PRINT"):
        print("[SCRIPT]: " + line[6:])
    elif line.startswith("IMPORT"):
        runScript(line[7:])
    elif line.startswith("DEFAULT_DELAY") or line.startswith("DEFAULTDELAY"):
        defaultDelay = int(line.split(" ")[1]) * 10
    else:
        newScriptLine = convertLine(line)
        runScriptLine(newScriptLine)

kbd = Keyboard(usb_hid.devices)
layout = KeyboardLayout(kbd)

time.sleep(0.5)

switch2 = digitalio.DigitalInOut(board.GP12)
switch2.direction = digitalio.Direction.INPUT
switch2.pull = digitalio.Pull.UP

switch = digitalio.DigitalInOut(board.GP10)
switch.direction = digitalio.Direction.INPUT
switch.pull = digitalio.Pull.UP

defaultDelay = 10

def runScript(file):
    global defaultDelay
    global progStatus

    duckyScriptPath = file
    f = open(duckyScriptPath, "r", encoding='utf-8')
    duckyScript = f.readlines()
    f.close()

    while duckyScript:
        parseLine(str(duckyScript[0]).rstrip())
        duckyScript.pop(0)

        if not switch.value:
            pr = "".join(duckyScript)
            f = open(duckyScriptPath, "w", encoding='utf-8')
            f.write(pr)
            f.close()
            progStatus = True
            break

progStatus = True
while True:    

    while progStatus:
        if switch2.value:
            progStatus = False

    if not progStatus:
        runScript("payload.dd")
