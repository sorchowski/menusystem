
Virtualenv:

    python3 -m venv /path/to/new/virtual/environment
    /path/to/new/virtual/environment/activate

unit tests everywhere!

add setup.py
    https://setuptools.pypa.io/en/latest/setuptools.html
    https://setuptools.pypa.io/en/latest/userguide/quickstart.html
choose oss license

add logging?

add try/catch around main menusystem::run() loop for graceful shutdown (or continuous operation?)?

add linux systemd service for menusystem
    run as alternate user with root permissions, other than root
    how to run service with sudo access (for rpi buttons)
    how to set permissions of scripts
    need to do anything to handle stop service cleanly?
    How to give main script access to any packages or structure files (i.e. executors.json)

    https://github.com/torfsen/python-systemd-tutorial
    https://www.digitalocean.com/community/tutorials/how-to-use-systemctl-to-manage-systemd-services-and-units
    https://alexandra-zaharia.github.io/posts/stopping-python-systemd-service-cleanly/

get scripts working

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
    