from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import firebase_admin
from selenium.webdriver.chrome.options import Options
from firebase_admin import credentials
from firebase_admin import firestore
import time
import unittest
import json
import os
from twilio.rest import Client
import sys
from flask import Flask, render_template, request, redirect, Response, jsonify
import random, json


class acv(unittest.TestCase):
   
    def sendMessage(self,textMessage):
        account_sid = 'ACfdaf54ef106ea4f48fae9e78588cd69e'
        auth_token = 'fb15a4c98079021641376ca358215f79'
        client = Client(account_sid, auth_token)

        numbers_to_message = ['+19294997605']
        for number in numbers_to_message:
            message = client.messages \
                .create(
            body= textMessage,
            from_= '+13016793819',
            to= number
            ) 


    def initDatabase(self):

        cred = credentials.Certificate("./acvdatabase-firebase-adminsdk-er7dp-d4bdc9c2cf.json")
        firebase_admin.initialize_app(cred)
        

    def addData(self, load):
        data = {
            u'staged': True
        }
        db = firestore.client()
        db.collection(u'loadIds').document(load).set(data)

    def checkData(self, load):
        db = firestore.client()
        doc_ref = db.collection('loadIds').document(load)
        doc = doc_ref.get()
        if doc.exists:
            return True
        else:
            return False

        
    def setUp(self):
        option = webdriver.ChromeOptions()

        GOOGLE_CHROME_PATH = '/app/.apt/usr/bin/google-chrome'
        CHROMEDRIVER_PATH = '/app/.chromedriver/bin/chromedriver'
        option.add_argument('headless')
        option.add_argument('--disable-gpu')
        option.add_argument('--no-sandbox')
        option.binary_location = GOOGLE_CHROME_PATH
        self.webdriver = webdriver.Chrome(executable_path=CHROMEDRIVER_PATH,options=option)
        self.webdriver.get("https://transport.acvauctions.com/jobs/available.php")
    
    def close(self):
        self.webdriver.close()

    def login(self):
        time.sleep(2)
        username = self.webdriver.find_element_by_xpath("//input[@name='email']")
        self.webdriver.execute_script("arguments[0].click();", username)
        username.send_keys("righttimenyc@yahoo.com")
        password = self.webdriver.find_element_by_xpath("//input[@name='password']")
        self.webdriver.execute_script("arguments[0].click();", password)
        password.send_keys("Tsikara95#")
        password.send_keys(Keys.ENTER)

        
    def refreshPage(self):
        time.sleep(1)
        self.webdriver.find_element_by_xpath("(//input[@class='btnstyle'])[1]").click()
    
    def stage_load_all_loads(self,load):
        acv.addData(load)
        acv.setUp()
        acv.login()
        time.sleep(1)
        search_tab = self.webdriver.find_element_by_xpath("//input[@name='search_txt']")
        self.webdriver.execute_script("arguments[0].click();", search_tab)
        search_tab.send_keys(load)

        filter_tab = self.webdriver.find_element_by_xpath("//input[@name='Filter']")
        self.webdriver.execute_script("arguments[0].click();", filter_tab)

        time.sleep(1)
        check_button = self.webdriver.find_element_by_xpath("(//input[@type= 'checkbox'])[2]")
        self.webdriver.execute_script("arguments[0].click();", check_button)

        if self.webdriver.find_element_by_xpath("(//input[@type= 'checkbox'])[2]").is_selected():
            select_button = self.webdriver.find_element_by_xpath("//input[@name='Submit']")
            self.webdriver.execute_script("arguments[0].click();", select_button)
        
        acv.close()
        return
    
    def one_way(self,pick_up,dollar,minDollar, dist, condition):
        acv.setUp()
        acv.login()
        time.sleep(1)
        self.webdriver.find_element_by_xpath("//select[@name='p_filter']/option[text()='"+ pick_up + "']").click()
        filter_tab = self.webdriver.find_element_by_xpath("//input[@name='Filter']")
        self.webdriver.execute_script("arguments[0].click();", filter_tab)
        acv.iterateStatesOneWay(pick_up, dollar, minDollar, dist, condition)

    def two_way(self, pick_up, delivery, dollar, minDollar,  dist, condition):
        acv.setUp()
        acv.login()
        time.sleep(2)
        self.webdriver.find_element_by_xpath("//select[@name='p_filter']/option[text()='"+ pick_up + "']").click()
        self.webdriver.find_element_by_xpath("//select[@name='d_filter']/option[text()='"+ delivery + "']").click()
        filter_tab = self.webdriver.find_element_by_xpath("//input[@name='Filter']")
        self.webdriver.execute_script("arguments[0].click();", filter_tab)
        acv.iterateStatesTwoWay(pick_up, delivery, dollar, minDollar, dist, condition)

    def local_zips(self,s_zip, e_zip):
        acv.setUp()
        acv.login()
        acv.iterateLocal(s_zip,e_zip)

    
    def iterateStatesTwoWay(self,pick_up,delivery,dollar,minDollar,  dist, condition):
        if dollar == '' or dollar == '---':
            dollar = 0.0
        else: 
            dollar = float(dollar)

        if minDollar == '' or minDollar == '---':
            minDollar = 0.0
        else: 
            minDollar = float(minDollar)

        
        if dist == '' or dist == '---':
            dist = float("inf")
        else:
            dist = float(dist)

        if condition == 'Operable':
            condition = 'Good'
        if condition == 'Inoperable':
            condition = 'INOP'
        
        if condition == 'Both' or condition == '':
            acv.iterateStatesTwoWayHelper(pick_up, delivery, dollar, minDollar, dist, condition)
            return

        self.webdriver.find_element_by_xpath("//select[@name='perpage']/option[text()='All']").click()
        table = self.webdriver.find_element_by_xpath("//table[2]")
        for row in table.find_elements_by_xpath(".//tr[@class='rowheight']"):
            info_array = [] 
            check_box = row.find_elements_by_xpath(".//input[@type='checkbox']")
            for td in row.find_elements_by_xpath(".//td[@class='arial14']"):      
                if td.text:
                    info_array.append(td.text)
            if acv.checkData(info_array[0]) == False:
                distance = info_array[12]
                if distance == '---':
                    continue
                pay = info_array[13][1:]
                if float(pay)/float(distance) >= dollar and float(distance) < dist:
                    if info_array[3] == condition and minDollar <= float(pay):  
                        self.webdriver.execute_script("arguments[0].click();", check_box[1])
                        select_button = self.webdriver.find_element_by_xpath("//input[@name='Submit']")
                        message = "Load ID: " + info_array[0] + "\nPick up: " + info_array[4] + " " + info_array[5] + "\n"
                        message += "Delivery: " + info_array[8] + " " + info_array[9] + "\n" + "Pay: " + info_array[13]
                        acv.sendMessage(message)
                        acv.addData(info_array[0])
                        self.webdriver.execute_script("arguments[0].click();", select_button)
                        acv.two_way(pick_up,delivery, dollar,minDollar,  dist, condition)
                        break
        acv.refreshPage()
        acv.iterateStatesTwoWay(pick_up,delivery, dollar, minDollar, dist, condition)
        
                       

    def iterateStatesTwoWayHelper(self,pick_up,delivery, dollar, minDollar,  dist, condition):
        if dollar == '' or dollar == '---':
            dollar = 0.0
        else: 
            dollar = float(dollar)

        if minDollar == '' or minDollar == '---':
            minDollar = 0.0
        else: 
            minDollar = float(minDollar)
        

        if dist == '' or dist == '---':
            dist = float("inf")
        else:
            dist = float(dist)

        if condition == 'Operable':
            condition = 'Good'
        if condition == 'Inoperable':
            condition = 'INOP'
        

        self.webdriver.find_element_by_xpath("//select[@name='perpage']/option[text()='All']").click()
        table = self.webdriver.find_element_by_xpath("//table[2]")
        for row in table.find_elements_by_xpath(".//tr[@class='rowheight']"):
            info_array = [] 
            check_box = row.find_elements_by_xpath(".//input[@type='checkbox']")
            for td in row.find_elements_by_xpath(".//td[@class='arial14']"):      
                if td.text:
                    info_array.append(td.text)
            if acv.checkData(info_array[0]) == False:
                distance = info_array[12]
                if distance == '---':
                    continue
                pay = info_array[13][1:]
                if float(pay)/float(distance) >= dollar and float(distance) < dist:
                    if minDollar <= float(pay):
                        self.webdriver.execute_script("arguments[0].click();", check_box[1])
                        select_button = self.webdriver.find_element_by_xpath("//input[@name='Submit']")
                        message = "Load ID: " + info_array[0] + "\nPick up: " + info_array[4] + " " + info_array[5] + "\n"
                        message += "Delivery: " + info_array[8] + " " + info_array[9] + "\n" + "Pay: " + info_array[13]
                        acv.sendMessage(message)
                        acv.addData(info_array[0])
                        self.webdriver.execute_script("arguments[0].click();", select_button)
                        acv.two_way(pick_up,delivery, dollar, minDollar, dist, condition)
                        break
        acv.refreshPage()
        acv.iterateStatesTwoWayHelper(pick_up,delivery, dollar, minDollar,  dist, condition)
                                
        
    

    def iterateStatesOneWay(self,pick_up, dollar,minDollar,  dist, condition):
        if dollar == '' or dollar == '---':
            dollar = 0.0
        else: 
            dollar = float(dollar)

        if minDollar == '' or minDollar == '---':
            minDollar = 0.0
        else: 
            minDollar = float(minDollar)
        

        if dist == '' or dist == '---':
            dist = float("inf")
        else:
            dist = float(dist)

        if condition == 'Operable':
            condition = 'Good'
        if condition == 'Inoperable':
            condition = 'INOP'

        if condition == 'Both' or condition == '':
            acv.iterateStatesOneWayHelper(pick_up, dollar, minDollar,  dist, condition)
            return
        
        self.webdriver.find_element_by_xpath("//select[@name='perpage']/option[text()='All']").click()
        table = self.webdriver.find_element_by_xpath("//table[2]")
        for row in table.find_elements_by_xpath(".//tr[@class='rowheight']"):
            info_array = [] 
            check_box = row.find_elements_by_xpath(".//input[@type='checkbox']")
            for td in row.find_elements_by_xpath(".//td[@class='arial14']"):      
                if td.text:
                    info_array.append(td.text)
            if acv.checkData(info_array[0]) == False:
                distance = info_array[12]
                if distance == '---':
                    continue
                pay = info_array[13][1:]
                if float(pay)/float(distance) >= dollar and float(distance) < dist: 
                    if info_array[3] == condition and minDollar <= float(pay):
                        self.webdriver.execute_script("arguments[0].click();", check_box[1])
                        select_button = self.webdriver.find_element_by_xpath("//input[@name='Submit']")
                        message = "Load ID: " + info_array[0] + "\nPick up: " + info_array[4] + " " + info_array[5] + "\n"
                        message += "Delivery: " + info_array[8] + " " + info_array[9] + "\n" + "Pay: " + info_array[13]
                        acv.sendMessage(message)
                        acv.addData(info_array[0])
                        self.webdriver.execute_script("arguments[0].click();", select_button)
                        acv.one_way(pick_up,dollar,minDollar, dist,condition)
                        
        acv.refreshPage()
        return "OK", acv.iterateStaesOneWay(pick_up, dollar, minDollar, dist, condition)
                                
        
    
    def iterateStatesOneWayHelper(self,pick_up, dollar,minDollar,  dist, condition):
        if dollar == '' or dollar == '---':
            dollar = 0.0
        else: 
            dollar = float(dollar)
        
        if minDollar == '' or minDollar == '---':
            minDollar = 0.0
        else: 
            minDollar = float(minDollar)

        

        if dist == '' or dist == '---':
            dist = float("inf")
        else:
            dist = float(dist)

    
        self.webdriver.find_element_by_xpath("//select[@name='perpage']/option[text()='All']").click()
        table = self.webdriver.find_element_by_xpath("//table[2]")
        for row in table.find_elements_by_xpath(".//tr[@class='rowheight']"):
            info_array = [] 
            check_box = row.find_elements_by_xpath(".//input[@type='checkbox']")
            for td in row.find_elements_by_xpath(".//td[@class='arial14']"):      
                if td.text:
                    info_array.append(td.text)
            if acv.checkData(info_array[0]) == False:
                distance = info_array[12]
                if distance == '---':
                    continue
                pay = info_array[13][1:]
                if float(pay)/float(distance) >= dollar and float(distance) < dist: 
                    if minDollar <= float(pay):
                        self.webdriver.execute_script("arguments[0].click();", check_box[1])
                        select_button = self.webdriver.find_element_by_xpath("//input[@name='Submit']")
                        message = "Load ID: " + info_array[0] + "\nPick up: " + info_array[4] + " " + info_array[5] + "\n"
                        message += "Delivery: " + info_array[8] + " " + info_array[9] + "\n" + "Pay: " + info_array[13]
                        acv.sendMessage(message)
                        acv.addData(info_array[0])
                        self.webdriver.execute_script("arguments[0].click();", select_button)
                        acv.one_way(pick_up,dollar,minDollar,  dist, condition)
                        break
        acv.refreshPage()
        acv.iterateStaesOneWayHelper(pick_up, dollar, minDollar, dist, condition)
                                
       
    def iterateLocal(self,s_zip,e_zip):
        self.webdriver.find_element_by_xpath("//select[@name='perpage']/option[text()='All']").click()
        table = self.webdriver.find_element_by_xpath("//table[2]")
        for row in table.find_elements_by_xpath(".//tr[@class='rowheight']"):
            info_array = [] 
            check_box = row.find_elements_by_xpath(".//input[@type='checkbox']")
            for td in row.find_elements_by_xpath(".//td[@class='arial14']"):      
                if td.text:
                    info_array.append(td.text)
            if acv.checkData(info_array[0]) == False:
                distance = info_array[12]
                pay = info_array[13][1:]
                if float(pay)/float(distance) >= 2.00:
                    if s_zip <= int(info_array[7]) <= e_zip and info_array[3] == "Good":
                        self.webdriver.execute_script("arguments[0].click();", check_box[1])
                        select_button = self.webdriver.find_element_by_xpath("//input[@name='Submit']")
                        message = "Load ID: " + info_array[0] + "\nPick up: " + info_array[4] + " " + info_array[5] + "\n"
                        message += "Delivery: " + info_array[8] + " " + info_array[9] + "\n" + "Pay: " + info_array[13]
                        acv.sendMessage(message)
                        acv.addData(info_array[0])
                        self.webdriver.execute_script("arguments[0].click();", select_button)
                        acv.local_zips(s_zip,e_zip)
                        break
                                
       
app = Flask(__name__)

acv = acv()
acv.initDatabase()

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
    inop = str(data[5]['inop'])

    response = 'ok'


    if len(deliv) == 1 and deliv[0] == '':
        for i in pick_up:
            return jsonify(response),acv.one_way(i,dollar,minTotalDollar, dist,inop)

    if len(deliv) >= 1 and deliv[0]:
        for i in pick_up:
            for j in deliv:
                acv.two_way(i,j, dollar, minTotalDollar,  dist, inop)

       
     
if __name__ == "__main__":
    app.run(threaded=True)
    
    
 
    
   
   


    





   
    
   
    



 



