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
    # Convert RGB to BGR 
    #open_cv_image = open_cv_image[:, :, ::-1].copy()
    return open_cv_image
device = connect_device()
def clickToTarget(coord):
    device.input_tap(coord[0], coord[1])
    sleep(1)
def getUserProfile(image,fullimg):
    img = converImagePilToCV(image)
    data = pytesseract.image_to_data(img, lang='eng', config='--psm 6',output_type='dict')
    if detectIsProFile(data) is True:
        idUser = getIdUser(fullimg)
        userName = getUserName(fullimg)
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
def getIdUser(img):
    coord_channel_Id = (778,230,1000,265)
    idUser = -1
    ImageChannelID = img.crop(coord_channel_Id)
    ImageChannelID = np.array(ImageChannelID) 
    # Convert RGB to BGR 
    ImageChannelID = ImageChannelID[:, :, ::-1].copy()
    data = pytesseract.image_to_data(ImageChannelID, lang='eng', config='--psm 10 --oem 3 -c tessedit_char_whitelist=0123456789',output_type='dict')
    for item in data["text"]:
        if item != '':
            idUser = int(re.search(r'\d+', item).group())
            break
    return idUser
def getUserName(img):
    coord_channel_UserName = (645,262,990,300)
    ImageChannelUserName = img.crop(coord_channel_UserName)
    ImageChannelUserName.show()
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
def chat(message):
    coord_chat_bar = [670,875]
    device.input_tap(coord_chat_bar[0],coord_chat_bar[1])
    device.input_text(message)
    device.input_tap(1565,870) #click to send button
    device.input_tap(60,25)
    sleep(1)
def randomCode():
    random_code = ""
    for i in range(0,5):
        random_code += chr(random.randrange(97, 97 + 26))
    return random_code
def groupTextFromPos(text,pos):
    res = ""
    for i in range(pos,len(text)):
        if res != "":
            break
        if text[i] != '':
            res += text[i]
    return res        
def getCoordList(data):
    text = data["text"]
    list = []
    info = {}
    for i in range(0,len(text)):
        if text[i] == "Shared":
            if text[i+1] == "a" or text[i+2] == "coordinate." or text[i+2] == "coordinate":
                info["left"] = data["left"][i]
                info["top"] = data["top"][i]
                info["positionInImg"] = i
                res = [False, False]
                for j in range(i+1,len(text)):
                    if text[j] != '':
                        if text[j][0] == "X":
                            info["x"] = text[j]
                            res[0] = True
                        elif text[j][0] == "Y":
                            if(len(text[j]) == 2):
                                info["y"] = text[j] + groupTextFromPos(text,j+1)
                            else:
                                info["y"] = text[j]
                            res[1] = True
                        if res[0] is True and res[1] is True:
                            list.append(info)
                            info = {}
                            break
            else:
                continue
    return list
def getCoordNth(data,pos):
    text = data["text"]
    info = {}
    for i in range(pos,len(text)):
        if text[i] == "Shared":
            if text[i+1] == "a" or text[i+2] == "coordinate." or text[i+2] == "coordinate":
                info["left"] = data["left"][i]
                info["top"] = data["top"][i]
                info["positionInImg"] = i
                res = [False, False]
                for j in range(i+1,len(text)):
                    if text[j] != '':
                        if text[j][0] == "X":
                            info["x"] = text[j]
                            res[0] = True
                        elif text[j][0] == "Y":
                            if(len(text[j]) == 2):
                                info["y"] = text[j] + groupTextFromPos(text,j+1)
                            else:
                                info["y"] = text[j]
                            res[1] = True
                        if res[0] is True and res[1] is True:
                            break
                break
            else:
                continue
    return info
def detectDone():
    word_done = ("done","xong","cảm ơn","thanks")
    time_for_duke = 180
    now = time.time()
    coord_message_list = (415,45,1140,895)
    result = False
    while True:
        img = take_screenshot(device)
        sleep(1)
        current_time = time.time()
        img = Image.open(io.BytesIO(img))
        messageList = img.crop(coord_message_list)
        messageList = converImagePilToCV(messageList)
        messageList = cv.cvtColor(messageList, cv.COLOR_BGR2GRAY)
        threshold_img = cv.threshold(messageList, 0, 255, cv.THRESH_BINARY | cv.THRESH_OTSU)[1]
        #cv.imshow("res",threshold_img)
        #cv.waitKey(0)
        data = getDataImage(threshold_img)
        for i in range(len(data["text"]),0,-1):
            if data["text"][i-1] == "on" and data["text"][i] == "you":
                for j in range(i+1, len(data["text"])):
                    if(data["text"][j].lower() in word_done):
                        print(data["text"][j])
                        result = True
                        break
                break
        if result is True:
            break
        if current_time - now > time_for_duke:
            chat(" Over time, I'm will load next player!!!")
            break
def scrollUp():
    device.input_swipe(950,140,950,550, 1000)
    sleep(1)
def scrollDown():
    device.input_swipe(950,550,950,140, 1000)
    sleep(1)
def scrollDownToFindCoord():
    res = ""
    infoCoord = {}
    def inside():
        nonlocal res, infoCoord
        global info, lastText
        coord_message_list = (415,45,1140,895)
        scrollDown()
        img = take_screenshot(device)
        sleep(1)
        img = Image.open(io.BytesIO(img))
        leftMessage = img.crop(coord_message_list)
        data = getDataImage(leftMessage)
        infoCoords = getCoordList(data)
        print(infoCoords)
        if len(infoCoords) >0:
            for i in range(0,len(infoCoords)):
                if infoCoords[i]["x"] != info["x"] and infoCoords[i]["y"] != info["y"]:
                    infoCoord = infoCoords[i].copy()
                    res = "action"
        if res == "":
            if array_equal(data["text"],lastText):
                res = "refresh"
    while res == "":
        inside()
    if res == "action":
        actionTitle(infoCoord)
    elif res == "refresh":
         reFreshFrame()
def scrollTopToFindCoord(config):
    infoCoord = {}
    res = ""
    def inside(config):
        nonlocal res,infoCoord
        global info, lastText
        coord_message_list = (415,45,1140,895)
        if config is True:
            scrollUp()
        print(config)
        img = take_screenshot(device)
        sleep(1)
        img = Image.open(io.BytesIO(img))
        leftMessage = img.crop(coord_message_list)
        data = getDataImage(leftMessage)
        infoCoords = getCoordList(data)
        print(infoCoords)
        if len(infoCoords) >0:
            for i in range(0,len(infoCoords)):
                if infoCoords[i]["x"] == info["x"] and infoCoords[i]["y"] == info["y"]:
                    if(i == len(infoCoords) - 1): #last_element_in screen
                        lastText = data["text"].copy()
                        res = "crollDown"
                    else:
                        infoCoord = infoCoords[i+1].copy()
                        res = "action"
        if res == "":
            if array_equal(data["text"],lastText):
                res = "refresh"
    inside(config)            
    while res == "":
        inside(True)
    if res == "action":
        actionTitle(infoCoord)
    elif res == "refresh":
         reFreshFrame()
    elif res == "crollDown":
        scrollDownToFindCoord()
def actionTitle(infoCoord):
    global info
    coord_message_list = (415,45,1140,895)
    coord_target_home = (790,460)
    coord_target_profile_info = (935,305)
    coord_target_title = (945,240)
    coord_chat_button = (190,845)
    coord_target_title_duke = (650,495)
    coord_target_title_confirm = (800,800)

    info = infoCoord
    print(info)
    position = ()
    if "positionInImg" in info:
        position = (info["left"], info["top"])
    if len(position):
        position = (position[0]+415, position[1] + 50)
        print(position)
        coord_position_avatar = [position[0] - 45, position[1] - 10]
        print(coord_position_avatar)
        device.input_tap(position[0] + 10, position[1] + 5)
        sleep(5) #wait 5s for loading postion animation
        clickToTarget(coord_target_home)
        sleep(1.5)
        clickToTarget(coord_target_title)
        sleep(1)
        clickToTarget(coord_target_title_duke)
        sleep(0.5)
        clickToTarget(coord_target_title_confirm)
        '''
        take_screenshot(device=device)
        sleep(1)
        img = Image.open('screen.png')
        coord_channel_Target = (600,82,990,130) #left top right bottom
        imageChannelTarget = img.crop(coord_channel_Target)'''
        #if getUserProfile(imageChannelTarget,img) is True:
        device.input_tap(coord_chat_button[0],coord_chat_button[1]) #click to chat button
        sleep(1)
        device.input_swipe(coord_position_avatar[0],coord_position_avatar[1] , coord_position_avatar[0],coord_position_avatar[1], 2500) #Metion user
        sleep(2.5)
        chat(" on you")
        chat(" time for duke is 3 min. I'm waiting in 3 min.")
        detectDone()
        scrollTopToFindCoord(False)
    else:
        print("Nothing see coord!!!")
def makeReFresh():
    infoCoord = {}
    def inside():
        global mark_message
        nonlocal infoCoord
        coord_message_list = (415,45,1140,895)
        img = take_screenshot(device)
        print("OK")
        sleep(1)
        img = Image.open(io.BytesIO(img))
        leftMessage = img.crop(coord_message_list)
        imgLeft = converImagePilToCV(leftMessage)
        data = getDataImage(imgLeft)
        #print(data)
        for i in range(0,len(data["text"])):
            if mark_message in data["text"][i] or mark_message == data["text"][i]:
                infoCoord = getCoordNth(data,i)
                break
        return infoCoord
    while True:
        infoCoord = inside()
        if "x" in infoCoord:
            break
    actionTitle(infoCoord)    
def reFreshFrame():
    infoCoords = {}
    res = ""
    def inside():
        global info
        nonlocal res,infoCoords
        coord_message_list = (415,45,1140,895)
        img = take_screenshot(device)
        sleep(1)
        img = Image.open(io.BytesIO(img))
        leftMessage = img.crop(coord_message_list)
        data = getDataImage(leftMessage)
        infoCoords = getCoordList(data)
        print(infoCoords)
        if len(infoCoords) >0:
            for i in range(0,len(infoCoords)):
                if infoCoords[i]["x"] == info["x"] and infoCoords[i]["y"] == info["y"]:
                    if(i == len(infoCoords) - 1): #last_element_in screen
                        res = ""
                    else:
                        res = "action"
                        infoCoords = infoCoords[i+1].copy()
    while res == "":
        sleep(2)
        inside()
    if res == "action":
        actionTitle(infoCoords)
coord_left_message = (415,50,760,840)
coord_channel_close = (1365,105)
#info = {'left': 77, 'top': 396, 'positionInImg': 39, 'x': 'X:781', 'y': 'Y:508)'}
#mark_message = "zjjmw"
lastText = []
mark_message = randomCode()
chat("Bot starting with code: "+mark_message)
info = {}
makeReFresh()
        
#def getIDUser(image):
