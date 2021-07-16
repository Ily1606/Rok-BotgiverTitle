import re
from time import sleep
import cv2 as cv
import numpy as np
from PIL import Image
from ppadb.client import Client
from pytesseract import pytesseract
import json

#img = cv.imread('resources/Training/ProFileUser.png',0)
#img = cv.resize(img, None, fx = 2, fy = 2, interpolation = cv.INTER_CUBIC)
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
    with open('screen.png', 'wb') as f:
        f.write(image)
device = connect_device()
def converImagePilToCV(ImagePIL):
    open_cv_image = np.array(ImagePIL) 
    # Convert RGB to BGR 
    open_cv_image = open_cv_image[:, :, ::-1].copy()
    return open_cv_image
def getUserProfile(image):
    img = converImagePilToCV(image)
    data = pytesseract.image_to_data(img, lang='eng', config='--psm 6',output_type='dict')
    if detectIsProFile(data) is True:
        idUser = getIdUser()
        userName = getUserName()
        #it okay, im ready push it to Queue
        PushToQueue(idUser,userName)
        return True
    else:
        print("Is not profile user!!!")
        return False
def detectIsProFile(data):
    result = False
    for i in range(0, len(data["text"])):
        if data["text"][i] == "GOVERNOR":
            if data["text"][i+1] == "PROFILE":
                result = True
                break
    return result
def getIdUser():
    global img
    coord_channel_Id = (778,230,1000,265)
    idUser = -1
    ImageChannelID = img.crop(coord_channel_Id)
    ImageChannelID = converImagePilToCV(ImageChannelID)
    cv.imshow("result",ImageChannelID)
    cv.waitKey(0)
    data = pytesseract.image_to_data(ImageChannelID, lang='eng', config='--psm 10 --oem 3 -c tessedit_char_whitelist=0123456789',output_type='dict')
    print(data)
    for item in data["text"]:
        if item != '':
            idUser = int(re.search(r'\d+', item).group())
            break
    return idUser
def getUserName():
    global img
    coord_channel_UserName = (645,262,990,300)
    ImageChannelUserName = img.crop(coord_channel_UserName)
    data = pytesseract.image_to_data(ImageChannelUserName, lang='eng', config='--psm 6',output_type='dict')
    UserName = ""
    for item in data["text"]:
        if item != '':
            UserName += item
    return UserName
def PushToQueue(id,username):
    global dukeQueue,coord_channel_close
    dukeQueue = {"id": id,"username": username}
    device.input_tap(coord_channel_close[0],coord_channel_close[1])
take_screenshot(device=device)
sleep(1)
img = Image.open('screen.png')
coord_channel_Target = (600,82,990,130) #left top right bottom
imageChannelTarget = img.crop(coord_channel_Target)
dukeQueue = {}
coord_channel_close = (1365,105)
getUserProfile(imageChannelTarget)
print(dukeQueue)
