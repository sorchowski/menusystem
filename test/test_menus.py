import unittest
from unittest.mock import patch

from pathlib import Path

from menu.menus import SelectionOption
from menu.menus import MenuDestination, ExecutorNode, ExecutorNodeType
from menu.menus import Menus, MenuNode, MenuNodeType
from menu.menus import Navigator, Executor

class TestSelectionOption(unittest.TestCase):

    def test_as_selection_option(self):
        testId = '12345'
        testDisplayName = 'test display name'
        inputDict = {}
        inputDict['menuNodeId'] = testId
        inputDict['displayName'] = testDisplayName

        selectionOption = SelectionOption.as_selection_option(inputDict)
        self.assertEqual(selectionOption.id, testId)
        self.assertEqual(selectionOption.display_name, testDisplayName)

class TestExecutorNode(unittest.TestCase):

    def test_as_executor_node(self):
        testType = 'method'
        testDestinationOverride = 'lastSelectOptionMenu'
        testId = '12345'
        testName = 'test executor node'
        inputDict = {}
        inputDict['type'] = testType
        inputDict['destinationOverride'] = testDestinationOverride
        inputDict['_id_'] = testId
        inputDict['name'] = testName

        executorNode = ExecutorNode.as_executor_node(inputDict)
        self.assertEqual(executorNode.id, testId)
        self.assertEqual(executorNode.name, testName)
        self.assertEqual(executorNode.executor_type, ExecutorNodeType(testType))
        self.assertEqual(executorNode.destination, MenuDestination(testDestinationOverride))

class TestMenuNode(unittest.TestCase):

    def test_as_menu_node_no_id(self):
        inputDict = {}
        inputDict['random'] = 'random test value'
        asMenuNodeResult = MenuNode.as_menu_node(inputDict)
        self.assertEqual(asMenuNodeResult, inputDict)

    def test_as_menu_node(self):
        testSOId = '12345'
        testSODisplayName = 'so display name'
        testSODict = {}
        testSODict['menuNodeId'] = testSOId
        testSODict['displayName'] = testSODisplayName

        testId = 'ROOT'
        testExecutorNodeId = 'testENId'
        testConfirmValue = True
        testType = 'selection'
        inputDict = {}
        inputDict['_id_'] = testId
        inputDict['selectionOptions'] = [testSODict]
        inputDict['executorNodeId'] = testExecutorNodeId
        inputDict['confirm'] = testConfirmValue
        inputDict['type'] = testType

        menuNode = MenuNode.as_menu_node(inputDict)
        self.assertEqual(menuNode.id, testId)
        self.assertEqual(menuNode.executor_id, testExecutorNodeId)
        self.assertEqual(menuNode.type, MenuNodeType.SELECTION)
        self.assertTrue(menuNode.selection_options is not None)
        self.assertEqual(len(menuNode.selection_options), 1) 
        self.assertTrue(menuNode.is_root)
        self.assertTrue(menuNode.is_confirm)
        self.assertEqual(menuNode.type, MenuNodeType('selection'))

class TestMenu(unittest.TestCase):

    def test_valid_menu_init(self):
        menu = Menus("test/test_input_menunode_files/menunodes_valid_init.json")
        self.assertIsNotNone(menu)

    def test_validate_one_root_node_exception(self):
        with self.assertRaises(Exception) as ecm:
            menu = Menus("test/test_input_menunode_files/menunodes_multiple_root.json")

        actualException = ecm.exception
        self.assertEqual(str(actualException), "Duplicates found")

    def test_validate_selection_options_exception(self):
        with self.assertRaises(Exception) as ecm:
            menu = Menus("test/test_input_menunode_files/menunodes_invalid_selection_id.json")

        actualException = ecm.exception
        self.assertEqual(str(actualException), "Selection Option must have valid menu node id BADID")

    def test_validate_executor_menu_nodes_exception(self):
        with self.assertRaises(Exception) as ecm:
            menu = Menus("test/test_input_menunode_files/menunodes_missing_executor_node_id.json")

        actualException = ecm.exception
        self.assertEqual(str(actualException), "Execution type menu nodes must have an executor node id")

    def test_get_menu_node(self):
        testId = "YUAD5J"
        menus = Menus("test/test_input_menunode_files/menunodes_valid_init.json")
        menuNode = menus.get_menu_node(testId)
        self.assertEqual(menuNode.type, MenuNodeType.EXECUTION)
        self.assertEqual(menuNode.id, testId)
        self.assertEqual(menuNode.executor_id, "ER5KI5")

    def test_get_root_menu_node(self):
        menus = Menus("test/test_input_menunode_files/menunodes_valid_init.json")
        menuNode = menus.get_root_menu_node()
        self.assertTrue(menuNode.is_root)
        self.assertEqual(menuNode.id, 'ROOT')

class TestNavigator(unittest.TestCase):

    def test_current_menu_node(self):

        menus = Menus("test/test_input_menunode_files/menunodes_valid_init.json")
        navigator = Navigator(menus)
        menuNode = navigator.current_menu_node
        self.assertEqual(menuNode.id, "ROOT")

    def test_cursor_position(self):

        menus = Menus("test/test_input_menunode_files/menunodes_valid_init.json")
        navigator = Navigator(menus)
        self.assertEqual(navigator.cursor_position, 0)

    def test_home(self):

        menus = Menus("test/test_input_menunode_files/menunodes_valid_init.json")
        navigator = Navigator(menus)
        navigator.home()

        self.assertEqual(navigator.cursor_position, 0)
        menuNode = navigator.current_menu_node
        self.assertEqual(menuNode.id, "ROOT")

    def test_scroll_up(self):

        menus = Menus("test/test_input_menunode_files/menunodes_valid_init.json")
        navigator = Navigator(menus)

        navigator.scroll_up()
        self.assertEqual(navigator.cursor_position, 0)
        navigator.scroll_down()
        navigator.scroll_down()
        navigator.scroll_up()
        self.assertEqual(navigator.cursor_position, 0)

    def test_scroll_down(self):

        menus = Menus("test/test_input_menunode_files/menunodes_valid_init.json")
        navigator = Navigator(menus)

        navigator.scroll_down()
        self.assertEqual(navigator.cursor_position, 1)
        navigator.scroll_down()
        self.assertEqual(navigator.cursor_position, 1)

    def navigate_to_selected_option(self):

        menus = Menus("test/test_input_menunode_files/menunodes_valid_init.json")
        navigator = Navigator(menus)

        navigator.navigate_to_selected_option()
        menuNode = navigator.current_menu_node
        self.assertEqual(menuNode.id, "YUAD5J")

    def navigate_to_confirmation_menu(self):

        menus = Menus("test/test_input_menunode_files/menunodes_valid_init.json")
        navigator = Navigator(menus)

        navigator.navigate_to_selected_option()
        menuNode = navigator.current_menu_node
        self.assertEqual(menuNode.id, "YUAD5J")
        navigator.navigate_to_confirmation_menu()
        self.assertEqual(navigator.current_menu_node.id, "CONFIRMATION")

    def navigate_to_last_selection_menu(self):

        menus = Menus("test/test_input_menunode_files/menunodes_valid_init.json")
        navigator = Navigator(menus)

        # first selection option is a confirm menu option
        navigator.navigate_to_selected_option()
        menuNode = navigator.current_menu_node
        self.assertEqual(menuNode.id, "YUAD5J")
        navigator.navigate_to_confirmation_menu()
        self.assertEqual(navigator.current_menu_node.id, "CONFIRMATION")
        navigator.navigate_to_last_selection_menu()
        self.assertEqual(navigator.current_menu_node.id, "ROOT")

    def navigate_to_post_execute_output(self):

        menus = Menus("test/test_input_menunode_files/menunodes_valid_init.json")
        navigator = Navigator(menus)

        navigator.navigate_to_post_execute_output()

        self.assertEqual(navigator.cursor_position, None)
        self.assertEqual(navigator.current_menu_node.id, "OUTPUT")
        self.assertEqual(navigator.current_menu_node.selection_options, None)


class TestExecutor(unittest.TestCase):

    def test_init_valid(self):

        executor = Executor("test/test_input_executor_files/executors_valid_init.json", Path("test-path"))

    def test_init_invalid(self):

        with self.assertRaises(Exception) as ecm:
            executor = Executor("test/test_input_executor_files/executors_duplicate_nodes.json", Path("test-path"))

        actualException = ecm.exception
        self.assertEqual(str(actualException), "Duplicates found")

    def test_execute_unsupported(self):

        executor = Executor("test/test_input_executor_files/executors_valid_init.json", Path("test-path"))
        testExecutorNode = ExecutorNode("id", None, None, None)
        executor._executors["id"] = testExecutorNode
        with self.assertRaises(Exception) as ecm:
            executor.execute("id", tempArg1="1", tempArg2="2")
        actualException = ecm.exception
        self.assertEqual(str(actualException), "Unsupported execution type")


    @staticmethod
    def handle_confirmation_no(**kwargs) -> Executor.ExecutionResult:
        return Executor.ExecutionResult(output="test-method-output", returnCode=0, postExecuteMenuDestination=MenuDestination.LAST_SELECT_OPTION_MENU)

    def test_execute_method(self):

        executor = Executor("test/test_input_executor_files/executors_valid_init.json", Path("test-path"))
        executor.register_method(self.handle_confirmation_no)
        executionResult = executor.execute("NO", tempArg1="tempArg1")
        self.assertEqual(executionResult.output, "test-method-output")
        self.assertEqual(executionResult.return_code, 0)
        self.assertEqual(executionResult.destination, MenuDestination.LAST_SELECT_OPTION_MENU)

    @patch('subprocess.check_output', return_value="test-output")
    def test_execute_script(self, mockCheckOutputMethod):

        executor = Executor("test/test_input_executor_files/executors_valid_init.json", Path("test-path"))
        executionResult = executor.execute("ER5KI5")
        self.assertEqual(executionResult.output, "test-output")


if __name__ == '__main__':
    unittest.main()