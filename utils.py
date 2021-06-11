import searcher
from rq import get_current_job

def no_filter_search(pick_up_state,delivery_state):
    acv = searcher.acv()
    acv.initDatabase()
    acv.setUp()
    acv.login()

    print("inside the function no filter")
    if len(delivery_state) == 1 and delivery_state[0] == '':
        print("inside the function no filter")
        acv.one_way_no_filter(pick_up_state)
        return 'OK'
    
    acv.two_way_no_filter(pick_up_state,delivery_state)
    return 'OK'
    


def one_state_search(pick_up_state,dollar, minTotalDollar,dist,condition):  
    print("inside the function one way")
    acv = searcher.acv()
    acv.initDatabase()
    acv.setUp()
    acv.login()
    acv.one_way(pick_up_state,dollar,minTotalDollar,dist,condition)
    return 'OK'

def two_state_search(pick_up_state,delivery_state, dollar, minTotalDollar,dist,condition):  
    print("inside the function two way")
    acv = searcher.acv()
    acv.initDatabase()
    acv.setUp()
    acv.login()
    acv.two_way(pick_up_state,delivery_state, dollar,minTotalDollar,dist,condition)
    return 'OK'
    