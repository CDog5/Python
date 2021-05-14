from glob import glob
from pydub import *
from math import *
from random import *
import sys
from pydub.playback import play
if len(sys.argv) > 2:
	AudioSegment.converter = sys.argv[1] #ffmpeg installation exe dir path
	AudioSegment.ffmpeg = sys.argv[1] #ffmpeg installation exe dir path
	AudioSegment.ffprobe = sys.argv[2] #ffprobe installation exe dir path

def calc_pan(index):
	return cos(radians(index))

filepath = input("Filepath: ")
interval = 0.2 * 1000 # sec
song = AudioSegment.from_wav(filepath)
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

# lets save it!
newfile = input("New Filename: ")
ambisonics_song.export(newfile+".wav", format='wav')
print(f"Saved as: {newfile}.wav")
result = AudioSegment.from_wav(newfile+".wav")
play(ambisonics_song)
