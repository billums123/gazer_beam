# import serial
# import time
# if __name__ == '__main__':
#     ser = serial.Serial('/dev/ttyACM0', 9600,timeout=2)
#     ser.flush() #clear out buffer

#     while True:
#         ser.write(b"on\n")
#         time.sleep(1)
#         ser.write(b"off\n")
#         time.sleep(1)

import serial
from tkinter import *
from tkinter import messagebox

from pygame import mixer
dirName = '/home/pi/Desktop/Python Scripts/'
mixer.init()
mixer.music.load(dirName + 'audio/audio2.mp3')

def init(win):
    win.title("Project Gazer Beam")
    win.minsize(500, 100)
    btn1.pack()
    btn2.pack()

def ledOn():
    ser.write(b'on\n')

#     messagebox.showinfo("Hello", "Pleased to meet you!")
def ledOff():
    ser.write(b'off\n')

def playMusic():
        mixer.music.play(-1)

def pauseMusic():
    mixer.music.pause()

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
btn1 = Button(win, text="Turn On LED", command=ledOn)
btn2 = Button(win, text="Turn Off LED", command=ledOff)


# initialise and start main loop
init(win)

frame3 = Frame(win) #select Difficulty Frame
btn_change_to_select_song = Button(frame3, text="Back")
btn_change_to_select_song.grid(column=3, row=5)
if __name__ == '__main__':
    ser = serial.Serial('/dev/ttyACM0',9600,timeout=1)
    ser.flush()
    musicPlaying = False
    frame3.pack(fill='both', expand=1)

    while True:
        print(ser.in_waiting)
        if ser.in_waiting > 0:
            win.update()
            LDR_value = ser.readline().decode('utf-8',errors='replace').strip()
            if musicPlaying == True:
                if LDR_value == "play music":
                    playMusic()
                    musicPlaying = False
            elif musicPlaying == False:
                if LDR_value == "pause music":
                    pauseMusic()
                    musicPlaying = True

            print(LDR_value)

win.mainloop()


