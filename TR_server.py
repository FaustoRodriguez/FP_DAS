import pymongo
from bson.objectid import ObjectId
from datetime import datetime
from collections import Counter

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["mydatabase"]
    
def logEvent(actionType,user):
    events = mydb["events"]
    events.insert_one({"actionType":actionType,"user":user})
    
def PostTweet(user,tweet):
    tweets = mydb["tweets"]
    tweets.insert_one({"user":user,"tweet":tweet,"type":"tweet"})
    logEvent("create tweet",user)
    
def PostComment(tweetID,user,comment):
    comments = mydb["comments"]
    tweets = mydb["tweets"]
    tweets.update_one({"_id":ObjectId(tweetID)},{"$set":{"type":"thread"}})
    comments.insert_one({"tweetID":tweetID,"user":user,"comment":comment})
    logEvent("reply tweet",user)
    
def getTimeStamp(id):
    return ObjectId(id).generation_time
    
def GetTweet(tweetID):
    tweets = mydb["tweets"]
    for tweet in tweets.find({"_id":ObjectId(tweetID)}):
        return tweet

def GetComments(tweetID):
    return mydb["comments"].find({"tweetID":tweetID})

def getEvents():
    return mydb["events"].find()

def GetLatestTweets(nTweets):
    tweets = mydb["tweets"]
    latestTweets = []
    for tweet in tweets.find().sort("_id", -1):
        nTweets -= 1
        latestTweets.append(tweet)
        if not nTweets :
            break
    return latestTweets

def GetTodayUsers():
    openings = GetTodayValues("events",{"actionType":"open application"},"user")
    users = {}
    for opening in openings:
            users[opening] = True
    return len(users)

def GetTodayMostCommentedTweet():
    tweets = Counter(GetTodayValues("comments",{},"tweetID"))
    v = list(tweets.values())
    k = list(tweets.keys())
    return k[v.index(max(v))]

def GetTodayMostActiveUser():
    users = Counter(GetTodayValues("events",{},"user"))
    v = list(users.values())
    k = list(users.keys())
    return k[v.index(max(v))]

def GetTodayValues(collection,query,key):
    col = mydb[collection]
    today = datetime.utcnow().day
    values = []
    for element in col.find(query):
        if ObjectId(element["_id"]).generation_time.day == today:
            values.append(element[key])
    return values

def cleanServer():
    mydb["comments"].drop()
    mydb["events"].drop()
    mydb["tweets"].drop()
    
def logIn(username):
    logEvent("open application",username)

#Unit tests
    
def test_PostTweet():
    testUser = "testuser"
    testTweet = "testTweet"
    PostTweet(testUser,testTweet)
    assert GetLatestTweets(1)[0]["user"] == testUser
    assert GetLatestTweets(1)[0]["tweet"] == testTweet
    testUser = ""
    testTweet = ""
    PostTweet(testUser,testTweet)
    assert GetLatestTweets(1)[0]["user"] == testUser
    assert GetLatestTweets(1)[0]["tweet"] == testTweet
    
 
def test_log():
    testEvent = "testuser"
    testUser = "testTweet"
    logEvent(testEvent,testUser)
    assert getEvents().sort("_id",-1)[0]["user"] == testUser
    assert getEvents().sort("_id",-1)[0]["event"] == testEvent
    testEvent = ""
    testUser = ""
    logEvent(testEvent,testUser)
    assert getEvents().sort("_id",-1)[0]["user"] == testUser
    assert getEvents().sort("_id",-1)[0]["event"] == testEvent
    
def test_getTweet():
    assert GetTweet("647822545933ac69e9db0fd0")["tweet"] == "n Hola amigos"
    assert GetTweet("647822545933ac69e9db0f30") == None