###########################################################################
# video2text.py : Converts the video from url to text file(.txt)          #
# ver           : 1.0                                                     #
# OS            : Windows 10 (64 bit)                                     #
# Author        : Lepakshi Datta Dupakuntl                                #
#                 ldupakun@syr.edu                                        #
###########################################################################


# Packages / Libraries / Tools to be installed or downloaded :
# ------------------------------------------------------------
#


from __future__ import unicode_literals
import youtube_dl
import speech_recognition as sr
import math
import os
import soundfile as sf


def videoToAudio(id):
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl':'test.%(ext)s',      #'outtmpl':'%(title)s.%(ext)s' -- output audio file name
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'wav',
            'preferredquality': '192'
        }],
        'postprocessor_args': [
            '-ar', '16000'
        ],
        'prefer_ffmpeg': True,
        'keepvideo': False
    }

    link ="https://www.youtube.com/watch?v="+id

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([link])

def audioToText():
    f = sf.SoundFile('test.wav')
    s = format(len(f)/f.samplerate) #formula to calculate the length of audio in seconds
    lengthAudio=int(float(s))

    r=sr.Recognizer()
    audio=[]

    x=sr.AudioFile('test.wav')

    with x as source:
        for i in range (0,math.ceil(lengthAudio / 5)):
            audio.append( r.record(source,duration=5))

    with open("captions.txt", "w") as f:
        for j in range(0,math.ceil(lengthAudio / 5)):
            try:
                text=r.recognize_google(audio[j])+' '
                f.write(text)
            except:
                print(' ')

    os.remove('test.wav') #to remove generated audio file


if __name__ == '__main__':
    try:
        id="1r3wbWPIuBw&t=1s"
        videoToAudio(id)
        audioToText()
    except:
        print('')

