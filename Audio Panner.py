from glob import glob
from pydub import *
from math import *
from random import *
import sys,os
from pysndfx import AudioEffectsChain
from pydub.playback import play
import numpy as np
if len(sys.argv) > 2:
	AudioSegment.converter = sys.argv[1] #ffmpeg installation exe dir path
	AudioSegment.ffmpeg = sys.argv[1] #ffmpeg installation exe dir path
	AudioSegment.ffprobe = sys.argv[2] #ffprobe installation exe dir path

def eightdsong(filename,searchdir):
        slash = r"\\"
        interval = 0.2 * 500 # 1000 is 1 sec
        if filename.endswith(".mp3"):
                try:    
                        song = AudioSegment.from_mp3(os.path.join(searchdir,filename))
                except:
                        return False
        elif filename.endswith(".wav"):
                try:
                        song = AudioSegment.from_wav(os.path.join(searchdir,filename))
                except:
                        return False
        else:
                return False
        newfile = "8D "+filename
        song_inverted = song.invert_phase()
        song.overlay(song_inverted)

        splitted_song = splitted_song_inverted = []
        song_start_point = 0

        while song_start_point+interval < len(song):
            splitted_song.append(song[song_start_point:song_start_point+interval])
            song_start_point += interval

        if song_start_point < len(song):
            splitted_song.append(song[song_start_point:])

        print ("Total Pieces: " + str(len(splitted_song)))

        ambisonics_song = splitted_song.pop(0)
        pan_index = 0
        for piece in splitted_song:
            pan_index += 5
            piece = piece.pan(calc_pan(pan_index))
            ambisonics_song = ambisonics_song.append(piece, crossfade=interval/50)
            #print("Piece No: ",str((pan_index/5)))
        print("Done!")

        # lets save it
        
        if not os.path.exists(searchdir+"Converted"+slash):
                os.mkdir(searchdir+"Converted"+slash)
        fullnewpath = os.path.join(searchdir,"Converted",newfile)
        ambisonics_song.export(fullnewpath, format='wav')
        print(f"Saved as: {newfile}")
        return  True

def calc_pan(index):
	return cos(radians(index))

searchdir = input("Path of dir to convert: ")
for filename in os.listdir(searchdir):
        eightdsong(filename,searchdir)
        print("8D",filename,searchdir)
    



