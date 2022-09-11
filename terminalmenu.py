from pathlib import Path
from queue import Queue
import signal

from menu.displays import TerminalDisplay
from menu.keyboardmenuaction import KeyboardMenuAction
from menu.menusystem import MenuSystem

actionQueue = Queue()

keyboardMenuAction = KeyboardMenuAction(actionQueue)

menuSystem = MenuSystem('menunodes.json', 'executors.json', Path("scripts"), TerminalDisplay(), actionQueue, keyboardMenuAction)

def handle_terminate(signalNumber, frame):
    print('Got signal to terminate, calling menuSystem.stop and keyboard.stop')
    keyboardMenuAction.stop()
    menuSystem.stop()

# Note, ctrl-c doesn't seem to work too well with the blocking input method for keyboard menu actions
signal.signal(signal.SIGINT, handle_terminate)

menuSystem.run() # Will block until user quits via terminal input 'q'
