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
def converImagePilToCV(ImagePIL):
    open_cv_image = np.array(ImagePIL) 
    open_cv_image = cv.cvtColor(open_cv_image,cv.COLOR_RGB2BGR)
    #open_cv_image = cv.resize(open_cv_image, None, fx = 2, fy = 2, interpolation = cv.INTER_CUBIC) #zoom x2 image for quality OCR
    return open_cv_image
device = connect_device()
img = Image.open(io.BytesIO(take_screenshot(device)))
img = img.crop((415,45,780,895))
img = converImagePilToCV(img)

text = pytesseract.image_to_data(img, lang='eng',  config='--psm 6',output_type='dict')
print(text)
cv.imshow("test",img)
cv.waitKey(0)