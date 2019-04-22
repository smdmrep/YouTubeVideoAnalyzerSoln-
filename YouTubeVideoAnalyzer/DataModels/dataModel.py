

#Commented coz I m running setup.py to keep dependency list of packages#
""" import os
import sys
#sys.path.append(os.path.dirname(os.path.abspath(__file__)))


PACKAGE_PARENT = '..'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT))) """

import configparser
import gridfs
from pymongo import MongoClient
from pprint import pprint
from random import randint

class DataModel:
    
    

    ######################### Initialize ############################
    #............. self.client holds the mongodb instance...........#
    #    
    #
    #****************************************************************#
    # Author        :   Guru
    # Created Date  :   04/22/2019          
    # Updated Date  : 
    def __init__(self):
        self.client = None



    ########################## Return Connection string ##########################
    #............. Read sections from configuration file. (config.ini)...........#
    #    
    #
    #****************************************************************#
    # Author        :   Guru
    # Created Date  :   04/22/2019          
    # Updated Date  : 

    def getConnectionString(self):
        try:
            config = configparser.ConfigParser()
            config.read("config.ini")
            userName =config["mongodbCluseterCredentials"]["userName"]
            password = config["mongodbCluseterCredentials"]["password"]
            hostName = config["mongodbCluseterCredentials"]["hostName"] 
            dbName = config["mongodbCluseterCredentials"]["dbName"]
            connectionString ="mongodb+srv://"+userName+":"+password+"@"+hostName+"/"+dbName+"?retryWrites=true"
            return connectionString
        except:
            print("exception occured!")



    ############### Connect to Mongo DB cluster ######################
    #............. Get the connection string and connect  ...........#
    #    
    #
    #****************************************************************#
    # Author        :   Guru
    # Created Date  :   04/22/2019          
    # Updated Date  :      
    def connectDb(self):
        try:
            connectionString = self.getConnectionString()
            self.client = MongoClient(connectionString)
        except:
            print("exception occured")


    ########################## Sample method to demonstrate retrieve info from database                             ########
    #......................... Retrieve all documents from collection productDetails under youtubeVideoAnalyzerTest .......#
    #****************************************************************#
    # Author        :   Guru
    # Created Date  :   04/22/2019          
    # Updated Date  :
    def getCollectionResults(self,collectionName):
        try:
            db      =   self.client.youtubeVideoAnalyzerTest
            result  =   db[collectionName].find({})
            for document in result:
                pprint(document)
        except:
            print("exception occured")


    ########################## Insert Video Content to database ##########################
    #......................... using gridfs module                    ...................#
    #......................... Once file is used, remove created file ...................#
    #......................... Return video id                        ....................#
    #****************************************************************#
    # Author        :   Guru
    # Created Date  :   04/22/2019          
    # Updated Date  :         
    def insertVideoContent(self,video):
        try:
            mp4file =   open(video,"rb")
            db      =   self.client.youtubeVideoAnalyzerTest
            fs      =   gridfs.GridFS(db)
            videoId =   fs.put(mp4file)
            mp4file.close()
            return videoId
        except Exception as e:
            print(e)



    ########################## Download Video Content from database ############################
    #......................... Get video from database using id             ...................#
    #......................... Once file is used, please remove created file...................#
    #****************************************************************#
    # Author        :   Guru
    # Created Date  :   04/22/2019          
    # Updated Date  : 
    def getVideoContent(self,videoId):
        try:
            db      =   self.client.youtubeVideoAnalyzerTest
            fs      =   gridfs.GridFS(db)
            video   =   fs.get(videoId)
            with open("temp.mp4", "wb") as handle:
                handle.write(video.read())
        except Exception as e:
            print(e)




# Calling this module..
# Create DataModel object and call respective method.
""" a = DataModel()
a.connectDb()
a.getCollectionResults("productDetails") """