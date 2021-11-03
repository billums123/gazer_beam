#!/usr/bin/python3
import serial
import time
from tkinter import *
from tkinter import messagebox
from pygame import mixer
dirName = '/home/pi/Desktop/Python Scripts/'
mixer.init()

# song2 = mixer.music.load(dirName + '/chael-sparks.mp3')
# mixer.music.play(-1)

ser = serial.Serial('/dev/ttyACM0', 9600, timeout=5)
def init(win):
    win.title("Project Gazer Beam")
    win.minsize(500, 100)
    btn1.pack()
    btn2.pack()

# button callback
def ledOn():
    print(ser.readline().decode("utf-8").strip())
    ser.write(b'set on\n')
    song1 = mixer.music.load(dirName + '/audio2.wav')
    mixer.music.play(-1)
#     messagebox.showinfo("Hello", "Pleased to meet you!")
def ledOff():
    print(ser.readline().decode("utf-8").strip())
    ser.write(b'set off\n')
    mixer.music.stop()
    song2 = mixer.music.load(dirName + '/chael-sparks.mp3')
    mixer.music.play(-1)


# create top-level window
win = Tk()

# Gets the requested values of the height and widht.
windowWidth = win.winfo_reqwidth()
windowHeight = win.winfo_reqheight()

 # Gets both half the screen width/height and window width/height
positionRight = int(win.winfo_screenwidth()/2 - windowWidth/2)
positionDown = int(win.winfo_screenheight()/2 - windowHeight/2)

# Positions the window in the center of the page.
win.geometry("+{}+{}".format(positionRight, positionDown))

# create a button
btn1 = Button(win, text="Turn On Led", command=ledOn)
btn2 = Button(win, text="Turn Off Led", command=ledOff)

# initialise and start main loop
init(win)
mainloop()

#read  from Arduino
# input_str = ser.readline()
# print("Read input " + input_str.decode("utf-8").strip() + " from Arduino")

while 1:
#     write something back
    ser.write(b'status\n')
    input_str = ser.readline().decode("utf-8").strip()
    if (input_str == ""):
        print (".")
    else:
        print("Read input back: " + input_str)

     time.sleep(5)

#     ser.write(b'set on\n')
#     input_str = ser.readline().decode("utf-8").strip()
#     if (input_str == ""):
#         print(".")
#     else:
#         print ("Read input back: " + input_str)

#     time.sleep(5)

#     ser.write(b'set off\n')
input_str = ser.readline().decode("utf-8").strip()
if (input_str == ""):
    print(".")
else:
    print ("Read input back: " + input_str)
time.sleep(5)