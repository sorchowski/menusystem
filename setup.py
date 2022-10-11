
import os
from setuptools import setup

# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name = "Simple Menu System",
    version = "0.0.1",
    author = "Stephen Orchowski",
    author_email = "steveoaz@gmail.com",
    description = ("A simple menuing system for triggering the execution of scripts (or methods) via user input"),
    license = "TODO",
    keywords = "menu raspberrypi lcd button terminal keyboard",
    url = "http://packages.python.org/an_example_pypi_project",
    packages=['menu', 'menu.action', 'menu.display', 'menuservice', 'test', 'test.action', 'test.display'],
    include_package_data=True,
    install_requires = [
        'RPi.GPIO',
        'sparkfun-qwiic-i2c',
        'sparkfun-qwiic-serlcd'
    ],
    long_description=read('README.md'),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "License :: OSI Approved :: BSD License",
        "License :: Free for non-commercial use"
    ],
)
