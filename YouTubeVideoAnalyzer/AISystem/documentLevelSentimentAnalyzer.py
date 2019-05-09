import nltk
import ast
import re
from nltk.tokenize import  word_tokenize
from nltk.corpus import wordnet
from nltk.corpus import sentiwordnet
from nltk.stem import WordNetLemmatizer
from YouTubeVideoAnalyzer.DataModels.dataModel import DataModel


class DocumentLevelSentimentAnalyzer():


    ######################### Initialize ############################
    #............. .................................................#
    #    
    #
    #****************************************************************#
    # Author        :   Guru
    # Created Date  :   04/25/2019          
    # Updated Date  : 
    def __init__(self):
        pass
    



    ######################### Preprocessing of the raw data ############################
    #........................ Currently not in use.....................................#
    #........................ Removes all stop words in the string using nltk.corpus...#    
    #
    #****************************************************************#
    # Author        :   Guru
    # Created Date  :   04/25/2019          
    # Updated Date  : 
    def preProcessing(self,data):
        try:        
            data = data.lower()
            cachedStopWords = nltk.corpus.stopwords.words("english")
            removedStopWords=(' '.join([word for word in data.split() if word not in cachedStopWords]))
            return removedStopWords
        except Exception as e:
            print(e)
            return None

        


    ######################### Tokenize the segmentedcaption ############################
    #........................ Take each sentence and tokenize them from entire paragraph of segmented captions...#    
    #
    #****************************************************************#
    # Author        :   Guru
    # Created Date  :   04/25/2019          
    # Updated Date  : 
    def tokenizeWords(self,segmentedCaptions):
        try:            
            tokenizedWords={}
            tokenizer = nltk.tokenize.punkt.PunktSentenceTokenizer()
            uniqueID = 1


            for sentence in tokenizer.tokenize(segmentedCaptions):
                tokenizedWords[uniqueID]= sentence
                uniqueID+=1
            return str(tokenizedWords)
        except Exception as e:
            print(e)
            return None



    ######################### POS tagger ############################
    #........................ tag all words with assosciated parts of speech...#    
    #........................ using nltk.postag
    #****************************************************************#
    # Author        :   Guru
    # Created Date  :   04/25/2019          
    # Updated Date  : 
    def partOfSpeechRecognition(self,tokenizedWords):
        try:
            inputTupples = ast.literal_eval(tokenizedWords)

            outputPost = {}

            for key,value in inputTupples.items():
                outputPost[key]=nltk.pos_tag(nltk.word_tokenize(value))
            return str(outputPost)
        except Exception as e:
            print(e)
            return None


    ######################### Aspect extraction. ############################
    #........................ Find all occurences of Noun, Proper Noun ...#    
    #........................ using pos tagged text from partOfSpeechRecognition(tokenizedWords) method.
    #****************************************************************#
    # Author        :   Guru
    # Created Date  :   04/25/2019          
    # Updated Date  : 
    def aspectExtraction(self,outputPost):
        try:    
            inputTupples = ast.literal_eval(outputPost)
            prevWord = ""
            currWord = ""
            prevTag = ""
            aspectList=[]
            outputDict={}

            for key,value in inputTupples.items():
                for word,tag in value:
                    if(tag=='NN' or tag=='NNP'):
                        if(prevTag=='NN' or prevTag=='NNP'):
                            currWord= prevWord + ' ' + word
                        else:
                            aspectList.append(prevWord.upper())
                            currWord= word
                    prevWord=currWord
                    prevTag=tag

            for aspect in aspectList:
                if(aspectList.count(aspect)>1):
                        if(outputDict.keys()!=aspect):
                                outputDict[aspect]=aspectList.count(aspect)
            outputAspect=sorted(outputDict.items(), key=lambda x: x[1],reverse = True)


            return str(outputAspect)
        except Exception as e:
            print(e)
            return None




    ######################### Orient the aspect list. ############################
    #........................ check whether they are more positive or more negative...#    
    #........................ using sentiwornet.
    #****************************************************************#
    # Author        :   Guru
    # Created Date  :   04/25/2019          
    # Updated Date  : 
    def orientation(self,inputWord): 
        try:
            wordSynset=wordnet.synsets(inputWord)
            if(len(wordSynset) != 0):
                word=wordSynset[0].name()
                orientation=sentiwordnet.senti_synset(word)
                if(orientation.pos_score()>orientation.neg_score()):
                    return True
                elif(orientation.pos_score()<orientation.neg_score()):
                    return False 
        except Exception as e:
            print(e)
            return None


    ######################### Identify the opinion words. ############################
    #........................ handle negative wordset like don't, can't etc...#    
    #........................ using Adjective (JJR), Adverb(RRB) either comparitive or superlative.
    #****************************************************************#
    # Author        :   Guru
    # Created Date  :   04/25/2019          
    # Updated Date  :
    def identifyOpinionWords(self,posTagged,aspectList):

        try:
            posTaggedTupples = ast.literal_eval(posTagged)
            aspectTupplues = ast.literal_eval(aspectList)

            outputAspectOpinionTuples={}
            orientationCache={}

            negativeWordSet = {"don't","never", "nothing", "nowhere", "noone", "none", "not",
                    "hasn't","hadn't","can't","couldn't","shouldn't","won't",
                    "wouldn't","don't","doesn't","didn't","isn't","aren't","ain't"}

            for aspect,no in aspectTupplues:
                aspectTokens= word_tokenize(aspect)
                count=0
                for key, value in posTaggedTupples.items():
                    condition = True
                    isNegative = False
                    for subWord in aspectTokens:
                        if(subWord in str(value).upper()):
                            condition = condition and True
                        else:
                            condition = condition and False
                    
                    if(condition):
                        for negword in negativeWordSet:
                            if(not isNegative):
                                if negword.upper() in str(value).upper():
                                    isNegative = isNegative or True
                
                        outputAspectOpinionTuples.setdefault(aspect,[0,0,0])
                    

                        for word,tag in value:
                            if(tag=='JJ' or tag=='JJR' or tag=='JJS'or tag== 'RB' or tag== 'RBR'or tag== 'RBS'):
                                count = count+1
                                if(word not in orientationCache):
                                    orien=self.orientation(word)
                                    orientationCache[word]=orien
                                else:
                                    orien = not orien
                                if(isNegative and orien is not None):
                                    orien = not orien
                                if(orien==True):
                                    outputAspectOpinionTuples[aspect][0]+=1
                                elif(orien==False):
                                    outputAspectOpinionTuples[aspect][1]+=1
                                elif(orien is None):
                                    outputAspectOpinionTuples[aspect][2]+=1


                if(count>0):
                    outputAspectOpinionTuples[aspect][0]=round((outputAspectOpinionTuples[aspect][0]/count)*100,2)
                    outputAspectOpinionTuples[aspect][1]=round((outputAspectOpinionTuples[aspect][1]/count)*100,2)
                    outputAspectOpinionTuples[aspect][2]=round((outputAspectOpinionTuples[aspect][2]/count)*100,2)
                    #print(aspect,':\t\tPositive => ', outputAspectOpinionTuples[aspect][0], '\tNegative => ',outputAspectOpinionTuples[aspect][1])
            
            return outputAspectOpinionTuples
        except Exception as e:
            print(e)
            return None




    ######################### Perform document(aspect level analysis) ############################
    #........................ entry point of the module...#    
    #........................ get segmented captions and perform document level analysis and perform bulk update of each individual score.
    #****************************************************************#
    # Author        :   Guru
    # Created Date  :   04/25/2019          
    # Updated Date  :
    def performDocumentAnalysis(self):
        try:
            dataModel = DataModel()
            dataModel.connectDb()
            segmentedCaptions = dataModel.getSegmentedCaptions()
        
            documentAnalyzer = DocumentLevelSentimentAnalyzer()

            count = 0
            analyzedDataSet =[]
            for data in segmentedCaptions:
                #   preProcessedText = documentAnalyzer.preProcessing(data["segmentedCaptions"])
                if "segmentedCaptions" in data:
                    tokenizedWords=documentAnalyzer.tokenizeWords(data["segmentedCaptions"])
                    taggedWords = documentAnalyzer.partOfSpeechRecognition(tokenizedWords)
                    aspectList = documentAnalyzer.aspectExtraction(taggedWords)
                    opinion = documentAnalyzer.identifyOpinionWords(taggedWords,aspectList)
                    data["documentScore"]=documentAnalyzer.generateDocumentLevelScore(opinion)
                    data["documentAspectList"]=opinion
                    count=count+1
                    analyzedDataSet.append(data)
                    #dataModel.updateDocumentLevelAnalysis(analyzedDataSet)
            dataModel.updateDocumentLevelAnalysis(analyzedDataSet)
        
        except Exception as e:
            print(e)




    ######################### Generate document level score based on list of all individual video score list############################
    #****************************************************************#
    # Author        :   Guru
    # Created Date  :   04/25/2019          
    # Updated Date  :
    def generateDocumentLevelScore(self,opinion):
        try:

            positiveScoreList=[]
            negativeScoreList=[]
            neutralityScoreList=[]
            opinionScore={}
            for key,value in opinion.items():
                positiveScoreList.append(value[0])
                negativeScoreList.append(value[1])
                neutralityScoreList.append(value[2])
        

            positiveLen=len(positiveScoreList)
            if(positiveLen==0):
                opinionScore["positive"]=0
            else:
                positiveSum=sum(positiveScoreList)
                opinionScore["positive"]=positiveSum/positiveLen

        
            negativeLen=len(negativeScoreList)
            if(negativeLen==0):
                opinionScore["negative"]=0
            else:
                negativeSum=sum(negativeScoreList)
                opinionScore["negative"]=negativeSum/negativeLen

        
            neutralityLen=len(neutralityScoreList)
            if(neutralityLen==0):
                opinionScore["neutrality"]=0
            else:
                neutralitySum=sum(neutralityScoreList)
                opinionScore["neutrality"]=neutralitySum/neutralityLen

            return opinionScore
        except Exception as e:
            print(e)
            return None
        


    ######################### Generate document level score for entire product.############################
    #****************************************************************#
    # Author        :   Guru
    # Created Date  :   04/25/2019          
    # Updated Date  :        
    def generateOverallScores(self):
        try:
            dataModel = DataModel()
            dataModel.connectDb()
            searchKeyResults = dataModel.getSearchkeyList()
            for key in searchKeyResults:
                documentScoreList = dataModel.getDocumentScores(key["searchKey"])
                
                positiveScoreArray = documentScoreList[0]["positive"]
                negativeScoreArray = documentScoreList[1]["negative"]
                neutralScoreArray = documentScoreList[2]["neutral"]
                count = documentScoreList[3]["count"]

                positiveScore = 0 if count == 0 else sum(positiveScoreArray)/count
                negativeScore = 0 if count == 0 else sum(negativeScoreArray)/count
                neutralScore = 0 if count == 0 else  sum(neutralScoreArray)/count
                dataModel.insertDocumentOverallScore({"searchKey": key["searchKey"],"documentPositive":round(positiveScore, 2),"documentNegative" : round(negativeScore, 2),"documentNeutral": round(neutralScore, 2) }) 
        except Exception as e:
            print(e)
        
# def main():

#     documentAnalyzer=DocumentLevelSentimentAnalyzer()
#     documentAnalyzer.performDocumentAnalysis()
#     documentAnalyzer.generateOverallScores()


# if __name__ == "__main__":
#     main()