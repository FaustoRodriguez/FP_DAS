import TR_server
import os

server = TR_server.dash_server_connection()

while(True):
    selection = int(input("Select options:\n See events dashboard (1)\n See usage reports (2)\n"))
    if selection == 1:
        print("Action\t\t\t\tUser\t\t\tTimestamp")
        for event in server.getEvents():
            print(event["actionType"],"\t\t\t",event["user"],"\t\t",server.getTimeStamp(str(event["_id"])))
    elif selection == 2:
        print("The user who registered the most actions is ", server.GetTodayMostActiveUser())
        mostRepliedTweet = server.GetTweet(server.GetTodayMostCommentedTweet())
        if type(mostRepliedTweet) == type(""):
            print("There's been no replies to any tweet today")
        else:
            print("The tweet with most replies is \"", mostRepliedTweet["tweet"], "\" by ", mostRepliedTweet["user"])
        print("Today this app was used by ",server.GetTodayUsers(), " users")
    else:
        print("Not valid option ")
    input("Enter to reload dashboard")
    os.system("clear")
    