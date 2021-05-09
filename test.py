#!flask/bin/python
import sys
from flask import Flask, render_template, request, redirect, Response
import random, json
app = Flask(__name__)

@app.route('/')
def output():
	# serve index template
	return render_template('acvlanding.html')

@app.route('/receiver', methods = ['POST'])
def worker():
	# read json + reply
	data = request.get_json()
	
	pick_up = str(data[0]['pu'])
	deliv = str(data[1]['del'])
	dollar = str(data[2]['minDollar'])
	dist = str(data[3]['maxDist'])
	inop = str(data[4]['inop'])
	print(pick_up)
	print(deliv)
	print(dollar)
	print(dist)
	print(inop)
	return 'OK'
if __name__ == '__main__':
	# run!
	app.run()