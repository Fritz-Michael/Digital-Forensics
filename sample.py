
import string
import time
import datetime
import os
import platform
import operator
import threading
import binascii
import glob
import sys
from ctypes import windll
import ctypes
import multiprocessing
from multiprocessing import Manager
import struct
from easygui import *
from PyQt5.QtWidgets import QApplication, QProgressBar, QWidget, QPushButton, QMainWindow, QLabel
from PyQt5.QtCore import QBasicTimer, QCoreApplication
from WindowsFunctions import *


if __name__ == '__main__':
	getmetadata('\\\\.\\C:','C',)