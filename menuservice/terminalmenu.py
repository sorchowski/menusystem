from pathlib import Path
from queue import Queue
import signal, os, logging

from menu.display.terminal import TerminalDisplay
from menu.action.keyboardmenuaction import KeyboardMenuAction
from menu.menusystem import MenuSystem

# Get the current location of this script
__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

logging.basicConfig(filename='/var/log/terminalmenu.log', level=logging.INFO)

actionQueue = Queue()

keyboardMenuAction = KeyboardMenuAction(actionQueue)

nodesPath = os.path.join(__location__, 'menunodes.json')
executorsPath = os.path.join(__location__, 'executors.json')
scriptsPath = os.path.join(__location__, 'scripts')

menuSystem = MenuSystem(nodesPath, executorsPath, Path(scriptsPath), TerminalDisplay(), actionQueue, keyboardMenuAction)

def handle_terminate(signalNumber, frame):
    logging.warn('Got signal to terminate, calling menuSystem.stop and keyboard.stop')
    keyboardMenuAction.stop()
    menuSystem.stop()

# Note, ctrl-c doesn't seem to work too well with the blocking input method for keyboard menu actions
signal.signal(signal.SIGINT, handle_terminate)

menuSystem.run() # Will block until user quits via terminal input 'q'
