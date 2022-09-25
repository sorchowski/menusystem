from pathlib import Path
from queue import Queue
import signal, os

from menu.display.terminal import TerminalDisplay
from menu.action.keyboardmenuaction import KeyboardMenuAction
from menu.menusystem import MenuSystem

# Get the current location of this script
__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

actionQueue = Queue()

keyboardMenuAction = KeyboardMenuAction(actionQueue)

# TODO: need better way for relative path to data
nodesPath = os.path.join(__location__, '..', 'data', 'menunodes.json')
executorsPath = os.path.join(__location__, '..', 'data', 'executors.json')
scriptsPath = os.path.join(__location__, '..', 'data', 'scripts')

menuSystem = MenuSystem(nodesPath, executorsPath, Path(scriptsPath), TerminalDisplay(), actionQueue, keyboardMenuAction)

def handle_terminate(signalNumber, frame):
    print('Got signal to terminate, calling menuSystem.stop and keyboard.stop')
    keyboardMenuAction.stop()
    menuSystem.stop()

# Note, ctrl-c doesn't seem to work too well with the blocking input method for keyboard menu actions
signal.signal(signal.SIGINT, handle_terminate)

menuSystem.run() # Will block until user quits via terminal input 'q'
