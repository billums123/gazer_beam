import tkinter as tk
import tkinter.font as font

def createSelectSongFrame(root):
    select_song_frame = tk.Frame(root)
    musicFiles_dict = dict()
    
    for musicFile in range(3):
        rowNumber = musicFile   
        musicFiles_dict[musicFile]= tk.Button(selection_menu_frame,
                                              text=f"Song {musicFile}",
                                              command = lambda musicFile=musicFile: selectMusic(musicFile))
        musicFiles_dict[musicFile].grid(column=0,row=rowNumber)