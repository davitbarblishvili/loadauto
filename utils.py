import requests
import searcher





def count_words_at_url(pick_up_state,dollar, minTotalDollar,dist,condition):  
    searcher.acv.one_way(pick_up_state,dollar,minTotalDollar,dist,condition)
    message = str(pick_up_state) + " " + str(dollar)  + " " + str(minTotalDollar) + " " + str(dist) + " " + str(condition)
    print(message)
    return message
    