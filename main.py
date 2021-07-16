from ppadb.client import Client
from PIL import Image
import numpy as np
import time
import cv2 as cv
import pytesseract
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
#device.input_tap(180, 845) #Start tap to chat button
#device.input_swipe(300,400,600,400,1000)
#device.input_roll(300,400)
##device.shell("adb shell input touchscreen swipe 500 500 500 2000")
take_screenshot(device=device)
time.sleep(2)
imageScreen = Image.open('screen.png')        
#imageScreen.crop((120,0,680,40)).save("resources/channels/current-channel.png")
height_of_screen = 890
margin_top_of_channel_list = 45
coord_channel_list = (10,margin_top_of_channel_list,400,height_of_screen) #left top right bottom
imageChannelList = imageScreen.crop(coord_channel_list)
height_of_channel = 85
coord_title_channel = (60,8,390,32)
coord_chat_bar = [670,875]
coord_close_chat_button = [1165,450]

queueDuke = []
img = cv.imread('screen.png')
status = True
markMessageDuke = []
def detection_title(ImagePIL):
    open_cv_image = np.array(ImagePIL) 
    # Convert RGB to BGR 
    open_cv_image = open_cv_image[:, :, ::-1].copy()
    pytesseract.pytesseract.tesseract_cmd = "C:/Program Files (x86)/Tesseract-OCR/tesseract.exe"
  
    text = pytesseract.image_to_string(open_cv_image)
    return text
def actionForDuke():
    print("Start action for duke")
    global queueDuke

    '''for item in queueDuke:
        if'''
def checkStatusBot():
    global status
    if status is False:
        device.input_tap(coord_chat_bar[0],coord_chat_bar[1])
        device.input_text("Bot giver title starting")
        device.input_tap(1565,870)
        status = True
        time.sleep(1)
for coord in range(-2,height_of_screen,height_of_channel):
    channel_item = imageChannelList.crop((0,coord+3,400,coord+85))
    channel_title = channel_item.crop(coord_title_channel)
    title = detection_title(channel_title)
    print(title)
    if "Duke" in title:
        coord_y = coord + margin_top_of_channel_list + 10
        device.input_tap(100,coord_y) #enter the room
        checkStatusBot()
        time.sleep(1)
        actionForDuke()
        break
    else:
        print("NO")
