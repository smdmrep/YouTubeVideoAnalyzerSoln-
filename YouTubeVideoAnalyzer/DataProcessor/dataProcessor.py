import urllib
import urllib.request
from YouTubeVideoAnalyzer.DataModels.dataModel import DataModel
    

class DataProcessor:



    def punctuate(self,caption):
        url ="http://bark.phon.ioc.ee/punctuator"
        data1 =urllib.parse.urlencode({"text":caption}).encode("utf-8")
        req = urllib.request.Request(url) 
        with urllib.request.urlopen(req,data=data1) as f:
            resp = f.read()
            return str(resp.decode("utf-8"))
            

    def processUnsegmentedTextFromSpeech(self,dataSet):
        
        segmentedDataSet=[]
        for data in dataSet:
            captionArray = data["captions"]
            caption = " ".join(captionArray)
            segmentedCaption = self.punctuate(caption)
            data["captions"] = segmentedCaption
            segmentedDataSet.append(data)
            
         

        return segmentedDataSet

# def main():

#     datProcessor= DataProcessor()

#     dataModel = DataModel()
#     dataModel.connectDb()
    
#     dataSet = dataModel.getCaptions()
#     processedDataSet = datProcessor.processUnsegmentedTextFromSpeech(dataSet)
    
#     dataModel.updateCaptions(processedDataSet)

# if __name__ == "__main__":
#     main()