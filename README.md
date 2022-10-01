
Virtualenv:

    python3 -m venv /path/to/new/virtual/environment
    /path/to/new/virtual/environment/activate

unit tests everywhere!

add note to setup.py about needing to perform: sudo apt install python-dev-is-python3 before running pytho setup.py install

choose oss license

add logging

add try/catch around main menusystem::run() loop for graceful shutdown (or continuous operation?)?

Add README.md

    section on dependencies
        sudo pip install RPi.GPIO
        sudo pip install sparkfun-qwiic-i2c
        sudo pip install sparkfun-qwiic-serlcd
    
        For Windows:
            pip install RPi.GPIO will require Windows build tools: https://visualstudio.microsoft.com/visual-cpp-build-tools/
            

    structure of menu system

        Display
            TerminalDisplay
            BoundedCharacterDisplay
                BoundedCharacterTerminalDisplay
                Sparkfun4x20LCDDisplay

        MenuAction
            KeyboardMenuAction
            RPiButtonBoardMenuAction

        executors
            method vs script
            registering methods

        menunodes
        special nodes
            execution, selection, output
            ROOT
            OUTPUT
            CONFIRMATION
            NO
            YES

    Special rules when defining nodes?
        selection nodes must have at least one selection option

    How to execute tests?

    Explain necesity of running rpi menu service as root (button gpio access).

    Future improvements
        Think about adding a timeout to the queue.get() so that the main run method doesn't block forever if the service should stop
        Handle control-c for KeyboardMenuAction
        Refine setup.py to be compatible with setuptools or run as pip install
        Add ability to scroll through output of script or method
        Add ability to return to previous menu (outside of confirmation menu "no") via left button press


