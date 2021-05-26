from flask import Flask, render_template, request
from rq import Queue, job
from worker import conn
from utils import one_state_search
from utils import two_state_search
from rq import cancel_job

       
app = Flask(__name__)
job_id = 0
q = Queue(connection=conn)
q.empty()


@app.route('/')
def output():
# serve index template
	return render_template('acvlanding.html')

@app.route('/receiver', methods = ['POST','GET'])
def server_worker():
    global job_id
    data = request.get_json()
    pick_up = data[0]['pu']
    if pick_up == 'stop':
        print("this is global result id" + str(job_id))
        cancel_job(str(job_id),connection=conn)
        q.empty()
        return 'OK'
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
        print("searching again")
        for i in pick_up:
            result = q.enqueue(one_state_search, i,dollar, minTotalDollar,dist,condition)
            job_id = result.id  
            q.empty()
            print("this is nested result id" + str(job_id))
        return 'OK'
        
         
    if len(deliv) >= 1 and deliv[0]:
        for i in pick_up:
            for j in deliv:
                result = q.enqueue(two_state_search, i,j, dollar, minTotalDollar,  dist, condition)
        return 'OK'
            
    

if __name__ == "__main__":
    app.run(threaded=True)
    
    
 
    
   
   


    





   
    
   
    



 



