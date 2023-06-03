import pymongo
from bson.objectid import ObjectId
from datetime import datetime
from collections import Counter

class calc():
    def mostRepeatedValue(arr):
        if len(arr) == 0:
            return "there's no one active yet today"
        dict = Counter(arr)
        v = list(dict.values())
        k = list(dict.keys())
        return k[v.index(max(v))]

class objId():
    def getTimeStamp(id):
        return ObjectId(id).generation_time 

class server_connection():
    
    _events = "events"
    _tweets = "tweets"
    _comments = "comments"
    
    def __init__(self):        
        server = pymongo.MongoClient("mongodb://localhost:27017/")
        self.__db = server["tweetdatabase"]
    
    def _postData(self,col,data):
        self.__db[col].insert_one(data)
        
    def _getData(self,col,query={}):
        return self.__db[col].find(query)
    
    def _updateData(self,col,query,newdata,update="one"):
        if update == "one":
            self.__db[col].update_one(query,newdata)
        elif update == "many":
            self.__db[col].update_many(query,newdata)

class client_server_connection(server_connection):
    def __init__(self,username):
        super().__init__()
        self.__logIn(username)
    
    def __logIn(self,username):
        self.__logEvent("open application",username)
    
    def GetComments(self,tweetID):
        return self._getData(self._comments,{"tweetID":tweetID})
    
    def GetTweet(self,tweetID):
        for tweet in self._getData(self._tweets,{"_id":ObjectId(tweetID)}):
            return tweet

    def GetLatestTweets(self,nTweets):
        latestTweets = []
        for tweet in self._getData(self._tweets).sort("_id", -1):
            nTweets -= 1
            latestTweets.append(tweet)
            if not nTweets :
                break
        return latestTweets
    
    def PostTweet(self,user,tweet):
        self._postData(self._tweets,{"user":user,"tweet":tweet,"type":"tweet"})
        self.__logEvent("create tweet",user)
    
    def __isThread(self,tweetID):
        return self.GetTweet(tweetID)["type"] == "thread"
    
    def __makeThread(self,tweetID):
        self._updateData(self._tweets,{"_id":ObjectId(tweetID)},{"$set":{"type":"thread"}},"one")
        
    def PostComment(self,tweetID,user,comment):
        self._postData(self._comments,{"tweetID":tweetID,"user":user,"comment":comment})
        if not self.__isThread(tweetID):
            self.__makeThread(tweetID)
        self.__logEvent("reply tweet",user)
        
    def __logEvent(self,actionType,user):
        self._postData(self._events,{"actionType":actionType,"user":user})

class dash_server_connection(server_connection):
    
    def __init__(self):
        super().__init__()
    
    def GetEvents(self):
        return self._getData(self._events)
    
    def GetTodayUsers(self):
        users = Counter(self.__GetTodayValues("events",{"actionType":"open application"},"user"))
        return len(users)

    def GetTodayMostCommentedTweet(self):
        return calc.mostRepeatedValue(self.__GetTodayValues(self._comments,{},"tweetID"))

    def GetTodayMostActiveUser(self):
        return calc.mostRepeatedValue(self.__GetTodayValues(self._events,{},"user"))

    def __GetTodayValues(self,collection,query,key):
        today = datetime.utcnow().day
        values = []
        for element in self._getData(collection,query):
            if objId.getTimeStamp(element["_id"]).day == today:
                values.append(element[key])
        return values
    def GetTweet(self,tweetID):
        try:
            obj = ObjectId(tweetID)
        except:
            return "Tweet not Found"
        for tweet in self._getData(self._tweets,{"_id":obj}):
            return tweet