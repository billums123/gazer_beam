from pygame import mixer
dirName = '/home/pi/Desktop/Python Scripts/'
mixer.init()
mixer.music.load(dirName + '/audio2.wav')
mixer.music.play(5)