
from YouTubeVideoAnalyzer.VideoScrapper import VideoScrapper
from YouTubeVideoAnalyzer.VideoScrapper.videoExtractScrapper import VideoExtractScrapper
from YouTubeVideoAnalyzer.VideoToTextConverter import *
from YouTubeVideoAnalyzer.DataProcessor.dataProcessor import DataProcessor
from YouTubeVideoAnalyzer.AISystem.NLP_Model import textBlob
from YouTubeVideoAnalyzer.AISystem.NLP_Model import stanfordNLP
from YouTubeVideoAnalyzer.AISystem.documentLevelSentimentAnalyzer import DocumentLevelSentimentAnalyzer


class Wrapper():


    ######################### Initialize ############################
    #............. .................................................#
    #    
    #
    #****************************************************************#
    # Author        :   Ganesh
    # Created Date  :   05/02/2019          
    # Updated Date  : 
    def __init__(self):
        pass
    


    ######################### Perform Youtube video analysis. ############################
    #........................ Extract videos and its captions from youtube...............#
    #........................ Convert video to audio and then to text if scraper cannot extract captions for it..#
    #........................ Process unsegmented data to segmented data.................#
    #........................ Perform document level analysis............................#
    #........................ Perform sentence level analysis............................#    
    #****************************************************************#
    # Author        :   Ganesh
    # Created Date  :   05/02/2019          
    # Updated Date  :
    def performYouTubeVideoAnalysis(self):
        
        #perform video extraction from you tube API. Call out videoExtractScrapper.py for exception

        #perform data processing of unsegmented data.. Calling DataProcessor from dataProcessor.py
        dataProcessor = DataProcessor()
        dataProcessor.processUnsegmentedTextFromSpeech()


        #perform document analysis
        documentAnalyzer=DocumentLevelSentimentAnalyzer()
        documentAnalyzer.performDocumentAnalysis()
        documentAnalyzer.generateOverallScores()


        #perform sentiment analysis





def main():
    print(".............Welcome To YouTube Video Analysis..............")
    wrapper = Wrapper()
    wrapper.performYouTubeVideoAnalysis()

if __name__ == "__main__":
    main()



