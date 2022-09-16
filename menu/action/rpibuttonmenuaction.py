from queue import Queue
import threading

from menu.action.menuaction import MenuAction

#    sudo pip install RPi.GPIO

import RPi.GPIO as GPIO

class RPiButtonBoardMenuAction(MenuAction):

    def __init__(self,
        actionQueue: Queue,\
        s1Pin: int, \
        s2Pin: int, \
        upPin: int, \
        downPin: int, \
        leftPin: int, \
        rightPin: int):

        self._actionQueue = actionQueue

        self._s1Pin = s1Pin
        self._s2Pin = s2Pin
        self._upPin = upPin
        self._downPin = downPin
        self._leftPin = leftPin
        self._rightPin = rightPin

        GPIO.setmode(GPIO.BOARD)

        # Button presses happen on rising edge
        GPIO.setup(upPin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(downPin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(leftPin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(rightPin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(s1Pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(s2Pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

        DEBOUNCE_TIME_IN_MS = 100
        GPIO.add_event_detect(upPin, GPIO.RISING, callback=self.button_press, bouncetime=DEBOUNCE_TIME_IN_MS)
        GPIO.add_event_detect(downPin, GPIO.RISING, callback=self.button_press, bouncetime=DEBOUNCE_TIME_IN_MS)
        GPIO.add_event_detect(leftPin, GPIO.RISING, callback=self.button_press, bouncetime=DEBOUNCE_TIME_IN_MS)
        GPIO.add_event_detect(rightPin, GPIO.RISING, callback=self.button_press, bouncetime=DEBOUNCE_TIME_IN_MS)
        GPIO.add_event_detect(s1Pin, GPIO.RISING, callback=self.button_press, bouncetime=DEBOUNCE_TIME_IN_MS)
        GPIO.add_event_detect(s2Pin, GPIO.RISING, callback=self.button_press, bouncetime=DEBOUNCE_TIME_IN_MS)


    def button_press(self, channel):
        print("channel type: "+str(type(channel)))
        print("channel value: "+str(channel))

        action = self.map_input_to_action(action)
        self._actionQueue.put(action)

    def get_actions(self):
        pass

    def start(self):
        pass

    def stop(self):
        self._actionQueue.put(MenuAction.Action.QUIT)
        GPIO.cleanup()

    # Maps a pin value to a menu action
    def map_input_to_action(self, value) -> MenuAction.Action:
        match value:
            case self._upPin:
                return MenuAction.Action.UP
            case self._downPin:
                return MenuAction.Action.DOWN
            case self._s2Pin | self._rightPin:
                return MenuAction.Action.SELECT
            case self._s1Pin:
                return MenuAction.Action.HOME
            case _:
                return MenuAction.Action.NONE