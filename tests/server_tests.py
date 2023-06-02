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