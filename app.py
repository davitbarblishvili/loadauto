from flask import Flask, render_template, request
from rq import Queue
from worker import conn
from utils import one_state_search
from utils import two_state_search
       
app = Flask(__name__)
q = Queue(connection=conn)


@app.route('/')
def output():
# serve index template
	return render_template('acvlanding.html')

@app.route('/receiver', methods = ['POST','GET'])
def worker():

    data = request.get_json()
    pick_up = data[0]['pu']
    deliv = data[1]['del']
    minTotalDollar = str(data[2]['minTotal'])
    dollar = str(data[3]['minDollar'])
    dist = str(data[4]['maxDist'])
    condition = str(data[5]['inop'])

    dollar = 0.0 if dollar == '' or dollar == '---' else float(dollar)
    minTotalDollar = 0.0 if minTotalDollar == '' or minTotalDollar == '---' else float(minTotalDollar)
    dist = float("inf") if dist == '' or dist == '---' else float(dist)
        
    if condition == 'Operable':
        condition = 'Good'
    if condition == 'Inoperable':
        condition = 'INOP'

    if len(deliv) == 1 and deliv[0] == '':
        for i in pick_up:
            result = q.enqueue(one_state_search, i,dollar, minTotalDollar,dist,condition)
        
        return
         

    if len(deliv) >= 1 and deliv[0]:
        for i in pick_up:
            for j in deliv:
                result = q.enqueue(two_state_search, i,j, dollar, minTotalDollar,  dist, condition)
        return

if __name__ == "__main__":
    app.run(threaded=True)
    
    
 
    
   
   


    





   
    
   
    



 



