from TR_server import dash_server_connection
from ScreenPrinter import dashboardPrinter

class dashboard():
    def __init__(self):
        server = dash_server_connection()
        sp = dashboardPrinter.getInstance()
        while(True):
            selection = sp.printScreen()
            if selection == 1:
                sp.printEvents(server.GetEvents())
            else:
                lines = []
                lines.append("The user who registered the most actions is " + server.GetTodayMostActiveUser())
                mostRepliedTweet = server.GetTweet(server.GetTodayMostCommentedTweet())
                if type(mostRepliedTweet) == type(""):
                    lines.append("There's been no replies to any tweet today")
                    sp.printLines(lines)
                else:
                    lines.append("The tweet with most replies is: ")
                    sp.printLines(lines)
                    sp.printTweet(mostRepliedTweet)
                sp.printLine("Today this app was used by " + str(server.GetTodayUsers()) + " users")
                
            input("Enter to reload dashboard ")

dashboard()