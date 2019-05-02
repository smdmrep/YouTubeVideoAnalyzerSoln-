
from YouTubeVideoAnalyzer.VideoScrapper import VideoScrapper
from YouTubeVideoAnalyzer.VideoScrapper.videoExtractScrapper import VideoExtractScrapper
from YouTubeVideoAnalyzer.VideoToTextConverter import *
from YouTubeVideoAnalyzer.DataProcessor.dataProcessor import DataProcessor
from YouTubeVideoAnalyzer.AISystem.NLP_Model import textBlob
from YouTubeVideoAnalyzer.AISystem.NLP_Model import stanfordNLP
from YouTubeVideoAnalyzer.AISystem.documentLevelSentimentAnalyzer import DocumentLevelSentimentAnalyzer


class Wrapper():

    def __init__(self):
        pass
    

    def performYouTubeVideoAnalysis(self):
        
        #perform video extraction from you tube API. Call out videoExtractScrapper.py for exception

        #perform data processing of unsegmented data.. Calling DataProcessor from dataProcessor.py
        dataProcessor = DataProcessor()
        dataProcessor.processUnsegmentedTextFromSpeech()


        #perform document analysis
        documentAnalyzer=DocumentLevelSentimentAnalyzer()
        documentAnalyzer.performDocumentAnalysis()


        #perfor sentiment analysis





def main():
    print(".............Welcome To YouTube Video Analysis..............")
    wrapper = Wrapper()
    wrapper.performYouTubeVideoAnalysis()

if __name__ == "__main__":
    main()



