import searcher



def one_state_search(pick_up_state,dollar, minTotalDollar,dist,condition):  
    acv = searcher.acv()
    acv.initDatabase()
    acv.setUp()
    acv.login()
    print("ready")
    message = str(pick_up_state) + " " + str(dollar)  + " " + str(minTotalDollar) + " " + str(dist) + " " + str(condition)
    print(message)
    acv.one_way(pick_up_state,dollar,minTotalDollar,dist,condition)
    return "200"

def two_state_search(pick_up_state,delivery_state, dollar, minTotalDollar,dist,condition):  
    acv = searcher.acv()
    acv.initDatabase()
    acv.setUp()
    acv.login()
    print("ready")
    message = str(pick_up_state) + " " + str(dollar)  + " " + str(minTotalDollar) + " " + str(dist) + " " + str(condition)
    print(message)
    acv.two_way(pick_up_state,delivery_state, dollar,minTotalDollar,dist,condition)
    return "200"
    