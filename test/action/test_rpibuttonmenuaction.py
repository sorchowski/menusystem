# from top-level directory, run "python -m unittest discover -s test"
# https://realpython.com/python-testing

# https://github.com/wolever/parameterized
# pip install parameterized


import unittest
from unittest.mock import Mock, MagicMock, patch
from parameterized import parameterized

from menu.action.menuaction import MenuAction
from menu.action.rpibuttonmenuaction import RPiButtonBoardMenuAction

GPIO_PIN_UP = 36    # GPIO16
GPIO_PIN_DOWN = 37  # GPIO26
GPIO_PIN_LEFT = 35  # GPIO19
GPIO_PIN_RIGHT = 31 # GPIO06
GPIO_PIN_S1 = 40    # GPIO21
GPIO_PIN_S2 = 38    # GPIO20

s1Pin = GPIO_PIN_S1
s2Pin = GPIO_PIN_S2
upPin = GPIO_PIN_UP
downPin = GPIO_PIN_DOWN
leftPin = GPIO_PIN_LEFT
rightPin = GPIO_PIN_RIGHT

class TestKeyboardMenuActions(unittest.TestCase):

    @parameterized.expand([
        (GPIO_PIN_UP, MenuAction.Action.UP),
        (GPIO_PIN_DOWN, MenuAction.Action.DOWN),
        (GPIO_PIN_S2, MenuAction.Action.SELECT),
        (GPIO_PIN_RIGHT, MenuAction.Action.SELECT),
        (GPIO_PIN_S1, MenuAction.Action.HOME)
    ])
    @patch.multiple('RPi.GPIO',
        setmode=MagicMock(return_value=None),
        setup=MagicMock(return_value=None),
        add_event_detect=MagicMock(return_value=None),
        cleanup=MagicMock(return_value=None))
    def test_map_input_to_action(self, inputValue, expectedAction: MenuAction.Action):
        actionQueue = Mock()
        rpiButtonMA = RPiButtonBoardMenuAction(actionQueue, s1Pin, s2Pin, upPin, downPin, leftPin, rightPin)
        menuAction = rpiButtonMA.map_input_to_action(inputValue)
        self.assertEqual(menuAction, expectedAction)


if __name__ == '__main__':
    unittest.main()