import requests

def count_words_at_url(pick_up_state,dollar, minTotalDollar,dist,condition):
    message = pick_up_state + dollar + minTotalDollar + dist + condition
    return message
    