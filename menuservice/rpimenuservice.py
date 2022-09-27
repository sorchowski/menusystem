from pathlib import Path
import signal, os
from queue import Queue

from menu.menusystem import MenuSystem
from menu.action.rpibuttonmenuaction import RPiButtonBoardMenuAction
from menu.display.sparkfunlcd import Sparkfun4x20LCDDisplay

# Get the current location of this script
__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

actionQueue = Queue()

GPIO_PIN_UP = 36    # GPIO16
GPIO_PIN_DOWN = 37  # GPIO26
GPIO_PIN_LEFT = 35  # GPIO19
GPIO_PIN_RIGHT = 31 # GPIO06
GPIO_PIN_S1 = 40    # GPIO21
GPIO_PIN_S2 = 38    # GPIO20

menuAction = RPiButtonBoardMenuAction(actionQueue, GPIO_PIN_S1, GPIO_PIN_S2, GPIO_PIN_UP, GPIO_PIN_DOWN, GPIO_PIN_LEFT, GPIO_PIN_RIGHT)

display = Sparkfun4x20LCDDisplay(4, 20, 'ascii')

nodesPath = os.path.join(__location__, 'menunodes.json')
executorsPath = os.path.join(__location__, 'executors.json')
scriptsPath = os.path.join(__location__, 'scripts')

menuSystem = MenuSystem(nodesPath, executorsPath, Path(scriptsPath), display, actionQueue, menuAction)

def handle_sigterm(sig, frame):
    menuAction.stop()
    menuSystem.stop()
    display.cleanup()

signal.signal(signal.SIGTERM, handle_sigterm)

menuSystem.run()
