import TR_server,os

username = input("Introduzca su nombre de usuario: ")
server = TR_server.server_connection(username)

def printTweet(tweet,nTweet):
    tweetstr = "("+ str(nTweet) +") "+tweet["user"]
    if tweet["type"] == "thread":
        tweetstr = tweetstr + " (Thread)"
    tweetstr = tweetstr + ": " + tweet["tweet"]
    print(tweetstr)

def printComments(comments):
    for comment in comments:
        commentstr = "\t" + comment["user"] + ": " + comment["comment"]
        print(commentstr)

def dashboard(user):
    os.system("clear")
    print("Inicio")
    print("Bienvenido ", user,"\n")
    tweets = server.GetLatestTweets(10)
    for nTweet in range(len(tweets)):
        printTweet(tweets[nTweet],nTweet+1)
    return tweets

def replyTweet(tweetID,user):
    while(True):
        comment = input("Introduzca su respuesta: ")
        if len(comment) < 301:
            server.PostComment(tweetID,user,comment)
            break
        else:
            print("Comentario mayor a 300 caracteres")

def openThread(tweetID):
    os.system("clear")
    tweet = server.GetTweet(tweetID)
    comments = server.GetComments(tweetID)
    print("Abriendo thread")
    printTweet(tweet,1)
    printComments(comments)
    input("Inserte -r para regresar al inicio\n")

while(True):
    tweets = dashboard(username)
    command = input("\nSeleccione una opcion:\n Responder tweet: -r numTweet\n Abrir Thread: -t numThread\n Escribir nuevo tweet: -n textoTweet \n Cargar nuevos tweets: -c\n")
    if "-r" in command:
        if int(command[2:]) > 0 and int(command[2:]) <= len(tweets):
            replyTweet(tweets[int(command[2:]) - 1]["_id"],username)
            continue
    elif "-t" in command:
        if int(command[2:]) > 0 and int(command[2:]) <= len(tweets) and tweets[int(command[2:])- 1]["type"] == "thread":
            openThread(tweets[int(command[2:]) - 1]["_id"])
            continue
        else:
            print("Esto no es un thread\n")
    elif "-n" in command:
        if len(command) < 302:
            server.PostTweet(username,command[2:])
        else:
            print("Tweet de más de 300 caracteres")
        continue
    elif "-c" in command:
        continue
    else:
        print("Opcion no valida")
    input()