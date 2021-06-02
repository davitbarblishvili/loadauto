import searcher

def one_state_search(acv,pick_up_state,dollar, minTotalDollar,dist,condition):  
    print("inside the function")
    acv.one_way(pick_up_state,dollar,minTotalDollar,dist,condition)
    return 'OK'

def two_state_search(acvObj,pick_up_state,delivery_state, dollar, minTotalDollar,dist,condition):  
    acv = acvObj
    acv.initDatabase()
    acv.setUp()
    acv.login()
    acv.two_way(pick_up_state,delivery_state, dollar,minTotalDollar,dist,condition)
    return 'OK'
    