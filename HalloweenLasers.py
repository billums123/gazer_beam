ACM0 = True
setToFullScreen = False
touchScreenMode = True
import json
import serial
import tkinter as tk
from tkinter import PhotoImage
import tkinter.font as font
import time
import pygame
import os #used for counting number of audio files
from PIL import Image, ImageTk #pillow used for images
from datetime import datetime
from time import strftime
from time import gmtime
from pygame import mixer
pygame.mixer.pre_init(48000, -16, 2, 2048)
pygame.mixer.init()
pygame.init()

musicTracksDirectory = '/home/pi/Desktop/Python Scripts/halloween_audio'
projectDirectory = '/home/pi/Desktop/Python Scripts/'
leaderboardFile = '/home/pi/Desktop/Python Scripts/highscore/leaderboard.json'
# easyLeaderboard = '/home/pi/Desktop/Python Scripts/easyLeaderboard.json'
# mediumLeaderboard = '/home/pi/Desktop/Python Scripts/easyLeaderboard.json'
# hardLeaderboard = '/home/pi/Desktop/Python Scripts/easyLeaderboard.json'
# xtremeLeaderboard = '/home/pi/Desktop/Python Scripts/easyLeaderboard.json'
# scoreData = json.loads('highscore/leaderboard.json')
# with open(leaderboardFile) as f:
#     data1 = json.load(leaderboardFile)
# print((data1['leaderboards']['easy']))

global frame5
global gameStartFlag
global highScoreNameIndex


gameStartFlag = True
highScoreNameIndex = 0

root = tk.Tk()
if touchScreenMode == True:
    root.config(cursor="none")
root.wm_attributes('-type','splash')#remove window title


#import images used
gazerbeam_logo = PhotoImage(file=projectDirectory + 'images/gazerbeam.png')
backButton  = PhotoImage(file=projectDirectory + 'menu/backArrow.png')
youWinMessage = PhotoImage(file=projectDirectory + 'victory/youWin.png')
gameoverMessage =  PhotoImage(file=projectDirectory + 'gameover/game_over.png')
backspaceIcon = PhotoImage(file=projectDirectory + 'highscore/backspaceIcon.png')
checkMarkIcon = PhotoImage(file=projectDirectory + 'highscore/checkMark.png')


##Create the multiple frames
frame1 = tk.Frame(root, bg="#fdfce9") #intro Frame
frame1.columnconfigure((0,1),weight=1)
frame1.rowconfigure(0,weight=1)
frame1.rowconfigure(1,weight=1)

frame2 = tk.Frame(root, bg="#73787C") #select Song Frame
# frame2.columnconfigure((0),weight=1)
frame2.columnconfigure((0,1,2),weight=4)
frame2.rowconfigure((0,1,2),weight=1)

frame3 = tk.Frame(root) #select Difficulty Frame
frame3.columnconfigure(0,weight=1)
frame3.columnconfigure(1,weight=5)
frame3.rowconfigure((0,1,2,3),weight=1)

frame4 = tk.Frame(root,bg="#73787C") #start Game Frame
frame4.columnconfigure(0,weight=1)
frame4.columnconfigure(1,weight=5)
frame4.rowconfigure((0,1,2),weight=1)

frame5 = tk.Frame(root, bg="#73787C") #game in progress frame
frame5.columnconfigure(0,weight=1)
frame5.rowconfigure(0,weight=1)
frame5.rowconfigure(1,weight=3)

frame6 = tk.Frame(root,bg="#73787C") #game failed frame
frame6.columnconfigure(0,weight=1)
frame6.rowconfigure(0,weight=3)
frame6.rowconfigure(1,weight=2)
frame6.rowconfigure(2,weight=1)

frame7 = tk.Frame(root, bg="#73787C") #game success frame
frame7.rowconfigure(0,weight=3)
frame7.rowconfigure(1,weight=2)
frame7.rowconfigure(2,weight=2)
frame7.rowconfigure(3,weight=1)

frame8 = tk.Frame(root) #select Leaderboard Frame
frame8.columnconfigure(0,weight=1)
frame8.columnconfigure(1,weight=5)
frame8.rowconfigure((0,1,2,3),weight=1)

frame9 = tk.Frame(root, bg="#6BAA41") #select Easy Leaderboard Frame
frame9.columnconfigure(0,weight=1)
frame9.columnconfigure(1,weight=1)
frame9.columnconfigure(2,weight=2)
frame9.columnconfigure(3,weight=4)
frame9.rowconfigure((0,1,2,3,4),weight=1)

frame10 = tk.Frame(root, bg="#DEA336") #select Medium Leaderboard Frame
frame10.columnconfigure(0,weight=1)
frame10.columnconfigure(1,weight=1)
frame10.columnconfigure(2,weight=2)
frame10.columnconfigure(3,weight=4)
frame10.rowconfigure((0,1,2,3,4),weight=1)

frame11 = tk.Frame(root, bg="#FF7518") #select Hard Leaderboard Frame
frame11.columnconfigure(0,weight=1)
frame11.columnconfigure(1,weight=1)
frame11.columnconfigure(2,weight=2)
frame11.columnconfigure(3,weight=4)
frame11.rowconfigure((0,1,2,3,4),weight=1)

frame12 = tk.Frame(root, bg="#D94E47") #select Xtreme Leaderboard Frame
frame12.columnconfigure(0,weight=1)
frame12.columnconfigure(1,weight=1)
frame12.columnconfigure(2,weight=2)
frame12.columnconfigure(3,weight=4)
frame12.rowconfigure((0,1,2,3,4),weight=1)

frame13 = tk.Frame(root, bg="#6BAA41") #Input highscore name frame 1
frame13.columnconfigure((0,4),weight=1)
frame13.columnconfigure((1,2,3),weight=4)
frame13.rowconfigure((0,1,2,3),weight=1)
nameEntry1 = tk.Entry(frame13, font = "Verdana 25")
nameEntry1.grid(row=0, column=1, columnspan=3, sticky="news")

frame14 = tk.Frame(root, bg="#6BAA41") #Input highscore name frame 2
frame14.columnconfigure((0,4),weight=1)
frame14.columnconfigure((1,2,3),weight=4)
frame14.rowconfigure((0,1,2,3),weight=1)
nameEntry2 = tk.Entry(frame14, font = "Verdana 25")
nameEntry2.grid(row=0, column=1, columnspan=3, sticky="news")


counter = 25200
running = False
def counter_label(label):
    def count():
        if running:
            global counter
            global playerTime


            tt = datetime.fromtimestamp(counter)
            string = tt.strftime("%M:%S")
            display=string
            playerTime = display

            label['text']=display   # Or label.config(text=display)

            # label.after(arg1, arg2) delays by
            # first argument given in milliseconds
            # and then calls the function given as second argument.
            # Generally like here we need to call the
            # function in which it is present repeatedly.
            # Delays by 1000ms=1 seconds and call count again.
            label.after(1000, count)
            counter += 1

    # Triggering the start of the counter.
    count()

def StartTimer(label):
    global running
    
    running=True
    counter_label(label)

# Stop function of the stopwatch
def StopTimer():
    global running
    running = False
    

# Reset function of the stopwatch
def ResetTimer(label):
    global counter
    counter=25200



#Count number of audio files
def count_number_of_files(directoryFilepath):

    numberOfFiles = 0
    for path in os.listdir(directoryFilepath):
        if os.path.isfile(os.path.join(directoryFilepath,path)):
            numberOfFiles += 1
    return numberOfFiles


def pauseMusic():
    pygame.mixer.music.pause()

def stopMusic():
    pygame.mixer.music.stop()

def playMusic(duration):
    if duration == "forever":
        duration = -1
    pygame.mixer.music.play(duration)
   

def loadMusic(audioFile):
    pygame.mixer.music.load(audioFile)
    
def playLoadScreenMusic():
    loadMusic(projectDirectory + 'loadScreen/loadScreenAudio.mp3')
    playMusic(1)

    
def playMenuMusic():
    loadMusic(projectDirectory + 'halloween_menu/menuMusic.mp3')
    playMusic("forever")
#stopwatch functions
# start function of the stopwatch

def center_window():
    """
    Centers window
"""
    width, height = 480, 320
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x_cord = int((screen_width/2) - (width/2))
    y_cord = int((screen_height/2) - (height/2))
    root.geometry("{}x{}+{}+{}".format(width,
                                           height,
                                           x_cord,
                                           y_cord))
def change_between_frames(currentFrame, newFrame):
    currentFrame.forget()
    newFrame.pack(fill='both', expand=1)

def selectMusic(trackNumber):
    global selected_song
    selected_song = musicTracksDirectory + '/audio' + str(trackNumber) + '.mp3'
    change_between_frames(frame2, frame3)


def selectDifficultyLevel(difficultyLevel):
    change_between_frames(frame3, frame4)
    global chosenDifficultyLevel
    if difficultyLevel == 0:
        chosenDifficultyLevel = b'easy\n'
    if difficultyLevel == 1:
        chosenDifficultyLevel = b'intermediate\n'
    if difficultyLevel == 2:
        chosenDifficultyLevel = b'hard\n'
    if difficultyLevel == 3:
        chosenDifficultyLevel = b'xtreme\n'
    
#     chosenDifficultyLevel = difficultyLevel
def getTimeAsInt(time_str):
    m, s = time_str.split(':')
    return int(m) * 60 + int(s)

def getTimeAsString(time_int):
    return strftime("%M:%S", gmtime(int(time_int)))

def startGameCountdown():
    global countdownTimer
    global timerLabel
    countdownTimer = tk.Label(frame5,text='',bg="#73787C", fg="#fdfce9", font="Verdana 80 bold")
    if (chosenDifficultyLevel == b'easy\n'):
        highScoreLabel = tk.Label(frame5, text="High Score: " + getTimeAsString(easyLeaderboard[0]["score"]), bg="#73787C", fg="#fdfce9", font="Verdana 20 bold").grid(column=0,row=0)
    if (chosenDifficultyLevel == b'intermediate\n'):
        highScoreLabel = tk.Label(frame5, text="High Score: " + getTimeAsString(intermediateLeaderboard[0]["score"]), bg="#73787C", fg="#fdfce9", font="Verdana 20 bold").grid(column=0,row=0)
    if (chosenDifficultyLevel == b'hard\n'):
        highScoreLabel = tk.Label(frame5, text="High Score: " + getTimeAsString(hardLeaderboard[0]["score"]), bg="#73787C", fg="#fdfce9", font="Verdana 20 bold").grid(column=0,row=0)
    if (chosenDifficultyLevel == b'xtreme\n'):
        highScoreLabel = tk.Label(frame5, text="High Score: " + getTimeAsString(xtremeLeaderboard[0]["score"]), bg="#73787C", fg="#fdfce9", font="Verdana 20 bold").grid(column=0,row=0)        
                                  
    countdownValue = 2

    
    while countdownValue > -1:
        countdownTimer.config(text = countdownValue+1)
        countdownTimer.grid(column=0,row=1)
        countdownValue -= 1

        root.update()
        time.sleep(1)
        
    countdownTimer.destroy()
    
    timerLabel = tk.Label(frame5, text="", bg="#73787C", fg="#fdfce9", font="Verdana 80 bold")
    ResetTimer(timerLabel)
    timerLabel.grid(column=0,row=1)
    StartTimer(timerLabel)
    


def deleteLetterInputHighScoreName(highScoreNameIndex):
    nameEntry1.delete(highScoreNameIndex-1,tk.END)
    nameEntry2.delete(highScoreNameIndex-1,tk.END)


def inputHighScoreName(highScoreNameIndex, letter):
    if ((len(nameEntry1.get()) and len(nameEntry2.get())) < 8):
        nameEntry1.insert(tk.END, letter)
        nameEntry2.insert(tk.END, letter)
        highScoreNameIndex = highScoreNameIndex + 1;

        

    
def loadCurrentHighScores(leaderboardFile):
    global easyLeaderboard
    global intermediateLeaderboard
    global hardLeaderboard
    global xtremeLeaderboard
    with open(leaderboardFile, "r") as currentLeaderboards:
        leaderboardData = json.load(currentLeaderboards)
        sortedEasyLeaderboard = sorted(leaderboardData['easy'], key = lambda i: int(i["score"]), reverse=False)
        easyLeaderboard = [sortedEasyLeaderboard[0], sortedEasyLeaderboard[1],sortedEasyLeaderboard[2],sortedEasyLeaderboard[3],sortedEasyLeaderboard[4]]
#         print("easyLead: ", easyLeaderboard)      
        sortedIntermediateLeaderboard = sorted(leaderboardData['intermediate'], key = lambda i: int(i["score"]), reverse=False)
        intermediateLeaderboard = [sortedIntermediateLeaderboard[0], sortedIntermediateLeaderboard[1],sortedIntermediateLeaderboard[2],sortedIntermediateLeaderboard[3],sortedIntermediateLeaderboard[4]]
#         print("intermediateLeaderboard: ", intermediateLeaderboard)
        sortedHardLeaderboard = sorted(leaderboardData['hard'], key = lambda i: int(i["score"]), reverse=False)
        hardLeaderboard = [sortedHardLeaderboard[0], sortedHardLeaderboard[1],sortedHardLeaderboard[2],sortedHardLeaderboard[3],sortedHardLeaderboard[4]]                        
#         print("hardLeaderboard: ", hardLeaderboard)
        sortedXtremeLeaderboard =sorted(leaderboardData['xtreme'], key = lambda i: int(i["score"]), reverse=False)
        xtremeLeaderboard = [sortedXtremeLeaderboard[0], sortedXtremeLeaderboard[1],sortedXtremeLeaderboard[2],sortedXtremeLeaderboard[3],sortedXtremeLeaderboard[4]]                        
#         print("xtremeLeaderboard: ", xtremeLeaderboard)
        
        for score in range(5):
            tk.Label(frame9, bg="#6BAA41", font ="Verdana 15 bold", fg ="#fdfce9", text=str(score+1)+".", borderwidth=0).grid(column=1,row=score, sticky="news")
            tk.Label(frame9, bg="#6BAA41", font ="Verdana 15 bold", fg ="#fdfce9", text=getTimeAsString(easyLeaderboard[score]["score"]), borderwidth=0).grid(column=2,row=score, sticky="news")
            tk.Label(frame9, bg="#6BAA41", font ="Verdana 15 bold", fg ="#fdfce9", text=easyLeaderboard[score]["name"], borderwidth=0).grid(column=3,row=score, sticky="news")
            
     
            tk.Label(frame10, bg="#DEA336", font ="Verdana 15 bold", fg ="#fdfce9", text=str(score+1)+".", borderwidth=0).grid(column=1,row=score, sticky="news")
            tk.Label(frame10, bg="#DEA336", font ="Verdana 15 bold", fg ="#fdfce9", text=getTimeAsString(intermediateLeaderboard[score]["score"]), borderwidth=0).grid(column=2,row=score, sticky="news")
            tk.Label(frame10, bg="#DEA336", font ="Verdana 15 bold", fg ="#fdfce9", text=intermediateLeaderboard[score]["name"], borderwidth=0).grid(column=3,row=score, sticky="news")
            
 
            tk.Label(frame11, bg="#FF7518", font ="Verdana 15 bold", fg ="#fdfce9", text=str(score+1)+".", borderwidth=0).grid(column=1,row=score, sticky="news")
            tk.Label(frame11, bg="#FF7518", font ="Verdana 15 bold", fg ="#fdfce9", text=getTimeAsString(hardLeaderboard[score]["score"]), borderwidth=0).grid(column=2,row=score, sticky="news")
            tk.Label(frame11, bg="#FF7518", font ="Verdana 15 bold", fg ="#fdfce9", text=hardLeaderboard[score]["name"], borderwidth=0).grid(column=3,row=score, sticky="news")
            
          
            tk.Label(frame12, bg="#D94E47", font ="Verdana 15 bold", fg ="#fdfce9", text=str(score+1)+".", borderwidth=0).grid(column=1,row=score, sticky="news")
            tk.Label(frame12, bg="#D94E47", font ="Verdana 15 bold", fg ="#fdfce9", text=getTimeAsString(xtremeLeaderboard[score]["score"]), borderwidth=0).grid(column=2,row=score, sticky="news")
            tk.Label(frame12, bg="#D94E47", font ="Verdana 15 bold", fg ="#fdfce9", text=xtremeLeaderboard[score]["name"], borderwidth=0).grid(column=3,row=score, sticky="news")
            
                        
#             difficultyLevelsColor = ["#6BAA41","#DEA336","#FF7518", "#D94E47"]
            
def chooseLeaderboard(frameToChangeTo):
    loadCurrentHighScores(leaderboardFile)
    if(frameToChangeTo == 0):
#         change_between_frames(frame8,frame13)
        change_between_frames(frame8,frame9)
    if(frameToChangeTo == 1):
        change_between_frames(frame8,frame10)
    if(frameToChangeTo == 2):
        change_between_frames(frame8,frame11)
    if(frameToChangeTo == 3):
        change_between_frames(frame8,frame12)


def updateLeaderboard(highScoreFile, leaderboardDifficulty, newHighScoreData):
        data = json.load(highScoreFile)
#         print("data: ", data)
#         print("high: ", newHighScoreData)
#         print("diff: ", leaderboardDifficulty)
        data[leaderboardDifficulty].append(newHighScoreData)
#         print(data)
#         sortedScoreData = sorted(data[leaderboardDifficulty], key = lambda i: int(i["score"]), reverse=False)
#         print("sorted: ",sortedScoreData)
        highScoreFile.seek(0)
        json.dump(data, highScoreFile, indent=2)
        nameEntry1.delete(0,tk.END)
        nameEntry2.delete(0,tk.END)
        loadCurrentHighScores(leaderboardFile)
        
def submitHighScoreName(currentFrame, highScoreName, playerTime):
    highScoreDict = dict()
    playerTime=getTimeAsInt(playerTime)
    newHighScore = {"name": highScoreName, "score": playerTime}
    difficultySelected = 0
    with open(leaderboardFile, "r+") as writeHighScoreFile:
        if (chosenDifficultyLevel == b'easy\n'):
            updateLeaderboard(writeHighScoreFile, "easy", newHighScore)

        if (chosenDifficultyLevel == b'intermediate\n'):
            updateLeaderboard(writeHighScoreFile, 'intermediate', newHighScore)

        if (chosenDifficultyLevel == b'hard\n'):
            updateLeaderboard(writeHighScoreFile, 'hard', newHighScore)

        if (chosenDifficultyLevel == b'xtreme\n'):
            updateLeaderboard(writeHighScoreFile, 'xtreme', newHighScore)

            
        newGame(currentFrame, frame2)

    
def startGame(currentFrame,newFrame):
    playMusic("forever")
    change_between_frames(currentFrame, newFrame)
    loadMusic('/home/pi/Desktop/Python Scripts/timer/countdown.mp3')
    playMusic("forever")
    loadCurrentHighScores(leaderboardFile)
    startGameCountdown()
    stopMusic()
    loadMusic(selected_song)
    playMusic("forever")

def gameOver():
    StopTimer()
    stopMusic()
    loadMusic('/home/pi/Desktop/Python Scripts/gameover/gameover.mp3')
    playMusic(1)
    gameoverLabel = tk.Label(frame6, image=gameoverMessage,borderwidth=0)
    gameoverLabel.grid(column=0,row=0)
    playerFailureTimeLabel = tk.Label(frame6,text=playerTime, fg="#fdfce9", bg="#73787C", font="Verdana 40 bold")
    playerFailureTimeLabel.grid(column=0,row=1)
    change_between_frames(frame5, frame6)
    timerLabel.destroy()

def playerWins():
    StopTimer()
    loadMusic('/home/pi/Desktop/Python Scripts/victory/victory.mp3')
    playMusic("forever")
    playerVictoryLabel = tk.Label(frame7,image=youWinMessage,borderwidth=0)
    playerVictoryLabel.grid(column=0,row=0)

    newScore = False
    if (chosenDifficultyLevel == b'easy\n'):
        if (getTimeAsInt(playerTime) < int(easyLeaderboard[4]["score"])):
            victoryText = "New High Score!"
            tk.Label(frame7,text=victoryText, fg="#fdfce9", bg="#73787C", font="Verdana 20 bold").grid(column=0,row=1)
            newScore = True
    if (chosenDifficultyLevel == b'intermediate\n'):
        if (getTimeAsInt(playerTime) < int(intermediateLeaderboard[4]["score"])):
            victoryText = "New High Score!"
            tk.Label(frame7,text=victoryText, fg="#fdfce9", bg="#73787C", font="Verdana 20 bold").grid(column=0,row=1)
            newScore = True
    if (chosenDifficultyLevel == b'hard\n'):
        if (getTimeAsInt(playerTime) < int(hardLeaderboard[4]["score"])):
            victoryText = "New High Score!"
            tk.Label(frame7,text=victoryText, fg="#fdfce9", bg="#73787C", font="Verdana 20 bold").grid(column=0,row=1)
            newScore = True
    if (chosenDifficultyLevel == b'xtreme\n'):
        if (getTimeAsInt(playerTime) < int(xtremeLeaderboard[4]["score"])):
            victoryText = "New High Score!"
            tk.Label(frame7,text=victoryText, fg="#fdfce9", bg="#73787C", font="Verdana 20 bold").grid(column=0,row=1)
            newScore = True
    if (newScore == True):
        tk.Button(frame7, text="Enter Name",bg="#72CC50",fg="#fdfce9",font="Verdana 20 bold",activebackground = "#72CC50",activeforeground = "#fdfce9",command= lambda : change_between_frames(frame7,frame13)).grid(column=0, row=3, sticky='news')
    else:
        tk.Button(frame7, text="New Game",bg="#72CC50",fg="#fdfce9",font="Verdana 20 bold",activebackground = "#72CC50",activeforeground = "#fdfce9",command= lambda : newGame(frame7,frame2)).grid(column=0, row=3, sticky='news')
    
    playerVictoryTimeLabel = tk.Label(frame7,text=playerTime, fg="#fdfce9", bg="#73787C", font="Verdana 40 bold")
    playerVictoryTimeLabel.grid(column=0,row=2)
    change_between_frames(frame5, frame7)
    timerLabel.destroy()
    
def resetTimerVariables():
    countdownTimer = 0
    counter = 50000 #25200
    playerFailureTimeLabel = 0


def tryAgain():
#     frame5.destroy()
    frame5 = tk.Frame(root)
    resetTimerVariables()
    startGame(frame6, frame5)
    
def newGame(currentFrame,newFrame):
    loadCurrentHighScores(leaderboardFile)
    frame5 = tk.Frame(root)
    resetTimerVariables()
    playMenuMusic()   
    change_between_frames(currentFrame,newFrame)


# root.title("Choose a Song!")
# root.configure(bg='lightblue')
if setToFullScreen == True:
        root.wm_attributes('-fullscreen',True)
else:
    center_window()

numberOfMusicFiles = count_number_of_files(musicTracksDirectory)

#Create desired fonts
font_large = font.Font(family='Georgia',
                       size='16',
                       weight='bold')
font_small = font.Font(family='Georgia',
                       size='12')
#Frame 1 Welcome Screen



gazerbeam_logo_label = tk.Label(frame1, image=gazerbeam_logo, borderwidth=0, )
gazerbeam_logo_label.grid(column=0,row=0, columnspan=2)
                            
btn_change_to_choose_song = tk.Button(frame1, borderwidth=0, text="Start",
                                      font="Verdana 30 bold",
                                      bg="#000000",
                                      fg="#fdfce9",
                                      activebackground = "#000000",
                                      activeforeground = "#fdfce9",
#                                       command= lambda : loadCurrentHighScores(leaderboardFile))
                                      command= lambda : change_between_frames(frame1, frame2))
btn_change_to_choose_song.grid(column=0, row=1, sticky="news")

                            
btn_troubleshoot = tk.Button(frame1, borderwidth=0, text="Troubleshoot",
                                      font="Verdana 30 bold",
                                      bg="#000000",
                                      fg="#fdfce9",
                                      activebackground = "#000000",
                                      activeforeground = "#fdfce9",
#                                       command= lambda : loadCurrentHighScores(leaderboardFile))
                                      command= lambda : change_between_frames(frame1, frame2))
btn_troubleshoot.grid(column=1, row=1, sticky="news")
#Frame 2 Select Song
musicFiles_dict = dict()
ent_dict = dict()

row = 0
col = 0
songName = ["Thriller", "Thriller", "Ghost\nBusters", "Monster\nMash","This Is\nHalloween","Somebody's\nWatching\nMe","Halloween\nTheme","Robots","M.I."]
songColor = ["#fdfce9","#FF7518","#000000","#FF7518","#000000","#FF7518","#000000","#FF7518", "#000000"] #"#8A1B7A"
songTextColor = ["#000000","#000000","#fdfce9","#000000","#fdfce9","#000000","#fdfce9","#000000", "#fdfce9"]
for musicFile in range(numberOfMusicFiles):
        
        if (musicFile % 3 == 0) and (musicFile != 0):
            row += 1
            col = 0
        if (musicFile == 0):
            highScores = musicFile
            goToHighScoresButton= tk.Button(frame2, text="High\nScores",
                                                  font = "Verdana 18 bold",
                                                  bg = songColor[musicFile],
                                                  activebackground = songColor[musicFile],
                                                  activeforeground = songTextColor[musicFile],
                                                  fg = songTextColor[musicFile],
                                                  command = lambda : change_between_frames(frame2, frame8))
            goToHighScoresButton.grid(column=col,row=row, sticky='nesw')
        if (musicFile > 0):
            musicFiles_dict[musicFile]= tk.Button(frame2, text=songName[musicFile],
                                                  font = "Verdana 15 bold",
                                                  bg = songColor[musicFile],
                                                  activebackground = songColor[musicFile],
                                                  activeforeground = songTextColor[musicFile],
                                                  fg = songTextColor[musicFile],
                                                  command = lambda musicFile=musicFile: selectMusic(musicFile))
            musicFiles_dict[musicFile].grid(column=col,row=row, sticky='nesw')

#         row +=
        col += 1


#Frame 3 Select Difficulty
btn_change_to_select_song = tk.Button(frame3, image=backButton,
                                      font="Verdana 20 bold",
                                      bg="#73787C", fg="#fdfce9",
                                      activebackground = "#73787C",
                                      activeforeground = "#fdfce9",                                      
                                      command= lambda : change_between_frames(frame3, frame2))
btn_change_to_select_song.grid(column=0, row=0,rowspan=4, sticky="news")

difficultyLevel_dict= dict()
difficultyLevelsText = ["Easy", "Medium", "Hard", "Xtreme"]
difficultyLevelsColor = ["#6BAA41","#DEA336","#FF7518", "#D94E47"]

for difficultyLevel in range(4):
    rowNumber = difficultyLevel
    difficultyLevel_dict[difficultyLevel]= tk.Button(frame3, text=difficultyLevelsText[difficultyLevel],
                                                     bg = difficultyLevelsColor[difficultyLevel],
                                                     font="Verdana 20 bold",
                                                     fg="#fdfce9",
                                                     activebackground = difficultyLevelsColor[difficultyLevel],
                                                     activeforeground = "#fdfce9", 
                                                     command = lambda difficultyLevel=difficultyLevel: selectDifficultyLevel(difficultyLevel))
    difficultyLevel_dict[difficultyLevel].grid(column=1,row=rowNumber,sticky='news')

#Frame 4 Start Game
btn_change_to_select_difficulty = tk.Button(frame4, image=backButton,
                                            bg="#73787C", fg="#fdfce9",
                                            activebackground = "#73787C",
                                            activeforeground = "#fdfce9", 
                                            command= lambda : change_between_frames(frame4, frame3))
btn_change_to_select_difficulty.grid(column=0, row=0, rowspan=3, sticky="news")

btn_start_game = tk.Button(frame4, text="Start\nGame",
                           bg="#6BAA41",
                           fg="#fdfce9",
                           font="Verdana 40 bold",
                           activebackground = "#6BAA41",
                           activeforeground = "#fdfce9",
                           command= lambda : startGame(frame4, frame5))
btn_start_game.grid(column=1, row=0, rowspan=3, sticky="news")

#Frame 6 Failure Try Again Screen
# btn_try_again = tk.Button(frame6, text="Try Again", font=font_small, command= tryAgain)
# btn_try_again.grid(column=0, row=5, sticky='news')
btn_new_game = tk.Button(frame6, text="New Game",
                         bg="#ED2939",
                         fg="#fdfce9",
                         font="Verdana 20 bold",
                         activebackground = "#ED2939",
                         activeforeground = "#fdfce9",
                         command= lambda : newGame(frame6, frame2))
btn_new_game.grid(column=0, row=2, sticky='news')
# timerLabel = tk.Label(frame6, text=playerTime, fg="black", font="Verdana 30 bold")

#Frame 7 You Win Screen


#Frame 8 Select Leaderboard
btn_change_to_select_song = tk.Button(frame8, image=backButton,
                                      font="Verdana 20 bold",
                                      bg="#73787C", fg="#fdfce9",
                                      activebackground = "#73787C",
                                      activeforeground = "#fdfce9",                                      
                                      command= lambda : change_between_frames(frame8, frame2))
btn_change_to_select_song.grid(column=0, row=0,rowspan=4, sticky="news")

difficultyLevel_dict= dict()
difficultyLevelsText = ["Easy High Scores", "Medium High Scores", "Hard High Scores", "Xtreme High Scores"]
difficultyLevelsColor = ["#6BAA41","#DEA336","#FF7518", "#D94E47"]

for difficultyLevel in range(4):
    rowNumber = difficultyLevel
    difficultyLevel_dict[difficultyLevel]= tk.Button(frame8, text=difficultyLevelsText[difficultyLevel],
                                                     bg = difficultyLevelsColor[difficultyLevel],
                                                     font="Verdana 20 bold",
                                                     fg="#fdfce9",
                                                     activebackground = difficultyLevelsColor[difficultyLevel],
                                                     activeforeground = "#fdfce9", 
                                                     command = lambda difficultyLevel = difficultyLevel : chooseLeaderboard(difficultyLevel))
    difficultyLevel_dict[difficultyLevel].grid(column=1,row=rowNumber,sticky='news')
#Frame 9 Easy Leaderboard
btn_easy_to_leaderboard = tk.Button(frame9, image=backButton,
                                      font="Verdana 20 bold",
                                      bg="#73787C", fg="#fdfce9",
                                      activebackground = "#73787C",
                                      activeforeground = "#fdfce9",    
                                      command= lambda : change_between_frames(frame9, frame8))
btn_easy_to_leaderboard.grid(column=0, row=0, rowspan = 5, sticky="news")

#Frame 10 Medium Leaderboard
btn_medium_to_leaderboard = tk.Button(frame10, image=backButton,
                                      font="Verdana 20 bold",
                                      bg="#73787C", fg="#fdfce9",
                                      activebackground = "#73787C",
                                      activeforeground = "#fdfce9",    
                                      command= lambda : change_between_frames(frame10, frame8))
btn_medium_to_leaderboard.grid(column=0, row=0,rowspan = 5, sticky="news")

#Frame 11 Hard Leaderboard
btn_hard_to_leaderboard = tk.Button(frame11, image=backButton,
                                      font="Verdana 20 bold",
                                      bg="#73787C", fg="#fdfce9",
                                      activebackground = "#73787C",
                                      activeforeground = "#fdfce9",   
                                      command= lambda : change_between_frames(frame11, frame8))
btn_hard_to_leaderboard.grid(column=0, row=0, rowspan = 5, sticky="news")

#Frame 12 Xtreme Leaderboard
btn_xtreme_to_leaderboard = tk.Button(frame12, image=backButton,
                                      font="Verdana 20 bold",
                                      bg="#73787C", fg="#fdfce9",
                                      activebackground = "#73787C",
                                      activeforeground = "#fdfce9",    
                                      command= lambda : change_between_frames(frame12, frame8))
btn_xtreme_to_leaderboard.grid(column=0, row=0,rowspan = 5, sticky="news")

#Page 13 (1st letter page)

btn_backspace = tk.Button(frame13, image = backspaceIcon,
                                      borderwidth=0,  
                                      font="Verdana 20 bold",
                                      bg="#73787C", fg="#fdfce9",
                                      activebackground = "#73787C",
                                      activeforeground = "#fdfce9",    
                                      command= lambda : deleteLetterInputHighScoreName(len(nameEntry1.get())))
btn_backspace.grid(column=0, row=0, columnspan=1, sticky="news")


btn_enter = tk.Button(frame13, width=96, image= checkMarkIcon,
                                      borderwidth=0,                      
                                      bg="#6BAA41", fg="#fdfce9",
                                      activebackground = "#6BAA41",
                                      activeforeground = "#fdfce9",    
                                      command= lambda : submitHighScoreName(frame13, nameEntry1.get(),playerTime))
btn_enter.grid(column=4, row=0, columnspan=1, sticky="news")

btn_to_second_letter_page = tk.Button(frame13, text="next",
                                      font="Verdana 20 bold",
                                      bg="#73787C", fg="#fdfce9",
                                      activebackground = "#73787C",
                                      activeforeground = "#fdfce9",    
                                      command= lambda : change_between_frames(frame13, frame14))
btn_to_second_letter_page.grid(column=3, row=3, columnspan=2, sticky="news")
letterRow = 1;
letterCol = 0;

firstPageLetters = ["A","B","C","D","E","F","G","H","I","J","K","L","M"]
for letterButton in range(13):
        
        if (letterButton % 5 == 0) and (letterButton != 0):
            letterRow += 1
            letterCol = 0

        if (letterButton >= 0) :
            letterSelectButton= tk.Button(frame13, text=firstPageLetters[letterButton],
                                                  font = "Verdana 20 bold",
                                                  bg = songColor[musicFile],
                                                  activebackground = songColor[musicFile],
                                                  activeforeground = songTextColor[musicFile],
                                                  fg = songTextColor[musicFile],
                                                  command = lambda letterButton = letterButton : inputHighScoreName(highScoreNameIndex, firstPageLetters[letterButton]))
        letterSelectButton.grid(column=letterCol,row=letterRow, sticky='nesw')

        letterCol += 1
        
secondPageLetterRow = 1;
secondPageLetterCol = 0;

#Page 14 (2nd letter page)
btn_second_page_backspace = tk.Button(frame14, image = backspaceIcon,
                                      font="Verdana 20 bold",
                                      bg="#73787C", fg="#fdfce9",
                                      activebackground = "#73787C",
                                      activeforeground = "#fdfce9",    
                                      command= lambda : deleteLetterInputHighScoreName(len(nameEntry2.get())))
btn_second_page_backspace.grid(column=0, row=0, columnspan=1, sticky="news")

btn_second_enter = tk.Button(frame14, image= checkMarkIcon,
                                      bg="#6BAA41", fg="#fdfce9",
                                      activebackground = "#6BAA41",
                                      activeforeground = "#fdfce9",    
                                      command= lambda : submitHighScoreName(frame14, nameEntry1.get(), playerTime))
btn_second_enter.grid(column=4, row=0, columnspan=1, sticky="news")

btn_to_first_letter_page = tk.Button(frame14, text="back",
                                      font="Verdana 20 bold",
                                      bg="#73787C", fg="#fdfce9",
                                      activebackground = "#73787C",
                                      activeforeground = "#fdfce9",    
                                      command= lambda : change_between_frames(frame14, frame13))
btn_to_first_letter_page.grid(column=0, row=3, columnspan=2, sticky="news")
secondPageLetters = ["N","O","P","Q","R","S","T","U","V","W","X","Y","Z"]
for secondPageLetterButton in range(13):
        
        if (secondPageLetterButton % 5 == 0) and (secondPageLetterButton != 0):
            secondPageLetterRow += 1
            secondPageLetterCol = 0
        if (secondPageLetterRow == 3) and secondPageLetterButton <11:
            secondPageLetterCol = 2

        if (secondPageLetterButton >= 0) :
            secondPageLetterSelectButton= tk.Button(frame14, text=secondPageLetters[secondPageLetterButton],
                                                  font = "Verdana 20 bold",
                                                  bg = songColor[musicFile],
                                                  activebackground = songColor[musicFile],
                                                  activeforeground = songTextColor[musicFile],
                                                  fg = songTextColor[musicFile],
                                                  command = lambda secondPageLetterButton = secondPageLetterButton : inputHighScoreName(highScoreNameIndex, secondPageLetters[secondPageLetterButton]))
        secondPageLetterSelectButton.grid(column=secondPageLetterCol,row=secondPageLetterRow, sticky='nesw')

        secondPageLetterCol += 1

# Start main code
if __name__ == '__main__':
    playLoadScreenMusic()
    playMenuMusic()
    if (ACM0 == True):
        ser = serial.Serial('/dev/ttyACM0',9600,timeout=1)
    else:
        ser = serial.Serial('/dev/ttyACM1',9600,timeout=1)
    ser.flush()
    frame1.pack(fill='both', expand=1)
    while True:
        

        if ser.in_waiting > 0:
            root.update()
#             if (ser.readline().decode('utf-8', errors='replace').strip() == "startTransmission"):
            gameStatus = ser.readline().decode('utf-8', errors='replace').strip()
#             print("betweengames: " + gameStatus);
#             print("beginninggameStatus)
            if ((running == True) and (gameStartFlag == True)):
                ser.write(b'gameStarted\n')
                print(running)
                print(gameStartFlag)
                ser.write(chosenDifficultyLevel)
                gameStartFlag = False
            if (gameStatus == "gameOver") and gameStartFlag == False:
                print("game Status: "+ gameStatus)
#                 print("startflag: "             + str(gameStartFlag));
                gameStartFlag = True
                gameOver()
                
            if (gameStatus == "playerWins") and gameStartFlag == False:
                print(gameStatus)
                gameStartFlag = True
                playerWins()
            


# 
# 
root.mainloop()
# # # root.grid_rowconfigure(0, weight=1)
# # # root.columnconfigure(0, weight=1)
# #
# # frame_main = tk.Frame(root, bg="gray")
# # frame_main.grid(sticky='news')
# #
# # label1 = tk.Label(frame_main, text="Label 1", fg="green")
# # label1.grid(row=0, column=0, pady=(5, 0), sticky='nw')
# #
# # label2 = tk.Label(frame_main, text="Label 2", fg="blue")
# # label2.grid(row=1, column=0, pady=(5, 0), sticky='nw')`bbbbbbbbbbbb 