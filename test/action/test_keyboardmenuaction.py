# from top-level directory, run "python -m unittest discover -s test"
# https://realpython.com/python-testing

# https://github.com/wolever/parameterized
# pip install parameterized


import unittest
from unittest.mock import Mock, patch
from parameterized import parameterized
import threading
from queue import Queue

from menu.action.menuaction import MenuAction
from menu.action.keyboardmenuaction import KeyboardMenuAction

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
        actionQueue = Mock()
        keyboardMA = KeyboardMenuAction(actionQueue)
        menuAction = keyboardMA.map_input_to_action(inputKey)
        self.assertEqual(menuAction, expectedAction)


    @patch('menu.action.keyboardmenuaction.KeyboardMenuAction.get_input', return_value='q')
    def test_get_action_quit(self, mockGetEventMethod):

        mockExitEvent = Mock(spec=threading.Event)
        mockExitEvent.is_set.side_effect = [False, True]
        mockActionQueue = Mock(spec=Queue)
        keyBoardMA = KeyboardMenuAction(mockActionQueue)
        with patch.object(keyBoardMA, '_exitEvent', mockExitEvent):
            keyBoardMA.get_actions()

        mockActionQueue.put.assert_called_once_with(MenuAction.Action.QUIT)
        mockExitEvent.set.assert_called_once()

    @patch('menu.action.keyboardmenuaction.KeyboardMenuAction.get_input', return_value='a')
    def test_get_action_non_quit(self, mockGetEventMethod):

        mockExitEvent = Mock(spec=threading.Event)
        mockExitEvent.is_set.side_effect = [False, True]
        mockActionQueue = Mock(spec=Queue)
        keyBoardMA = KeyboardMenuAction(mockActionQueue)
        with patch.object(keyBoardMA, '_exitEvent', mockExitEvent):
            keyBoardMA.get_actions()

        mockActionQueue.put.assert_called_once_with(MenuAction.Action.HOME)
        mockActionQueue.join.assert_called_once()
        mockExitEvent.set.assert_not_called()

if __name__ == '__main__':
    unittest.main()
