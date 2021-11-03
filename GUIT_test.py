import tkinter as tk
from pygame import mixer
dirName = '/home/pi/Desktop/Python Scripts/audio'
mixer.init()
mixer.music.load(dirName + '/audio2.wav')

root = tk.Tk()
root.grid_rowconfigure(0, weight=1)
root.columnconfigure(0, weight=1)

frame_main = tk.Frame(root, bg="gray")
frame_main.grid(sticky='news')

label1 = tk.Label(frame_main, text="Label 1", fg="green")
label1.grid(row=0, column=0, pady=(5, 0), sticky='nw')

label2 = tk.Label(frame_main, text="Label 2", fg="blue")
label2.grid(row=1, column=0, pady=(5, 0), sticky='nw')

label3 = tk.Label(frame_main, text="Label 3", fg="red")
label3.grid(row=3, column=0, pady=5, sticky='nw')

# Create a frame for the canvas with non-zero row&column weights
frame_canvas = tk.Frame(frame_main)
frame_canvas.grid(row=2, column=0, pady=(5, 0), sticky='nw')
frame_canvas.grid_rowconfigure(0, weight=1)
frame_canvas.grid_columnconfigure(0, weight=1)
# Set grid_propagate to False to allow 5-by-5 buttons resizing later
frame_canvas.grid_propagate(False)

# Add a canvas in that frame
canvas = tk.Canvas(frame_canvas, bg="yellow")
canvas.grid(row=0, column=0, sticky="news")

# Link a scrollbar to the canvas
vsb = tk.Scrollbar(frame_canvas, orient="vertical", command=canvas.yview)
vsb.grid(row=0, column=1, sticky='ns')
canvas.configure(yscrollcommand=vsb.set)

# Create a frame to contain the buttons
frame_buttons = tk.Frame(canvas, bg="blue")
canvas.create_window((0, 0), window=frame_buttons, anchor='nw')

def ledOn():
    ser.write(b'on\n')

#     messagebox.showinfo("Hello", "Pleased to meet you!")
def ledOff():
    ser.write(b'off\n')

def playMusic():
        mixer.music.play(-1)

def pauseMusic():
    mixer.music.pause()

# Add 9-by-5 buttons to the frame
rows = 9
columns = 5
buttons = [[tk.Button() for j in range(columns)] for i in range(rows)]
for i in range(0, rows):
    for j in range(0, columns):
        buttons[i][j] = tk.Button(frame_buttons, text=("%d,%d" % (i+1, j+1)), command=playMusic)
        buttons[i][j].grid(row=i, column=j, sticky='news')

# Update buttons frames idle tasks to let tkinter calculate buttons sizes
frame_buttons.update_idletasks()

# Resize the canvas frame to show exactly 5-by-5 buttons and the scrollbar
first5columns_width = sum([buttons[0][j].winfo_width() for j in range(0, 5)])
first5rows_height = sum([buttons[i][0].winfo_height() for i in range(0, 5)])
frame_canvas.config(width=first5columns_width + vsb.winfo_width(),
                    height=first5rows_height)

# Set the canvas scrolling region
canvas.config(scrollregion=canvas.bbox("all"))


# 
# def init(win):
#     win.title("Project Gazer Beam")
root.maxsize(480, 320)
root.minsize(480, 320)
#     btn1.pack()
#     btn2.pack()


# 
# win = Tk()
# 
# # Gets the requested values of the height and widht.
# windowWidth = win.winfo_reqwidth()
# windowHeight = win.winfo_reqheight()
# 
#  # Gets both half the screen width/height and window width/height
# positionRight = int(win.winfo_screenwidth()/2 - windowWidth/2)
# positionDown = int(win.winfo_screenheight()/2 - windowHeight/2)
# 
# # Positions the window in the center of the page.
# win.geometry("+{}+{}".format(positionRight, positionDown))
# 
# # create a button
# btn1 = Button(win, text="Turn On LED", command=ledOn)
# btn2 = Button(win, text="Turn Off LED", command=ledOff)
# 
# 
# # initialise and start main loop
# init(win)


if __name__ == '__main__':
    ser = serial.Serial('/dev/ttyACM0',9600,timeout=1)
    ser.flush()
    musicPlaying = False

    while True:

        if ser.in_waiting > 0:
            win.update()
            LDR_value = ser.readline().decode('utf-8').strip()
            if musicPlaying == True:
                if LDR_value == "play music":
                    playMusic()
                    musicPlaying = False
            elif musicPlaying == False:
                if LDR_value == "pause music":
                    pauseMusic()
                    musicPlaying = True

            print(LDR_value)




# Launch the GUI
root.mainloop()