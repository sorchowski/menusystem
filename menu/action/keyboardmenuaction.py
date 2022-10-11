import threading, logging
from queue import Queue
from .menuaction import MenuAction

class KeyboardMenuAction(MenuAction):
    def __init__(self, actionQueue: Queue):
        self._actionQueue = actionQueue
        self._exitEvent = threading.Event()

    # a=home
    # s=<nothing>
    # i=up,m=down,j=<nothing>,l=select
    # q=quit

    # For unit test mocking purposes
    def get_input(self):
        return input('enter menu cmd ')

    def get_actions(self):

        while not self._exitEvent.is_set():
            charVal = self.get_input()
            logging.info("Got character input: "+str(charVal))
            action = self.map_input_to_action(charVal)
            self._actionQueue.put(action)
            if action == MenuAction.Action.QUIT:
                self._exitEvent.set()
            else:
                self._actionQueue.join() #Wait for the menu to process and update display

    def start(self):
        logging.info("Keyboard Menu Action starting")
        self._actionThread = threading.Thread(target=self.get_actions)
        self._actionThread.start()

    def stop(self):
        logging.info("Keyboard Menu Action stopping")
        self._actionQueue.put(MenuAction.Action.QUIT) #TODO: check if this is necessary
        self._exitEvent.set()
        self._actionThread.join()

    def map_input_to_action(self, value) -> MenuAction.Action:
        match value:
            case 'i':
                return MenuAction.Action.UP
            case 'm':
                return MenuAction.Action.DOWN
            case 'l' | 's':
                return MenuAction.Action.SELECT
            case 'a':
                return MenuAction.Action.HOME
            case 'q':
                return MenuAction.Action.QUIT
            case _:
                return MenuAction.Action.NONE

