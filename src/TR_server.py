import pymongo
from bson.objectid import ObjectId
from datetime import datetime
from collections import Counter

class server_connection():
    
    __events = "events"
    __tweets = "tweets"
    __comments = "comments"
    
    def __init__(self,username):        
        server = pymongo.MongoClient("mongodb://localhost:27017/")
        self.__db = server["mydatabase"]
        self.__logIn(username)
        
    def __logEvent(self,actionType,user):
        self.__db[self.__events].insert_one({"actionType":actionType,"user":user})
        
    def PostTweet(self,user,tweet):
        self.__db[self.__tweets].insert_one({"user":user,"tweet":tweet,"type":"tweet"})
        self.__logEvent("create tweet",user)
    
    def __isThread(self,tweetID):
        return self.__db[self.__tweets].find({"_id":ObjectId(tweetID)})[0]["type"] == "thread"
    
    def __makeThread(self,tweetID):
        self.__db[self.__tweets].update_one({"_id":ObjectId(tweetID)},{"$set":{"type":"thread"}})
        
    def PostComment(self,tweetID,user,comment):
        self.__db[self.__comments].insert_one({"tweetID":tweetID,"user":user,"comment":comment})
        if not self.__isThread(tweetID):
            self.__makeThread(tweetID)
        self.__logEvent("reply tweet",user)
        
    def getTimeStamp(id):
        return ObjectId(id).generation_time
        
    def GetTweet(self,tweetID):
        for tweet in self.db[self.__tweets].find({"_id":ObjectId(tweetID)}):
            return tweet

    def GetComments(self,tweetID):
        return self.__db[self.__comments].find({"tweetID":tweetID})

    def getEvents(self):
        return self.__db[self.__events].find()

    def GetLatestTweets(self,nTweets):
        latestTweets = []
        for tweet in self.__db[self.__tweets].find().sort("_id", -1):
            nTweets -= 1
            latestTweets.append(tweet)
            if not nTweets :
                break
        return latestTweets

    def GetTodayUsers(self):
        users = Counter(self.__GetTodayValues("events",{"actionType":"open application"},"user"))
        return len(users)
    
    def __mostRepeatedValue(list):
        dict = Counter(list)
        v = list(dict.values())
        k = list(dict.keys())
        return k[v.index(max(v))]

    def GetTodayMostCommentedTweet(self):
        return self.__mostRepeatedValue(self.__GetTodayValues(self.__comments,{},"tweetID"))

    def GetTodayMostActiveUser(self):
        return self.__mostRepeatedValue(self.__GetTodayValues(self.__events,{},"user"))

    def __GetTodayValues(self,collection,query,key):
        today = datetime.utcnow().day
        values = []
        for element in self.__db[collection].find(query):
            if self.getTimeStamp(element["_id"]).day == today:
                values.append(element[key])
        return values
        
    def __logIn(self,username):
        self.__logEvent("open application",username)