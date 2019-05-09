

#Commented coz I m running setup.py to keep dependency list of packages#
""" import os
import sys
#sys.path.append(os.path.dirname(os.path.abspath(__file__)))


PACKAGE_PARENT = '..'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT))) """


from pkg_resources import Requirement, resource_filename
configurationFile = resource_filename(Requirement.parse("YouTubeVideoAnalyzer"),"config.ini")


import configparser
import gridfs
from pymongo import MongoClient
from pprint import pprint
from random import randint
from bson import json_util
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
            config.read(configurationFile)
            userName =config["mongodbCluseterCredentials"]["userName"]
            password = config["mongodbCluseterCredentials"]["password"]
            hostName = config["mongodbCluseterCredentials"]["hostName"] 
            dbName = config["mongodbCluseterCredentials"]["dbName"]
            connectionString ="mongodb+srv://"+userName+":"+password+"@"+hostName+"/"+dbName+"?retryWrites=true"
            return connectionString
        except Exception as e:
            print(e)



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
            # for document in result:
            #     pprint(document)
            return result
        except Exception as e:
            print(e)
            return None


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


    
    ########################## List search key details ############################
    #......................... from searchKeyDetails collection ...................#
    #****************************************************************#
    # Author        :   Guru
    # Created Date  :   04/22/2019          
    # Updated Date  : 
    def getSearchkeyList(self):
        try:
            db      =   self.client.youtubeVideoAnalyzerTest
            result  =   db["searchKeyDetails"].find({})
            # for document in result:
            #     pprint(document)
            return result
        except Exception as e:
            print(e)
            return None




    ########################## List caption  details ##############################
    #......................... from productDetails collection ...................#
    #****************************************************************#
    # Author        :   Guru
    # Created Date  :   04/22/2019          
    # Updated Date  : 
    def getCaptions(self):
        try:
            db= self.client.youtubeVideoAnalyzerTest
            result = db["productDetails"].find({}, { "_id": 0, "captions": 1,"video_id":2 })
            #db["productDetails"].update({}, {"$set": {"segmentedCaptions": ""}}, False, True)

            return result
        except Exception as e:
            print(e)
            return None



    ########################### update captions & set segmented captions ##############################
    #......................... to productDetails collection ..........................................#
    #****************************************************************#
    # Author        :   Guru
    # Created Date  :   04/22/2019          
    # Updated Date  : 
    def updateCaptions(self,dataSet):
        try:
            db=self.client.youtubeVideoAnalyzerTest
            for item in dataSet:
                db["productDetails"].update(
                    {"video_id": item["video_id"]},
                    { 
                        "$set": {
                                "segmentedCaptions": item["captions"]
                        }
                    }
                )
            
        except Exception as e:
            print(e)        



    ########################### get segmented captions ##############################
    #......................... from productDetails collection ......................#
    #****************************************************************#
    # Author        :   Guru
    # Created Date  :   04/22/2019          
    # Updated Date  : 
    def getSegmentedCaptions(self):
        try:
            db=self.client.youtubeVideoAnalyzerTest
            result=db["productDetails"].find({},{"_id":0,"segmentedCaptions":1,"video_id":2})
            return result
        except Exception as e:
            print(e)
            return None



    ########################### update document(aspect) level analysis ##############################
    #......................... to  productDetails collection .......................................#
    #****************************************************************#
    # Author        :   Guru
    # Created Date  :   04/22/2019          
    # Updated Date  : 
    def updateDocumentLevelAnalysis(self,analyzedDataSet):
        try:
            db=self.client.youtubeVideoAnalyzerTest
            for item in analyzedDataSet:
                db["productDetails"].update(
                    {"video_id": item["video_id"]},
                    { 
                        "$set": {
                                "documentScore":item["documentScore"],
                                "documentAspectList": item["documentAspectList"]
                        }
                    }
                )
            
        except Exception as e:
            print(e)



    ########################### list out sentence score for each individual video. ##############################
    #......................... from   productDetails collection .......................................#
    #****************************************************************#
    # Author        :   Guru
    # Created Date  :   05/02/2019          
    # Updated Date  :
    def getSentenceScores(self,searchKey): 
        db = self.client.youtubeVideoAnalyzerTest
        sentenceScoreList=db["productDetails"].find({"topic":searchKey},{"_id":0,"sentenceLevelScore":1})
        positiveScore =[]
        negativeScore =[]
        neutralityScore = []
        result=[]
        count =0
        for score in sentenceScoreList:
            if "sentenceLevelScore" in score:
                if len(score["sentenceLevelScore"]) !=0:
                    count = count+1
                    positiveScore.append(score["sentenceLevelScore"]["positive"])
                    negativeScore.append(score["sentenceLevelScore"]["negative"])
                    neutralityScore.append(score["sentenceLevelScore"]["neutrality"])

        result.append({"positive":positiveScore})
        result.append({"negative":negativeScore})
        result.append({"neutrality":neutralityScore})
        result.append({"count":count})
        return result



    ########################### update overall sentence score for entire product. ##############################
    #......................... to   productDetails collection .......................................#
    #****************************************************************#
    # Author        :   Guru
    # Created Date  :   05/02/2019          
    # Updated Date  :
    def updateSentenceOverallScore(self,sentenceLevelScore):
        db = self.client.youtubeVideoAnalyzerTest
        db["youtubeVideoAnalyzedScore"].update(
                    {"searchKey": sentenceLevelScore["searchKey"]},
                    { 
                        "$set": {
                                "sentencePositive":sentenceLevelScore["sentencePositive"],
                                "sentenceNegative": sentenceLevelScore["sentenceNegative"],
                                "sentenceNeutral":sentenceLevelScore["sentenceNeutral"]
                        }
                    }
                )



    ########################### Redundant... ##############################
    #......................... not in use.......................................#
    #****************************************************************#
    # Author        :   Guru
    # Created Date  :   05/02/2019          
    # Updated Date  :
    def updateOverallSentenceLevelScore(self,overallSentenceScore):
        db=self.client.youtubeVideoAnalyzerTest
        for item in overallSentenceScore:
            db["youtubeVideoAnalyzedScore"].update(
                {"Samsung Galaxy S10": item["Samsung Galaxy S10"]},
                    { 
                        "$set": {
                                "sentenceLevelScore":item["sentenceLevelScore"]
                        }
                    }
                )


    ########################### update sentence score for each individual video ##############################
    #.........................  from productDetails collection.......................................#
    #****************************************************************#
    # Author        :   Guru
    # Created Date  :   05/02/2019          
    # Updated Date  :
    def updateSentenceLevelAnalysis(self,analyzedDataSet):
        db=self.client.youtubeVideoAnalyzerTest
        for item in analyzedDataSet:
            db["productDetails"].update(
                {"video_id": item["video_id"]},
                    { 
                        "$set": {
                                "sentenceLevelScore":item["sentenceLevelScore"]
                        }
                    }
                )



    #Get the connection to the database.
    def getConnection(self):
        return self.client.youtubeVideoAnalyzerTest
    



    ########################### insert document(aspect) overall score##############
    #......................... to productDetails collection ......................#
    #****************************************************************#
    # Author        :   Guru
    # Created Date  :   04/22/2019          
    # Updated Date  : 
    def insertDocumentOverallScore(self,documentOverallScore):
        db = self.client.youtubeVideoAnalyzerTest
        db["youtubeVideoAnalyzedScore"].insert_one(documentOverallScore)





    ########################### list document(aspect) score.#######################
    #......................... from productDetails collection ......................#
    #****************************************************************#
    # Author        :   Guru
    # Created Date  :   04/22/2019          
    # Updated Date  : 
    def getDocumentScores(self,searchKey):
        db = self.client.youtubeVideoAnalyzerTest
        documentScoreList=db["productDetails"].find({"topic":searchKey},{"_id":0,"documentScore":1,"documentAspectList":2})
        positiveScore =[]
        negativeScore =[]
        neutralityScore = []
        result=[]
        count =0
        for score in documentScoreList:
            if "documentAspectList" in score:
                if len(score["documentAspectList"])!=0:
                    count = count+1
                    positiveScore.append(score["documentScore"]["positive"])
                    negativeScore.append(score["documentScore"]["negative"])
                    neutralityScore.append(score["documentScore"]["neutrality"])        


        result.append({"positive":positiveScore})
        result.append({"negative":negativeScore})
        result.append({"neutral":neutralityScore})
        result.append({"count":count})
        return result    
        



    # def insertYouTubeVideoAnalyzedScores(self):
    #     db = self.client.youtubeVideoAnalyzerTest
    #     pass
        

    @staticmethod
    def readMetaData(db):
        searchKeysList = [] 
        table = db.searchKeyDetails
        searchKeys = table.find()
        for searchKey in searchKeys:
            searchKeysList.append(searchKey['searchKey'])
        return searchKeysList
    
    #function for saving all the data mined for videos to database.
    @staticmethod
    def saveVideosInfo(db,searchKey,videosInfo):
        #access the table.
        productDetails = db.productDetails
                
        productVideos = productDetails.find({"topic":searchKey})
        
        #check if the video has already been uploaded in database. If yes, ignore it.
        for productVideo in productVideos:
            for i in range(len(videosInfo)):
                videoInfoLoad = json_util.loads(videosInfo[i])
                if videoInfoLoad['video_id'] == productVideo['video_id']:
                    del videosInfo[i]
                    break
                        
        data = []
        for videoInfo in videosInfo:
            data.append(json_util.loads(videoInfo))
            
        #save all the documents to the database.
        result = productDetails.insert_many(data)
        
        return result

# Calling this module..
# Create DataModel object and call respective method.
# a = DataModel()
# a.connectDb()
# a.getCaptions()