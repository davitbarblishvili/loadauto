import searcher

def one_state_search(pick_up_state,dollar, minTotalDollar,dist,condition):  
    print("inside the function")
    acv = searcher.acv()
    acv.initDatabase()
    acv.setUp()
    acv.login()
    return 'OK',acv.one_way(pick_up_state,dollar,minTotalDollar,dist,condition)

def two_state_search(pick_up_state,delivery_state, dollar, minTotalDollar,dist,condition):  
    acv = searcher.acv()
    acv.initDatabase()
    acv.setUp()
    acv.login()
    acv.two_way(pick_up_state,delivery_state, dollar,minTotalDollar,dist,condition)
    return 'OK'
    