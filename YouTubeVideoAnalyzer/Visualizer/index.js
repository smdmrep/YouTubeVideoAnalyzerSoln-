/*
###########################################################################
# index.js      : Displays the analysis on to web app using node.js       #        
# ver           : 1.0                                                     #
# Authors       : Madhu Jayarama                                          #
###########################################################################

# Dependencies :
# ------------------------------------------------------------
# * async
# * express
# * express-handlebars
# * mongodb
#
# How to Run :
# ------------------------------------------------------------
# $ npm install
#   (installs the Dependencies)
#
# $ npm start
#   (starts the server)
#
# Maintenance History
# -------------------
# ver 1.0 : 4 May 2019
*/

const express = require('express');
const path = require('path');
const exphbs = require('express-handlebars');
const mongo = require('mongodb');
const MongoClient = require('mongodb').MongoClient;

const PORT = process.env.PORT || 3000;
const uri = "mongodb+srv://dbAdmin:dbAdmin@cluster0-lymfp.azure.mongodb.net/test?retryWrites=true&retries = Infinity";
const dbName = "youtubeVideoAnalyzerTest";

const app = express();

app.engine('handlebars', exphbs({defaultLayout: 'main'}));
app.set('view engine', 'handlebars');

var numberOfSearchKey = 0;
var numberOfVideos = 0;
var products = Array;

const client = new MongoClient(uri, { useNewUrlParser: true });
client.connect(err => {
    const searchKeyCollection = client.db(dbName).collection("youtubeVideoAnalyzedScore");
    const productCollection = client.db(dbName).collection("productDetails");

    searchKeyCollection.find().toArray((err, items) => {
        products = items;
        numberOfSearchKey = items.length;
    });

    productCollection.find().toArray((err, items) => {
        numberOfVideos = items.length;
        console.log("error: " + err);
    });
    //client.close();
});

app.get('/', (request, response) => {
    console.log('Redirecting to index page');
    response.render('index', {
        numberOfSearchKey: numberOfSearchKey,
        numberOfVideos: numberOfVideos,
    });
});

app.get('/home', (request, response) => {
    console.log('Redirecting to home page');
    response.render('index', {
        numberOfSearchKey: numberOfSearchKey,
        numberOfVideos: numberOfVideos
    });
});

app.get('/product', (request, response) => {
    console.log('Redirecting to product page');
    response.render('product', {
        products
    });
});

app.get('/product_analysis', (request, response) => {
    var id = mongo.ObjectID(request.query._id);
    var productName = "";
    var documentPositive = 0;
    var documentNegative = 0;
    var documentNeutral = 0;
    var sentencePositive = 0;
    var sentenceNegative = 0;
    var sentenceNeutral = 0;

    client.connect(err => {
        //youTubeVideoAnalysedScore
        const youTubeVideoAnalysedScoreCollection = client.db(dbName).collection("youtubeVideoAnalyzedScore");
    
        youTubeVideoAnalysedScoreCollection.findOne({_id: id}, (err, item) => {
            productName = item.searchKey;
            documentPositive = item.documentPositive;
            documentNegative = item.documentNegative;
            documentNeutral = item.documentNeutral;
            sentencePositive = item.sentencePositive;
            sentenceNegative = item.sentenceNegative;
            sentenceNeutral = item.sentenceNeutral;

            var videoPositive = 0;

            const productCollection = client.db(dbName).collection("productDetails");

            productCollection.find({topic: productName}).toArray((err, videos) => {
                response.render('product_analysis', {
                    productName: productName,
                    documentPositive: documentPositive,
                    documentNegative: documentNegative,
                    documentNeutral: documentNeutral,
                    sentencePositive: sentencePositive,
                    sentenceNegative: sentenceNegative,
                    sentenceNeutral: sentenceNeutral,
                    videos: videos,
                    videoPositive: videoPositive
                });
            });
            
            
        })

        //client.close();
    });

    console.log('Redirecting to product_analysis page');
});

app.use(express.static(path.join(__dirname, 'public')));

app.listen(PORT, () => console.log(`Server runnning on port ${PORT}`));