from appium import webdriver
from appium.webdriver.common.appiumby import AppiumBy
from appium.webdriver.common.touch_action import TouchAction
import time
import json
import random
from datetime import datetime
from appium.webdriver.appium_service import AppiumService
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from qt_material import apply_stylesheet
import ui_main
from sys import *
import os
import threading



DESIRED_CAP = {
    "deviceName": "emulator-5554",
    "platformName": 'Android',
}

SERVER_URL = "http://localhost:4723/wd/hub"

PORT = "4723"



ELEMENT_JSON = "element.json"

RANDOM_NUMBER = [0, 0, 1, 1, 2, 2, 3, 3, -1, 10]

def init():
    global SPEED
    SPEED = 1
