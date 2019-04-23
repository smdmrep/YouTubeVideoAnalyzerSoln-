import os
from  pytube import YouTube
from YouTubeVideoAnalyzer.DataModels.dataModel import DataModel

try:
    from urllib.request import urlopen
except ImportError:
    import urllib2 


class   videoExtractScrapper():

    ######################### Initialize ############################
    #............. self.url holds the url of video .................#
    #    
    #
    #****************************************************************#
    # Author        :   Guru
    # Created Date  :   04/22/2019          
    # Updated Date  : 
    def __init__(self,url):
        self.url = url



    ########################## Download Video Content and insert it into database ############################
    #......................... Download using YouTube object from pytube ...................................#
    #......................... Push to database using dataModel and remove created file
    #                          in the parent directory                   ...................................#    
    #
    #......................... TODO: scraping is pending.
    #****************************************************************#
    # Author        :   Guru
    # Created Date  :   04/22/2019          
    # Updated Date  : 
    def scrapVideoContent(self):
        try:
            youTube = YouTube(self.url)
            video = youTube.streams.first().download()

            dataModel = DataModel()
            dataModel.connectDb()
            videoId = dataModel.insertVideoContent(video)


            os.remove(video)
            return videoId
        except Exception as e:
            print(e)




    ########################## Download Video Content from database ############################
    #......................... Get video from database using id        ........................#
    #......................... Using dataModel and remove created file ........................#
    #****************************************************************#
    # Author        :   Guru
    # Created Date  :   04/22/2019          
    # Updated Date  : 
    def getVideoContent(self,videoId):
        try:
            dataModel   =   DataModel()
            dataModel.connectDb()
            dataModel.getVideoContent(videoId)
        except Exception as e:
            print(e)


# Calling this module..
# Create videoExtractScrapper object and call respective method.
""" url = "https://www.youtube.com/watch?v=KzdLNlCXQSo"
videoExtractScrapper = videoExtractScrapper(url)
videoId = videoExtractScrapper.scrapVideoContent()
videoExtractScrapper.getVideoContent(videoId) """