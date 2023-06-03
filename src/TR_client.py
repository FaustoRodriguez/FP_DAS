from ScreenPrinter import twitterPrinter
import TR_server

class client():
    
    def __init__(self):
        self.user = input("Introduzca su nombre de usuario: ")
        self.server = TR_server.client_server_connection(self.user)
        self.sp = twitterPrinter.getInstance()
        
        while(True):
            tweets = self.startScreen()
            command = input("\nSeleccione una opcion:\n Responder tweet: -r numTweet\n Abrir Thread: -t numThread\n Escribir nuevo tweet: -n textoTweet \n Cargar nuevos tweets: -c\n")
            if "-r" in command:
                if int(command[2:]) > 0 and int(command[2:]) <= len(tweets):
                    self.replyTweet(tweets[int(command[2:]) - 1]["_id"],self.user)
                    continue
            elif "-t" in command:
                if int(command[2:]) > 0 and int(command[2:]) <= len(tweets) and tweets[int(command[2:])- 1]["type"] == "thread":
                    self.openThread(tweets[int(command[2:]) - 1]["_id"])
                    continue
                else:
                    print("Esto no es un thread\n")
                    continue
            elif "-n" in command:
                if len(command) < 302:
                    self.server.PostTweet(self.user,command[2:])
                else:
                    print("Tweet de más de 300 caracteres")
                    continue
            elif "-c" in command:
                continue
            else:
                print("Opcion no valida")
            input()

    def startScreen(self):
        tweets = self.server.GetLatestTweets(10)
        self.sp.printScreen(tweets,self.user)
        return tweets

    def replyTweet(self,tweetID,user):
        while(True):
            comment = input("Introduzca su respuesta: ")
            if len(comment) < 301:
                self.server.PostComment(tweetID,user,comment)
                break
            else:
                print("Comentario mayor a 300 caracteres")

    def openThread(self,tweetID):
        self.sp.clearScreen
        tweet = self.server.GetTweet(tweetID)
        comments = self.server.GetComments(tweetID)
        print("Abriendo thread")
        self.sp.printTweet(tweet,1)
        self.sp.printComments(comments)
        input("Inserte -r para regresar al inicio\n")

client()