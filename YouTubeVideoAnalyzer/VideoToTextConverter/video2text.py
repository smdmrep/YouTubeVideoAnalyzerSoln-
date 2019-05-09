###########################################################################
# video2text.py : Converts the video from url to text file(.txt)          #
# ver           : 1.0                                                     #
# OS            : Windows 10 (64 bit)                                     #
# Author        : Lepakshi Datta Dupakuntla                               #
#                 ldupakun@syr.edu                                        #
###########################################################################


from __future__ import unicode_literals
import youtube_dl
import speech_recognition as sr
import math
import os
import soundfile as sf
from YouTubeVideoAnalyzer.DataModels.dataModel import DataModel



class VideoToText:


    ########################### Initialize #######################
    #****************************************************************#
    # Author        :   Guru
    # Created Date  :   05/03/2019
    # Updated Date  :
    def __init__(self):
        pass




    ########################### This function converts the generated audio file into text #######################
    #****************************************************************#
    # Author        :   Lepakshi Datta Dupakuntla
    # Created Date  :   05/03/2019
    # Updated Date  :
    def audioToText(self):
        try:
            f = sf.SoundFile('test.wav')
            s = format(len(f)/f.samplerate) #formula to calculate the length of audio in seconds
            lengthAudio=int(float(s))

            r=sr.Recognizer()
            audio=[]
            captions_array=[]
            x=sr.AudioFile('test.wav')

            with x as source:
                for i in range (0,math.ceil(lengthAudio / 5)):
                    audio.append( r.record(source,duration=5))


            for j in range(0,math.ceil(lengthAudio / 5)):
                try:
                    text=r.recognize_google(audio[j])
                    captions_array.append(text)
                except:
                    captions_array.append("")
            os.remove('test.wav')
            return captions_array
        except Exception as e:
            print(e)
            return None



    ########################### This function takes the video id as input and returns the audio file in .wav format#######################
    #****************************************************************#
    # Author        :   Lepakshi Datta Dupakuntla
    # Created Date  :   05/03/2019
    # Updated Date  :
    def videoToAudio(self,id):
        try:
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
        except Exception as e:
            print(e )



    ########################### Entry point to the module. Takes video without captions by converting them to text #######################
    #************************** And then update the productDetails Collection. **************************************#
    # Author        :   Lepakshi Datta Dupakuntla
    # Created Date  :   05/03/2019
    # Updated Date  :
    def convertVideoToText(self):
        try:
            dataModel = DataModel()
            dataModel.connectDb()

            dataSet = dataModel.getCaptions()
            for data in dataSet:
                if(data["captions"]==[]):
                    id=data["video_id"]
                    self.videoToAudio(id)
                    data["captions"] = self.audioToText()
                    dataModel.updateConvertedCaptionsFromVideo(data)
                else:
                    continue
        except Exception as e:
            print(e)


# if __name__ == '__main__':
#
#    videototext= VideoToText()
#    videototext.convertVideoToText()