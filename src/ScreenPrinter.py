from abc import abstractmethod
from TR_server import objId
import os

class screenPrinter():
    @abstractmethod
    def printScreen(self):
        pass
    
    @abstractmethod
    def printTweet(self):
        pass
    
    def clearScreen(self):
        os.system("clear")
    
class twitterPrinter(screenPrinter):
    
    __instance = None
    @staticmethod 
    def getInstance():
        if twitterPrinter.__instance == None:
            twitterPrinter()
        return twitterPrinter.__instance
    
    def __init__(self):
        super().__init__()
        if twitterPrinter.__instance != None:
            raise Exception("This class is a singleton!")
        else:
            twitterPrinter.__instance = self

    def printTweet(self,tweet,nTweet):
        tweetstr = "("+ str(nTweet) +") " + tweet["user"]
        if tweet["type"] == "thread":
            tweetstr = tweetstr + " (Thread)"
        tweetstr = tweetstr + ": " + tweet["tweet"]
        print(tweetstr)
        
    def printComments(self,comments):
        for comment in comments:
            commentstr = "\t" + comment["user"] + ": " + comment["comment"]
            print(commentstr)
    
    def printScreen(self,tweets,user):
        self.clearScreen()
        print("Inicio")
        print("Bienvenido ", user,"\n")
        for nTweet in range(len(tweets)):
            self.printTweet(tweets[nTweet],nTweet+1)
        return tweets
    
    
class dashboardPrinter(screenPrinter):
    
    __instance = None
    @staticmethod 
    def getInstance():
        if dashboardPrinter.__instance == None:
            dashboardPrinter()
        return dashboardPrinter.__instance
    
    def __init__(self):
        super().__init__()
        if dashboardPrinter.__instance != None:
            raise Exception("This class is a singleton!")
        else:
            dashboardPrinter.__instance = self
            
    def printScreen(self):
        try:
            selection = int(input("Select options:\n See events dashboard (1)\n See usage reports (2)\n"))
            if selection == 1 or selection == 2:
                return selection
            else:
                self.clearScreen()
                return self.printScreen()
        except:
            self.clearScreen()
            return self.printScreen()
        
    def printEvents(self,events):
        print("Action\t\t\t\tUser\t\t\tTimestamp")
        for event in events:
            print(event["actionType"],"\t\t\t",event["user"],"\t\t",objId.getTimeStamp(str(event["_id"])))
    
    def printLine(self,line):
        print(line)
    
    def printLines(self,lines):
        for line in lines:
            self.printLine(line)
            
    def printTweet(self,tweet):
        print(tweet["tweet"]," by user: ",tweet["user"])