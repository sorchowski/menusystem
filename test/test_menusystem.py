import unittest
from unittest.mock import Mock, call

from menu.menusystem import MenuSystem
from menu.menus import MenuNode, MenuNodeType, MenuDestination
from menu.menus import Executor
from menu.action.menuaction import MenuAction

class TestMenuSystem(unittest.TestCase):

    def test_handle_confirmation_yes_success(self):

        mockMenus=Mock()
        mockExecutor=Mock()
        mockNavigator=Mock()
        mockDisplay = Mock()
        mockActionQueue = Mock()
        mockMenuAction = Mock()

        menuSystem = MenuSystem(menus=mockMenus,executor=mockExecutor,navigator=mockNavigator,display=mockDisplay,actionQueue=mockActionQueue,menuAction=mockMenuAction)

        mockHandleYesExecutor = Mock()
        mockHandleYesExecutor.execute.return_value = 'test_result'
        result = menuSystem.handle_confirmation_yes(savedExecutorNodeId='test-executor-id', executor=mockHandleYesExecutor)
        self.assertEqual(result, 'test_result')

    def test_handle_confirmation_yes_missing_executor_node(self):

        mockMenus=Mock()
        mockExecutor=Mock()
        mockNavigator=Mock()
        mockDisplay = Mock()
        mockActionQueue = Mock()
        mockMenuAction = Mock()

        menuSystem = MenuSystem(menus=mockMenus,executor=mockExecutor,navigator=mockNavigator,display=mockDisplay,actionQueue=mockActionQueue,menuAction=mockMenuAction)

        mockHandleYesExecutor = Mock()
        mockHandleYesExecutor.execute.return_value = 'test_result'
        with self.assertRaises(Exception) as ecm:
            menuSystem.handle_confirmation_yes(executor=mockHandleYesExecutor)
        actualException = ecm.exception
        self.assertEqual(str(actualException), "missing required kwargs value: savedExecutorNodeId")

    def test_handle_confirmation_yes_missing_executor_object(self):

        mockMenus=Mock()
        mockExecutor=Mock()
        mockNavigator=Mock()
        mockDisplay = Mock()
        mockActionQueue = Mock()
        mockMenuAction = Mock()

        menuSystem = MenuSystem(menus=mockMenus,executor=mockExecutor,navigator=mockNavigator,display=mockDisplay,actionQueue=mockActionQueue,menuAction=mockMenuAction)

        mockHandleYesExecutor = Mock()
        mockHandleYesExecutor.execute.return_value = 'test_result'
        with self.assertRaises(Exception) as ecm:
            menuSystem.handle_confirmation_yes(savedExecutorNodeId='test-executor-id')
        actualException = ecm.exception
        self.assertEqual(str(actualException), "missing required kwargs value: executor")

    def test_display_selection(self):

        menuNode = MenuNode(id="test-id", menuNodeType=MenuNodeType.SELECTION, selectionOptions=None,confirm=False,executorNodeId=None,isRoot=False)

        mockMenus=Mock()
        mockExecutor=Mock()
        mockNavigator=Mock(current_menu_node=menuNode, cursor_position=0)
        mockDisplay = Mock()
        mockActionQueue = Mock()
        mockMenuAction = Mock()

        menuSystem = MenuSystem(menus=mockMenus,executor=mockExecutor,navigator=mockNavigator,display=mockDisplay,actionQueue=mockActionQueue,menuAction=mockMenuAction)

        menuSystem.display()
        mockDisplay.display_menu.assert_called_with(menuNode, 0)

    def test_display_output(self):

        menuNode = MenuNode(id="test-id", menuNodeType=MenuNodeType.OUTPUT, selectionOptions=None,confirm=False,executorNodeId=None,isRoot=False)

        mockMenus=Mock()
        mockExecutor=Mock()
        mockNavigator=Mock(current_menu_node=menuNode)
        mockDisplay = Mock()
        mockActionQueue = Mock()
        mockMenuAction = Mock()

        menuSystem = MenuSystem(menus=mockMenus,executor=mockExecutor,navigator=mockNavigator,display=mockDisplay,actionQueue=mockActionQueue,menuAction=mockMenuAction)

        menuSystem._executionResult = Executor.ExecutionResult(output="test-output", returnCode=0, postExecuteMenuDestination=MenuDestination.POST_EXECUTE_OUTPUT)

        menuSystem.display()
        mockDisplay.display_output.assert_called_with(menuNode, "test-output")

    def test_handle_execution_node_confirm(self):

        mockMenus=Mock()
        mockExecutor=Mock()
        mockNavigator=Mock()
        mockDisplay = Mock()
        mockActionQueue = Mock()
        mockMenuAction = Mock()

        menuSystem = MenuSystem(menus=mockMenus,executor=mockExecutor,navigator=mockNavigator,display=mockDisplay,actionQueue=mockActionQueue,menuAction=mockMenuAction)

        executionNode = MenuNode(id="test-id", menuNodeType=MenuNodeType.EXECUTION, selectionOptions=None, confirm=True, executorNodeId="test-executor-node=id", isRoot=False)
        menuSystem.handle_execution_node(executionNode)
        mockNavigator.navigate_to_confirmation_menu.assert_called()

    def test_handle_execution_node_nonconfirm(self):

        mockMenus=Mock()
        mockExecutor=Mock()
        mockNavigator=Mock()
        mockDisplay = Mock()
        mockActionQueue = Mock()
        mockMenuAction = Mock()

        menuSystem = MenuSystem(menus=mockMenus,executor=mockExecutor,navigator=mockNavigator,display=mockDisplay,actionQueue=mockActionQueue,menuAction=mockMenuAction)

        executionNode = MenuNode(id="test-id", menuNodeType=MenuNodeType.EXECUTION, selectionOptions=None, confirm=False, executorNodeId="test-executor-node=id", isRoot=False)
        executionResult = Executor.ExecutionResult(output="test-output", returnCode=0, postExecuteMenuDestination=MenuDestination.LAST_SELECT_OPTION_MENU)
        mockExecutor.execute.return_value = executionResult
        menuSystem.handle_execution_node(executionNode)
        mockNavigator.navigate_to_last_selection_menu.assert_called()

    def test_run_immediate_quit(self):

        menuNode = MenuNode(id="test-id", menuNodeType=MenuNodeType.SELECTION, selectionOptions=None,confirm=False,executorNodeId=None,isRoot=False)

        mockMenus=Mock()
        mockExecutor=Mock()
        mockNavigator=Mock(current_menu_node=menuNode, cursor_position=0)
        mockDisplay = Mock()
        mockActionQueue = Mock()
        mockMenuAction = Mock()

        menuSystem = MenuSystem(menus=mockMenus,executor=mockExecutor,navigator=mockNavigator,display=mockDisplay,actionQueue=mockActionQueue,menuAction=mockMenuAction)

        mockActionQueue.get.side_effect = [MenuAction.Action.QUIT]

        menuSystem.run()

        mockMenuAction.start.assert_called()
        mockActionQueue.task_done.assert_called()
        mockDisplay.display_menu.assert_called()
        mockMenuAction.stop.assert_called()


    def test_run_navigate_up(self):

        menuNode = MenuNode(id="test-id", menuNodeType=MenuNodeType.SELECTION, selectionOptions=None,confirm=False,executorNodeId=None,isRoot=False)

        mockMenus=Mock()
        mockExecutor=Mock()
        mockNavigator=Mock(current_menu_node=menuNode, cursor_position=0)
        mockDisplay = Mock()
        mockActionQueue = Mock()
        mockMenuAction = Mock()

        menuSystem = MenuSystem(menus=mockMenus,executor=mockExecutor,navigator=mockNavigator,display=mockDisplay,actionQueue=mockActionQueue,menuAction=mockMenuAction)

        mockActionQueue.get.side_effect = [MenuAction.Action.UP, MenuAction.Action.QUIT]

        menuSystem.run()

        mockMenuAction.start.assert_called()
        mockActionQueue.task_done.assert_has_calls([call(), call()])
        mockNavigator.scroll_up.assert_called()
        mockDisplay.display_menu.assert_has_calls([call(menuNode, 0)])
        self.assertEqual(mockDisplay.display_menu.call_count, 2)
        mockMenuAction.stop.assert_called()


if __name__ == '__main__':
    unittest.main()