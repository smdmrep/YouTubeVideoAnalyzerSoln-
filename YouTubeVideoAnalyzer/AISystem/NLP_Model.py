###########################################################################
# NLP_Model.py  : Provides functions to preform Sentiment analysis        #        
# ver           : 1.0                                                     #
# OS            : Windows 10 (64 bit)                                     #
# Author        : Ganesh Mamatha Sheshappa                                #
#                 gmamatha@syr.edu                                        #
#                 +1 (315)-378-7890                                       #
###########################################################################

# Package Operations:
# -------------------
# Provides the functions to determine the  sentiment of the given 
# statement / paragraph / text.

# Required Files:
# ---------------
# None

# Packages / Libraries / Tools to be installed or downloaded :
# ------------------------------------------------------------
# 1) curl https://nlp.stanford.edu/software/stanford-corenlp-full-2018-10-05.zip -O https://nlp.stanford.edu/software/stanford-english-corenlp-2018-10-05-models.jar -O
#   (Download Stanford CoreNLP - Built on Java Language)
#   (Importance - Allows us to use the pre-trained model to do sentiment analysis)
#    (If Failed : Download from http://nlp.stanford.edu/software/stanford-english-corenlp-2018-10-05-models.jar)
#    
# 2) unzip stanford-corenlp-full-2018-10-05.zip
#    mv stanford-english-corenlp-2018-10-05-models.jar stanford-corenlp-full-2018-10-05
#    (Install the Stanford CoreNLP package)
#
# 3) cd stanford-corenlp-full-2018-10-05
#    java -mx5g -cp "*" edu.stanford.nlp.pipeline.StanfordCoreNLPServer -timeout 10000
#    (Start the server - needed to access the Stanford libraries from python)
#
# 4) pip install pycorenlp
#    (Install pycorenlp libraries)
#    (Python Wrapper around the Stanford NLP libraries)
#
# 5) pip install -U textblob
#   (Install the textblob libraries)
#   (Importance - Allows us to get the polarity of the statement)
#
# 6) Install java (If java is not already installed)
#  (Source : https://www.oracle.com/technetwork/java/javase/downloads/jdk12-downloads-5295953.html)
#

# Reference Lins
# ---------------
# 1) https://stackoverflow.com/questions/32879532/stanford-nlp-for-python
# 2) https://textblob.readthedocs.io/en/dev/install.html
# 3) https://stanfordnlp.github.io/CoreNLP/other-languages.html
# 4) https://github.com/dasmith/stanford-corenlp-python
# 5) https://www.youtube.com/watch?time_continue=189&v=f7rT0h1Q5Wo

# Maintenance History
# -------------------
# ver 1.0 : 20 Apr 2019


#--------------< Import all the neccesary Libraries >-----------------
from textblob import TextBlob
from pycorenlp import StanfordCoreNLP
import nltk.data
import sys
from dataModel import *

#--------------< Using textblob libraries for sentiment analysis >-----------------
class textBlob:
    '''
    Funciton Name       : sentimentAnalyserTB
    Function Descryption: 
    Function Input Args : dotSeparatedTxt - Dot separated sentences on which,
                          sentiment analysis needs to be performed
    Function Returns    : Output sentiment values list for the input sentences ranging
                          from -1 to +1 (-1 Negative, +1 Positive)
    '''
    def sentimentAnalyserTB(self, dotSeparatedTxt, verbose = False):
        try:
            sentimentValue = []
            ipTxt = TextBlob(dotSeparatedTxt)
            for sentence in ipTxt.sentences:
                if(verbose):
                    print("Sentence: ", sentence , " Value : " , sentence.sentiment.polarity)
                sentimentValue.append(sentence.sentiment.polarity)
            return sentimentValue
        except:
            print ("There was a problem in TextBlob libraries!")

#Analysis of the sentiment percentage for the Stanford NLP libraries
def countOcc(lst, x): 
    count = 0
    for ele in lst: 
        if (ele == x): 
            count = count + 1
    return count

#--------------< Using Stanford Core-NLP libraries for sentiment analysis >-----------------
class stanfordNLP:
    '''
    Funciton Name       : sentimentAnalyserSF
    Function Descryption: 
    Function Input Args : dotSeparatedTxt - Dot separated sentences on which,
                          sentiment analysis needs to be performed
    Function Returns    : Output sentiment values list for the input statement ranging
                          from 0 to 4 (0 Very Negative, 1 Negative, 2 Neutral, 
                          3 Positive, 4 Very Positive)
    '''
    def sentimentAnalyserSF(self, dotSeparatedTxt , verbose = False):
        try:
            sentimentValue = []
            nlp = StanfordCoreNLP('http://localhost:9000')
            res = nlp.annotate(dotSeparatedTxt,
                   properties={
                       'annotators': 'sentiment',
                       'outputFormat': 'json',
                       'timeout': 10000,
                   })
            for s in res["sentences"]:
                sentimentValue.append(int(s["sentimentValue"]))
                if(verbose):
                    print("%d: '%s': %s %s" % (
                    s["index"],
                    " ".join([t["word"] for t in s["tokens"]]),
                    s["sentimentValue"], s["sentiment"]))
            return sentimentValue
        except:
            print ("There was a problem in Standford NLP libraries!")

    def generateSentenceLevelScore(self,opinion):
        return "a"

    def sentimentPercentageCalculate(self, sf_analysis_list):
        try:
            sentence_count_sf = len(sf_analysis_list)
            sf_pos_count = countOcc(sf_analysis_list, 3) + countOcc(sf_analysis_list,4)
            sf_neg_count = countOcc(sf_analysis_list, 0) + countOcc(sf_analysis_list, 1)
            sf_neu_count = countOcc(sf_analysis_list, 2)
            sentiment_result = []
            if(sentence_count_sf == 0):
               return None
            else:
                sentiment_result.append(sf_pos_count/sentence_count_sf*100)
                sentiment_result.append(sf_neg_count/sentence_count_sf*100)
                sentiment_result.append(sf_neu_count/sentence_count_sf*100)
            return sentiment_result
        except:
            print ("There was a problem in sentiment percentage calculater for Stanford Analysis!")

    def sentenceLevelAnalyzer(self):
        try:
            sentenceLevelAnalysis()
        except:
            print ("There was a problem in sentiment percentage calculater for Stanford Analyzer!")

def sentenceLevelAnalysis():
    try:
        dataModel = DataModel()
        dataModel.connectDb()
        segmentedCaptions = dataModel.getSegmentedCaptions()
        analyzedDataSet=[]
        overallSentResult = [0,0,0]
        stanfordnlp = stanfordNLP()
        count = 0
        for data in segmentedCaptions:
            if "segmentedCaptions" in data:
                #analyzedDataSet=[]
                sentimentResults = []
                print("Processed :", count, " files ")
                sf_analysis_list = stanfordnlp.sentimentAnalyserSF(data["segmentedCaptions"], verbose = False)
                # PositiveScore NegativeScore NeutralScore
                sentimentResults = stanfordnlp.sentimentPercentageCalculate(sf_analysis_list)
                if(sentimentResults != None):
                    count = count + 1
                    data["sentenceLevelScore"] = {"positive":sentimentResults[0], "negative":sentimentResults[1], "neutrality":sentimentResults[2]} 
                    analyzedDataSet.append(data)
                    #dataModel.updateSentenceLevelAnalysis(analyzedDataSet)
        
        dataModel.updateSentenceLevelAnalysis(analyzedDataSet)
        generateOverallSentenceScore(dataModel)
    except Exception as e:
        print(e)

def generateOverallSentenceScore(dataModel):
    searchKeyResults = dataModel.getSearchkeyList()
    for key in searchKeyResults:
        sentenceScoreList = dataModel.getSentenceScores(key["searchKey"])
        positiveScoreArray = sentenceScoreList[0]["positive"]
        negativeScoreArray = sentenceScoreList[1]["negative"]
        neutralScoreArray = sentenceScoreList[2]["neutrality"]
        count = sentenceScoreList[3]["count"]
            
        positiveScore = 0 if count == 0 else sum(positiveScoreArray)/count
        negativeScore = 0 if count == 0 else sum(negativeScoreArray)/count
        neutralScore = 0 if count == 0 else  sum(neutralScoreArray)/count
        dataModel.updateSentenceOverallScore({"searchKey": key["searchKey"],"sentencePositive":round(positiveScore, 2),"sentenceNegative" : round(negativeScore, 2),"sentenceNeutral": round(neutralScore, 2) })


#def main():
#    try:
#        sentenceLevelAnalysis()
#        print("Done")
#        ##--------< Test Stub for the NLP_Model.py module >-------
#        #print("Test Stub for NLP_Model.py")
#        #print("--------------------------")

#        #dotSepTxt = "This is very good day. But yesterday was bad. Tomorrow will be a wonderful day. Madhu is good boy. This is good DAy. "
#        #tb = textBlob()
#        #print(tb.sentimentAnalyserTB(dotSepTxt, verbose = False))
#        #sf = stanfordNLP()
#        #print(sf.sentimentAnalyserSF(dotSepTxt, verbose = False))

#        #a = DataModel()
#        #a.connectDb()
#        #a.getCollectionResults("productDetails")

#     #--------< Error Handling >-------
#    except IOError:
#        print('Handled Error: An error occured trying to read the file.')
    
#    except ValueError:
#        print('Handled Error: Non-numeric data found in the file.')

#    except NameError:
#        print("Handled Error: Name Error has occured - Variable not defined.")

#    except ImportError:
#        print("Handled Error: Module not found")
    
#    except EOFError:
#        print("Handled Error: EOF Error")

#    except KeyboardInterrupt:
#        print("Handled Error: Operation inturrupted by keyboard")

#    except:
#        print("Handled Error: An Unknown error occured.")

#if __name__ == "__main__":
#    main()

