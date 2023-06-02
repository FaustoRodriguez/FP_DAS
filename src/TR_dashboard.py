import TR_server
import os


while(True):
    selection = int(input("Select options:\n See events dashboard (1)\n See usage reports (2)\n"))
    if selection == 1:
        print("Action\t\t\tUser\t\t\tTimestamp")
        for event in TR_server.getEvents():
            print(event["actionType"],"\t\t",event["user"],"\t\t",TR_server.getTimeStamp(str(event["_id"])))
    elif selection == 2:
        print("The user who registered the most actions is ", TR_server.GetTodayMostActiveUser())
        print("The tweet with most replies is ", TR_server.GetTodayMostCommentedTweet())
        print("Today this app was used by ",TR_server.GetTodayUsers(), " users")
    else:
        print("Not valid option ")
    input("Enter to reload dashboard")
    os.system("clear")
    