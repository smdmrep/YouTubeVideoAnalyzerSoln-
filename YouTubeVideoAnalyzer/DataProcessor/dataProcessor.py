import urllib
import urllib.request
from YouTubeVideoAnalyzer.DataModels.dataModel import DataModel
    

class DataProcessor:




    ######################### Initialize ############################
    #............. .................................................#
    #    
    #
    #****************************************************************#
    # Author        :   Guru
    # Created Date  :   04/24/2019          
    # Updated Date  : 
    def __init__(self):
        pass




    ########################## punctuate a given unsegmented data ####################################################################
    #............. Make API call to the Punctuator2 which has been developed by Ottokart with help of deep neural networks...........#
    #    
    #
    #****************************************************************#
    # Author        :   Guru
    # Created Date  :   04/24/2019          
    # Updated Date  : 
    def punctuate(self,caption):
        try:
            url ="http://bark.phon.ioc.ee/punctuator"
            data1 =urllib.parse.urlencode({"text":caption}).encode("utf-8")
            req = urllib.request.Request(url) 
            with urllib.request.urlopen(req,data=data1) as f:
                resp = f.read()
                return str(resp.decode("utf-8"))
        except Exception as e:
            print(e)    



    ########################## process unsegmented data and update segmentedCaptions #######################
    #......................... Entry point of the module...................................................#
    #......................... Take all the unsegmented captions from productDetails table and punctuate them..#
    #......................... Call puncutate function.    
    #
    #****************************************************************#
    # Author        :   Guru
    # Created Date  :   04/24/2019          
    # Updated Date  : 
    def processUnsegmentedTextFromSpeech(self):
        try:
            dataModel = DataModel()
            dataModel.connectDb()

            dataSet = dataModel.getCaptions()

            segmentedDataSet=[]
            for data in dataSet:
                captionArray = data["captions"]
                caption = " ".join(captionArray)
                segmentedCaption = self.punctuate(caption)
                data["captions"] = segmentedCaption
                segmentedDataSet.append(data)
            dataModel.updateCaptions(segmentedDataSet)
        except Exception as e:
            print(e)


# def main():

#    datProcessor= DataProcessor()

#    datProcessor.processUnsegmentedTextFromSpeech()
    

# if __name__ == "__main__":
#     main()