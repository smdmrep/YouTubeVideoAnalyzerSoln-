from pymongo import MongoClient
from pprint import pprint
#configparser.ConfigParser()
#print(config.sections())
import google.oauth2.credentials
import json
import os
import sys
import httplib2
import google_auth_oauthlib.flow
import googleapiclient.discovery
import datetime

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google_auth_oauthlib.flow import InstalledAppFlow

from apiclient.discovery import build_from_document
from apiclient.errors import HttpError
from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
from oauth2client.tools import argparser, run_flow
import pymongo
from youtube_transcript_api import YouTubeTranscriptApi
from bson import json_util
sys.path.append('/YouTubeVideoAnalyzer/DataModels/')
from dataModel import *

CLIENT_SECRETS_FILE = "client_secret.json"

SCOPES = ['https://www.googleapis.com/auth/youtube.force-ssl']
API_SERVICE_NAME = 'youtube'
API_VERSION = 'v3'

# This variable defines a message to display if the CLIENT_SECRETS_FILE is
# missing.
MISSING_CLIENT_SECRETS_MESSAGE = """
WARNING: Please configure OAuth 2.0

To make this sample run you will need to populate the client_secrets.json file
found at:
   %s
with information from the APIs Console
https://console.developers.google.com

For more information about the client_secrets.json file format, please visit:
https://developers.google.com/api-client-library/python/guide/aaa_client_secrets
""" % os.path.abspath(os.path.join(os.path.dirname(__file__),
                                   CLIENT_SECRETS_FILE))

#test function to print the response
def print_response(response):
    print(json.dumps(response))
    
# Remove keyword arguments that are not set
def remove_empty_kwargs(**kwargs):
    good_kwargs = {}
    if kwargs is not None:
        for key, value in kwargs.items():
            if value:
                good_kwargs[key] = value
    return good_kwargs

#invokes the youtube search API to search the youtube videos with keywords.
def search_list_by_keyword(client, **kwargs):
    kwargs = remove_empty_kwargs(**kwargs)
    response = client.search().list(
        **kwargs
        ).execute()
    return response

#get the video id from the dictionary
def getVideoId(dict_id):
    for key,value in dict_id.items():
        if key == 'videoId':
            return value

#get the video details like video published date, channel id, title, description, channel title from the response dictionary
def getVideoDetails(dict_snippet):
    publishedDate =""
    channelId = ""
    channelTitle = ""
    videoTitle = ""
    videoDescription = ""
    
    for key,value in dict_snippet.items():
        if key == 'publishedAt':
            publishedDate = value
        elif key == 'channelId':
            channelId = value
        elif key == 'title':
            videoTitle = value
        elif key == 'description':
            videoDescription = value
        elif key == 'channelTitle':
            channelTitle = value
            
    return publishedDate,channelId,videoTitle,videoDescription,channelTitle

# Authorize the request and store authorization credentials.
def get_authenticated_service(args):
    flow = flow_from_clientsecrets(CLIENT_SECRETS_FILE, scope=SCOPES,
                                   message=MISSING_CLIENT_SECRETS_MESSAGE)

    storage = Storage("%s-oauth2.json" % sys.argv[0])
    credentials = storage.get()

    if credentials is None or credentials.invalid:
        credentials = run_flow(flow, storage, args)

  # Trusted testers can download this discovery document from the developers page
  # and it should be in the same directory with the code.
    with open("youtube-v3-api-captions.json", "r", encoding="utf8") as f:
        doc = f.read()
        return build_from_document(doc, http=credentials.authorize(httplib2.Http()))
  
# # Call the API's captions.list method to list the existing caption tracks.
# def list_captions(youtube, video_id):
#     results = youtube.captions().list(
#         part="snippet",
#         videoId=video_id
#         ).execute()
# 
#     for item in results["items"]:
#         id = item["id"]
#         name = item["snippet"]["name"]
#         language = item["snippet"]["language"]
#         print("Caption track '%s(%s)' in '%s' language." % (name, id, language))
# 
#     return results["items"]
# 
# def download_caption(youtube, caption_id, tfmt = None):
#     subtitle = ""
#     try:
#         subtitle = youtube.captions().download(
#             id=caption_id,
#             tfmt=tfmt
#             ).execute()
#         print(subtitle)      
#     except Exception:
#         print ("Exception occured")
#     
#     return subtitle

#The function uses youtube transcript api to get the captions by extracting the contents of the text key.
#Also, it adds all the videos to the list for which captions are not available.    
def getVideoCaptions(videoId,videoAnalyzer,videosWithExceptions):
    try:
        dictTranscript = YouTubeTranscriptApi.get_transcript(videoId,languages=['en'])
        
        for transcript in dictTranscript:
            if(transcript['text'] != "[Music]" and transcript['text'] != "[Applause]"):
                videoAnalyzer.getCaptions().append(transcript['text'])
    except Exception:
        videosWithExceptions.append(videoId)
        
#The function gets all the video comment threads which are the main comments. 
#Also, it gets the replies to all those comments. 
def getVideoComments(videoId,videoAnalyzer):
    try:
        request = client.commentThreads().list(part="snippet", moderationStatus="published", order="time", videoId=videoId)
        response = request.execute()
        for commentThread in response["items"]:
            parentCommentId = commentThread["snippet"]["topLevelComment"]["id"]
            videoAnalyzer.getComments().append(commentThread["snippet"]["topLevelComment"]["snippet"]["textOriginal"])
            if(commentThread["snippet"]["totalReplyCount"] > 0):
                requestReply = client.comments().list(part="snippet", parentId=parentCommentId)
                responseReply = requestReply.execute()
                for comments in responseReply["items"]:
                    videoAnalyzer.getComments().append(comments["snippet"]["textOriginal"])
    
    except Exception:
        print("Comments have been disabled for this video.")
 
#The function gets all the video statistics like view count, like count, dislike count for the video.
def getVideoStatistics(videoId):
    viewCount = 0
    likeCount = 0
    dislikeCount = 0 
    try:
        request = client.videos().list(part="statistics", id = videoId)
        response = request.execute()
        for stats in response["items"]:
            viewCount = int(stats["statistics"]["viewCount"])
            likeCount = int(stats["statistics"]["likeCount"])
            dislikeCount = int(stats["statistics"]["dislikeCount"])
    except Exception:
        print("Video statistics have been disabled for this video.")
        
    return viewCount,likeCount,dislikeCount

#The function gets all the channel statistics like view count, subscriber count, video upload count for the channel.
def getChannelStatistics(channelId):
    channelViewCount = 0
    channelSubscriberCount = 0
    channelVideoCount = 0
    
    try:
       request = client.channels().list(part="statistics", id = channelId)
       response = request.execute()
       for stats in response["items"]:
           channelViewCount = int(stats["statistics"]["viewCount"])
           channelSubscriberCount = int(stats["statistics"]["subscriberCount"])
           channelVideoCount = int(stats["statistics"]["videoCount"])
    except Exception:
        print("Channel statistics have been disabled for this video.")
        
    return channelViewCount,channelSubscriberCount,channelVideoCount

#This function establishes the connection to mongo db.            
def connectMongoDB():    
    mongoClient = pymongo.MongoClient("mongodb+srv://dbAdmin:dbAdmin@cluster0-lymfp.azure.mongodb.net/test?retryWrites=true")
    db = mongoClient.youtubeVideoAnalyzerTest
    return db

#this function queries the database for  reading the search keys for which topics the youtube videos are to 
#be mined for captions and comments. 
# def readMetaData(db):
#     searchKeysList = [] 
#     table = db.searchKeyDetails
#     searchKeys = table.find()
#     for searchKey in searchKeys:
#         searchKeysList.append(searchKey['searchKey'])
#     return searchKeysList

#class for saving all the video data to the database.
class VideoAnalyzer:
    #initializing all the data members to default values.
    def __init__(self, topic):
        self.topic = topic #topic for which the video was searched.
        self.video_id = 0  #video id
        self.pulled_in_date = "" #data pulled in date and time.
        self.video_title = "" #video title
        self.published_date = "" #video published date.
        self.video_description = "" # video description.
        self.video_link = "" # video url.
        self.captions = [] #list of video captions i.e. content in text format.
        self.comments = [] #list of video comments.
        self.channel_id = "" #video channel id.
        self.channel_name = "" #video channel name.
        self.channel_contributor = "" #channel contributor youtube id.
        self.channel_view_count = 0 #channel view count.
        self.subscriber_count = 0 #channel subscriber count.
        self.num_of_videos_uploaded = 0 # channel videos uploaded by subscriber.
        self.video_like_count = 0 #video like count
        self.video_dislike_count = 0 #video dislike count
        self.video_view_count = 0 #video view count.
    
    #setters and getters for all the class fields.    
    def setVideoId(self,video_id):
        self.video_id = video_id   
        
    def getVideoId(self):
        return self.video_id
    
    def setPulledInDate(self,pulled_in_date):
        self.pulled_in_date = pulled_in_date
    
    def setVideoTitle(self,video_title):
        self.video_title = video_title   
        
    def getVideoTitle(self):
        return self.video_title
    
    def setPublishedDate(self,published_date):
        self.published_date = published_date   
        
    def getPublishedDate(self):
        return self.published_date
    
    def setVideoDescription(self,video_description):
        self.video_description = video_description   
        
    def getVideoDescription(self):
        return self.video_description
    
    def setVideoLink(self,video_link):
        if(video_link is not None):
            video_link = "https://www.youtube.com/watch?v="+video_link
        self.video_link = video_link   
        
    def getVideoLink(self):
        return self.video_link
     
    def setVideoViewCount(self,video_view_count):
        self.video_view_count = video_view_count   
        
    def getVideoViewCount(self):
        return self.video_view_count
    
    def setChannelId(self,channel_id):
        self.channel_id = channel_id   
        
    def getChannelId(self):
        return self.channel_id
    
    def setChannelName(self,channel_name):
        self.channel_name = channel_name   
        
    def getChannelName(self):
        return self.channel_name
    
    def setChannelContributor(self,channel_contributor):
        self.channel_contributor = channel_contributor   
        
    def getChannelContributor(self):
        return self.channel_contributor
    
    def setChannelViewCount(self,channel_view_count):
        self.channel_view_count = channel_view_count
        
    def getChannelViewCount(self):
        return self.channel_view_count
    
    def setSubscriberCount(self,subscriber_count):
        self.subscriber_count = subscriber_count
        
    def getSubscriberCount(self):
        return self.subscriber_count
    
    def setNumOfVideosUploaded(self,num_of_videos_uploaded):
        self.num_of_videos_uploaded = num_of_videos_uploaded   
        
    def getNumOfVideosUploaded(self):
        return self.num_of_videos_uploaded
    
    def setVideoLikeCount(self,video_like_count):
        self.video_like_count = video_like_count   
        
    def getVideoLikeCount(self):
        return self.video_like_count
    
    def setVideoDislikeCount(self,video_dislike_count):
        self.video_dislike_count = video_dislike_count   
        
    def getVideoDislikeCount(self):
        return self.video_dislike_count
    
    def setCaptions(self,captions):
        self.captions = captions   
        
    def getCaptions(self):
        return self.captions
    
    def setComments(self,comments):
        self.comments = comments
        
    def getComments(self):
        return self.comments
    
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)
    
    #function to fire the request to search for videos according to the keyword.
    @staticmethod    
    def searchVideosByTopic(topic):
        #get 50 videos in one request.
        videoDictionary = search_list_by_keyword(client,
                               part ='snippet',
                               maxResults=50,
                               pageToken="",
                               q=topic,
                               relevanceLanguage="en"
                               )
        
        #get the next page token fpr searching next set of videos.
        nextPageToken = videoDictionary["nextPageToken"]
        
        #get next 50 videos.
        nextVideoDictionary = search_list_by_keyword(client,
                               part ='snippet',
                               maxResults=50,
                               pageToken = nextPageToken,
                               q=topic,
                               relevanceLanguage="en"
                               )
        
        #return the list of videos retrieved. 
        return videoDictionary,nextVideoDictionary
    
    #once the videos have been retrieved, get the contents of the videos like video id, channel id,
    #captions, comments, statistics for video and channels by triggering various API requests. 
    @staticmethod
    def processVideoDetails(videoDictionary,videosInfo,topic,pulledInDate,videosWithExceptions):
        for key,value in videoDictionary.items():
            if key == "items":
                for it in value:
                    videoAnalyzer = VideoAnalyzer(topic)
                    videoId = getVideoId(it["id"])
                    videoAnalyzer.setVideoId(videoId)
                    videoAnalyzer.setPulledInDate(pulledInDate)
                    publishedDate,channelId,videoTitle,videoDescription,channelTitle = getVideoDetails(it["snippet"])
                    videoAnalyzer.setPublishedDate(publishedDate)
                    videoAnalyzer.setChannelId(channelId)
                    videoAnalyzer.setVideoTitle(videoTitle)
                    videoAnalyzer.setVideoDescription(videoDescription)
                    videoAnalyzer.setChannelName(channelTitle)
                    videoAnalyzer.setChannelContributor(channelTitle)
                    getVideoCaptions(videoId,videoAnalyzer,videosWithExceptions)
                    getVideoComments(videoId,videoAnalyzer)
                    viewCount,likeCount,dislikeCount = getVideoStatistics(videoId)
                    videoAnalyzer.setVideoViewCount(viewCount)
                    videoAnalyzer.setVideoLikeCount(likeCount)
                    videoAnalyzer.setVideoDislikeCount(dislikeCount)
                    videoAnalyzer.setVideoLink(videoId)
                    if channelId:
                        channelViewCount,channelSubscriberCount,channelVideoCount = getChannelStatistics(channelId)
                        videoAnalyzer.setChannelViewCount(channelViewCount)
                        videoAnalyzer.setSubscriberCount(channelSubscriberCount)
                        videoAnalyzer.setNumOfVideosUploaded(channelVideoCount)
                    videosInfo.append(videoAnalyzer.toJSON())
    
    #function to trigger search of the videos based on the topic and get the details of the videos
    #as class instances of VideoAnalyzer. Save the instances in list videosInfo and returns the list. 
    @staticmethod
    def getVideosInfo(topic,videosWithExceptions):
        videosInfo = []
        now = datetime.datetime.now()
        pulled_in_date = now.strftime("%Y-%m-%d %H:%M")
        videoDictionary,nextVideoDictionary = VideoAnalyzer.searchVideosByTopic(topic)
        VideoAnalyzer.processVideoDetails(videoDictionary,videosInfo,topic,pulled_in_date,videosWithExceptions)
        VideoAnalyzer.processVideoDetails(nextVideoDictionary,videosInfo,topic,pulled_in_date,videosWithExceptions)
        return videosInfo
    
    #function for saving all the data mined for videos to database.
#     @staticmethod
#     def saveVideosInfo(videosInfo):
#         #access the table.
#         productDetails = db.productDetails
#         
#         #delete the existing data.
#         productDetails.delete_many({})
#         
#         data = []
#         for videoInfo in videosInfo:
#             data.append(json_util.loads(videoInfo))
#             
#         #save all the documents to the database.
#         result = productDetails.insert_many(data)
    
    #function to retrieve all the videos according to the search key list retrieved from the database.
    @staticmethod
    def getVideosInfoBySearchWords(db,searchKeysList):
        videosWithExceptions = []
        for searchKey in searchKeysList:
            videosInfo = VideoAnalyzer.getVideosInfo(searchKey,videosWithExceptions)
            DataModel.saveVideosInfo(db,searchKey,videosInfo)
        return videosWithExceptions
                        
if __name__ == '__main__':
    model = DataModel()
    model.connectDb()
    #db = model.getConnection()#uncomment this function once data model is fixed.
    db = connectMongoDB()#can comment this function once data model is fixed.
    searchKeysList = DataModel.readMetaData(db)
    argparser.add_argument("--language", help="Caption track language", default="en")
    argparser.add_argument("--action", help="Action", default="download")
    
    args = argparser.parse_args()
    
    client = get_authenticated_service(args)
    
    videosWithExceptions = VideoAnalyzer.getVideosInfoBySearchWords(db,searchKeysList)



