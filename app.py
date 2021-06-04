from flask import Flask, render_template, request
from rq import Queue
from worker import conn
from utils import one_state_search
from utils import two_state_search
from rq.registry import StartedJobRegistry
from rq.command import send_stop_job_command
from searcher import *
from rq import get_current_job
import time


       
app = Flask(__name__)
class mainApp():
    q = Queue(connection=conn)
    q.empty()
    
    
    @app.route('/')
    def output():
    # serve index template
        return render_template('acvlanding.html')

    @app.route('/receiver', methods = ['POST','GET'])
    def server_worker():
    
        data = request.get_json()
        pick_up = data[0]['pu']     
        if pick_up == 'stop':
            registry = StartedJobRegistry(connection=conn)
            running_job_ids = registry.get_job_ids()
            print(running_job_ids)
            jobId = str(data[1]['jobid'])
            send_stop_job_command(conn, jobId )
            return 'OK'
        deliv = data[1]['del']
        minTotalDollar = str(data[2]['minTotal'])
        dollar = str(data[3]['minDollar'])
        dist = str(data[4]['maxDist'])
        condition = str(data[5]['inop'])
        jobid = str(data[6]['jobid'])
        
    
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
                result = mainApp.q.enqueue(one_state_search, args=(i,dollar, minTotalDollar,dist,condition),job_id=jobid,job_timeout=-1)
            return 'OK'
            
            
        if len(deliv) >= 1 and deliv[0]:
            for i in pick_up:
                for j in deliv:
                    result = mainApp.q.enqueue(two_state_search,args=(i,j, dollar, minTotalDollar,  dist, condition),job_timeout=-1)
            return 'OK'
            
    

if __name__ == "__main__":
    app.run(threaded=True)
    mainapp = mainApp()
    
    
 
    
   
   


    





   
    
   
    



 



