from pathlib import Path

from menu.displays import TerminalDisplay
from menu.menuactions import KeyboardMenuAction
from menu.menusystem import MenuSystem

menuSystem = MenuSystem('menunodes.json', 'executors.json', Path("scripts"), TerminalDisplay(), KeyboardMenuAction())
menuSystem.run()