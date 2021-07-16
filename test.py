from datetime import datetime
import io
import random
import re
from time import sleep
import time
import cv2 as cv
import numpy as np
from PIL import Image
from numpy.core.numeric import array_equal
from ppadb.client import Client
from pytesseract import pytesseract

pytesseract.tesseract_cmd = "C:/Program Files (x86)/Tesseract-OCR/tesseract.exe"
def getDataImage(img):
    data = pytesseract.image_to_data(img, lang='eng', config='',output_type='dict')
    return data
pytesseract.tesseract_cmd = "C:/Program Files (x86)/Tesseract-OCR/tesseract.exe"
def connect_device():
    adb = Client(host='127.0.0.1',port=5037)
    devices = adb.devices()
    if len(devices) == 0:
        print("No Devices Attached")
        quit()
    return devices[0]
def take_screenshot(device):
    image = device.screencap()
    return image
device = connect_device()
img = Image.open(io.BytesIO(take_screenshot(device)))
img.show()