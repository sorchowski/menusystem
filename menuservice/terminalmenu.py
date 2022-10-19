from pathlib import Path
from queue import Queue
import signal, os, logging

from menu.display.terminal import TerminalDisplay
from menu.action.keyboardmenuaction import KeyboardMenuAction
from menu.menusystem import MenuSystem
from menu.menus import Menus, Executor, Navigator

# Get the current location of this script
__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

logging.basicConfig(filename='/var/log/terminalmenu.log', level=logging.INFO)

nodesPath = os.path.join(__location__, 'menunodes.json')
executorsPath = os.path.join(__location__, 'executors.json')
scriptsPath = os.path.join(__location__, 'scripts')

menus = Menus(nodesPath)
executor = Executor(executorsPath, Path(scriptsPath))
navigator = Navigator(menus)
actionQueue = Queue()
keyboardMenuAction = KeyboardMenuAction(actionQueue)

menuSystem = MenuSystem(menus, executor, navigator, TerminalDisplay(), actionQueue, keyboardMenuAction)


def handle_terminate(signalNumber, frame):
    logging.warn('Got signal to terminate, calling menuSystem.stop and keyboard.stop')
    keyboardMenuAction.stop()
    menuSystem.stop()

# Note, ctrl-c doesn't seem to work too well with the blocking input method for keyboard menu actions
signal.signal(signal.SIGINT, handle_terminate)

menuSystem.run() # Will block until user quits via terminal input 'q'
