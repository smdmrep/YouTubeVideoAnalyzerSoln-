# YouTubeVideoAnalyzerSoln-


## Project Idea:
  The objective of our project is to perform sentimental analysis on the youtube videos to determine the sustainability of the product in the market. In extension to this, the opinions of NEWS channels in youtube toward the public figures are outlined.


## Project Description:
Due to the fast growing internet, Youtube has become one of the top social media for every topic. It offers a wide variety of user-generated and corporate media videos which ranges from educational to entertainment. Available content includes video clips, TV show clips, music videos, short and documentary films, audio recordings, movie trailers, live streams, and other content such as video blogging, short original videos, and educational videos. Most of the content on YouTube is uploaded by individuals, but media corporations including CBS, the BBC, Vevo, and Hulu offer some of their material via YouTube as part of the YouTube partnership program. Because of its tremendous data, mining and processing them is a very challenging task.  

Analysis of the content of the platform as a whole is not deterministic and impractical, an attempt is made towards analyzing the contents dedicated towards tech products from technology-focused videos.

We extract the content of youtube videos followed by the processing and training of the data produced by conversion of video to text. In our approach, we use NLP (Natural Language Processing) algorithms to achieve the objective.

## Significance of Project:
  Analyzation will provide a probability of the product success which is drawn from the reviews of youtube content providers. (Example: Samsung S10)




----------------------------------------------------------------------------------------------------------------------------------------
## Setting up the project environment:-




Required Files and python packages:


### VideoScrapper using youtube API
Install the following API's using pip command.

	1) google-api-python-client 1.7.8
	python -m pip install google-api-python-client
	2) google-auth              1.6.3
	python -m pip install google-auth
	3) google-auth-httplib2     0.0.3
	python -m pip install google-auth-httplib2
	4) google-auth-oauthlib     0.3.0
	python -m pip install google-auth-oauthlib
	5) httplib2                 0.12.1
	python -m pip install httplib2
	6) idna                     2.8
	python -m pip install idna
	7) oauth2client             4.1.3
	python -m pip install oauth2client
	8) oauthlib                 3.0.1
	python -m pip install oauthlib
	9) pip                      19.1.1
	python -m pip install pip
	10) pyasn1                   0.4.5
	python -m pip install pyasn1
	11) pyasn1-modules           0.2.4
	python -m pip install pyasn1-modules
	12) pycparser                2.19
	python -m pip install pycparser
	13) pymongo                  3.7.2
	python -m pip install pymongo
	14) requests                 2.21.0
	python -m pip install requests
	15) requests-oauthlib        1.2.0
	python -m pip install requests-oauthlib
	16) rsa                      4.0
	python -m pip install rsa
	17) setuptools               40.6.2
	python -m pip install setuptools
	18) six                      1.12.0
	python -m pip install six
	19) Unidecode                1.0.23
	python -m pip install Unidecode
	20) uritemplate              3.0.0
	python -m pip install uritemplate
	21) urllib3                  1.24.1
	python -m pip install urllib3
	22) youtube-dl               2019.4.30
	python -m pip install youtube-dl
	23) youtube-transcript-api   0.1.3
	python -m pip install youtube-transcript-api
	24) appier                   1.18.7
	python -m pip install appier
	25) cachetools               3.1.0
	python -m pip install cachetools
	26) certifi                  2019.3.9
	python -m pip install certifi
	27) cffi                     1.12.3
	python -m pip install cffi
	28) chardet                  3.0.4
	python -m pip install chardet
	29) decorator                4.3.2
	python -m pip install decorator
	30) dnspython                1.16.0
	python -m pip install dnspython
	31) ffmpeg                   1.4
	python -m pip install ffmpeg
	32) ffprobe                  0.5
	python -m pip install ffprobe


### Video to Text Converter:

	1)
	2)
	3)
	4)
	5)




### Data PreProcessor

	
	1) Run python -m pip install urllib





### DataModel using MongoDb driver in python (DataModel.py)

	
	1) Run python -m pip install pymongo
	2) Run python -m pip install dnspython
	





### AISystem - Document Level Analysis (documentLevelSentimentAnalyzer.py) : Follow these instruction

	1) Run python -m pip install nltk --user
	
	2) Run following script to download all the nltk toolkit:
			import nltk
			nltk.download('stopwords')
			nltk.download('punkt')
			nltk.download('averaged_perceptron_tagger')
			nltk.download('wordnet')
			nltk.download('sentiwordnet')
			






### AISystem - Sentence Level Analysis(NLP_Model.py) : Follow these setup instruction.


	1) 	curl https://nlp.stanford.edu/software/stanford-corenlp-full-2018-10-05.zip -O https://nlp.stanford.edu/software/stanford-english-corenlp-2018-10-05-models.jar -O
		(Download Stanford CoreNLP - Built on Java Language)
		(Importance - Allows us to use the pre-trained model to do sentiment analysis)
		(If Failed : Download from http://nlp.stanford.edu/software/stanford-english-corenlp-2018-10-05-models.jar)
		
	2) 	unzip stanford-corenlp-full-2018-10-05.zip
		mv stanford-english-corenlp-2018-10-05-models.jar stanford-corenlp-full-2018-10-05
		(Install the Stanford CoreNLP package)
	
	3) 	cd stanford-corenlp-full-2018-10-05
		java -mx5g -cp "*" edu.stanford.nlp.pipeline.StanfordCoreNLPServer -timeout 10000
		(Start the server - needed to access the Stanford libraries from python)
	
	4) 	pip install pycorenlp
		(Install pycorenlp libraries)
		(Python Wrapper around the Stanford NLP libraries)
	
	5) pip install -U textblob
		(Install the textblob libraries)
		(Importance - Allows us to get the polarity of the statement)
	
	6)	Install java (If java is not already installed)
		(Source : https://www.oracle.com/technetwork/java/javase/downloads/jdk12-downloads-5295953.html)






### Visualizer

	
	1)	Dependencies:
			async
			express
			express-handlebars
			mongodb

	2)	Download and install node.js  - https://nodejs.org/en/download/

	3)	Run npm install
	
	4) 	Run npm start - to start a server. 






### Initial Setup: Follow these instruction for project as package.


	1)	CD C:/path_to_project/YouTubeVideoAnalyzerSoln-
	2)	Run python config.py to initialize configuration files.
	3)	Once complete, Run python setup.py install --user










#### Author
#### [Guruprasanna Hegde](https://github.com/guruprasannahegde)



