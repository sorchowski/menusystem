# from top-level directory, run "python -m unittest discover -s test"
# https://realpython.com/python-testing

# https://github.com/wolever/parameterized
# pip install parameterized


import unittest
from unittest.mock import patch
from parameterized import parameterized

from menu.menuaction import MenuAction
from menu.keyboardmenuaction import KeyboardMenuAction

class TestKeyboardMenuActions(unittest.TestCase):

    @parameterized.expand([
        ("i", MenuAction.Action.UP),
        ("m", MenuAction.Action.DOWN),
        ("j", MenuAction.Action.NONE),
        ("l", MenuAction.Action.SELECT),
        ("s", MenuAction.Action.SELECT),
        ("q", MenuAction.Action.QUIT),
        ("a", MenuAction.Action.HOME),
        ("d", MenuAction.Action.NONE)
    ])
    def test_map_input_to_action(self, inputKey, expectedAction: MenuAction.Action):
        keyboardMA = KeyboardMenuAction()
        menuAction = keyboardMA.map_input_to_action(inputKey)
        self.assertEqual(menuAction, expectedAction)

    @patch('menu.menuactions.KeyboardMenuAction.get_input', return_value='q')
    def test_get_action(self, input_value):
        keyBoardMA = KeyboardMenuAction()
        menuAction = keyBoardMA.get_action()
        self.assertEqual(menuAction, MenuAction.Action.QUIT)

if __name__ == '__main__':
    unittest.main()
