import unittest
from unittest.mock import MagicMock, call
from parameterized import parameterized

from menu.menus import MenuNode, MenuNodeType, SelectionOption
from menu.displays import TerminalDisplay


class TestTerminalDisplay(unittest.TestCase):

    def setUp(self):
        self._terminalDisplay = TerminalDisplay()

    def test_display_menu_exception(self):
        emptyMenuNode = MenuNode(id=None, menuNodeType=None, selectionOptions=None, confirm=True, executorNodeId=None, isRoot=False)
        with self.assertRaises(Exception) as ecm:
            self._terminalDisplay.display_menu(emptyMenuNode, None)
        
        actualException = ecm.exception
        self.assertEqual(str(actualException), "Must have selection options to display")

    def test_display_menu(self):
        displayName1 = "Option1"
        displayName2 = "Option2"
        selOption1 = SelectionOption(id="1234", displayName=displayName1)
        selOption2 = SelectionOption(id="4321", displayName=displayName2)
        selectionOptions = [selOption1, selOption2]
        menuNodeWithSelections = MenuNode(id=None, menuNodeType=MenuNodeType.SELECTION, selectionOptions=selectionOptions, confirm=False, executorNodeId=None, isRoot=False)

        self._terminalDisplay._output_data = MagicMock()

        self._terminalDisplay.display_menu(menuNodeWithSelections, 1)

        calls = [call('  0: Option1'), call('> 1: Option2')]
        self._terminalDisplay._output_data.assert_has_calls(calls)


class TestBoundedCharacterDisplay(unittest.TestCase):

    def test_prepare_selection_menu_display_buffer(self):
        #TODO
        # prepare_selection_menu_display_buffer(self, selectionOptions: List[SelectionOption], windowTop: int, windowBottom: int, cursorPos: int) -> List[bytearray]:
        pass

    def test_prepare_output_display_buffer(self):
        #TODO
        # prepare_output_display_buffer(self, output: str, numRows, numColumns) -> List[bytearray]:
        pass

    def test_set_window(self):
        #TODO
        # Should we test this if set_window() only modifies 'private' attributes?
        pass

class TestBoundedCharacterTerminalDisplay(unittest.TestCase):

    def test_exception_num_rows_zero(self):
        #TODO
        pass
    
    def test_exception_num_columns_zero(self):
        #TODO
        pass

    def test_display_menu_exception(self):
        #TODO
        pass

    def test_display_output_not_called(self):
        #TODO
        # prepare_output_display_buffer  NOT called?
        pass

if __name__ == '__main__':
    unittest.main()